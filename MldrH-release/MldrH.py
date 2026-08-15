# -*- coding: utf-8 -*-
"""Portable MldrH v1.1: CPU retrieval plus local CUDA BF16 PEFT generation."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from threading import Event, Thread

import chromadb
import torch
from peft import PeftModel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
SYSTEM_PROMPT = ROOT / "system_prompt.txt"
THINK_PROMPT = ROOT / "think_system_prompt.txt"
THINK_EXPANSION_PROMPT = ROOT / "think_expansion_prompt.txt"
RULE = "-" * 56


@dataclass
class State:
    top_k: int = 8
    count: int = 0
    think: bool = True
    sources: list[dict] = field(default_factory=list)
    question: str = ""
    answer: str = ""


class CancelCriteria(StoppingCriteria):
    def __init__(self, event: Event) -> None:
        self.event = event

    def __call__(self, input_ids, scores, **kwargs) -> bool:
        return self.event.is_set()


def load_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError(f"Required prompt is empty: {path.name}")
    return text


def config() -> dict:
    if not CONFIG_PATH.exists():
        raise RuntimeError("Missing config.json. Run setup_mldrh.ps1 first.")
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    required = ("embedding_base_model", "generation_base_model", "retrieval_adapter", "think_adapter", "database_path")
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        raise RuntimeError("config.json fields missing: " + ", ".join(missing))
    return data


def asset_paths(data: dict) -> dict[str, Path]:
    names = ("embedding_base_model", "generation_base_model", "retrieval_adapter", "think_adapter", "database_path")
    paths = {name: Path(data[name]) for name in names}
    return {name: path if path.is_absolute() else ROOT / path for name, path in paths.items()}


def select_sources(rows: list[dict], limit: int = 4) -> list[dict]:
    selected, seen = [], set()
    for row in rows:
        if row["source"] not in seen:
            selected.append(row)
            seen.add(row["source"])
        if len(selected) == limit:
            break
    return selected


def context(rows: list[dict], budget: int = 3000) -> str:
    rows = select_sources(rows)
    parts = []
    for index, row in enumerate(rows):
        share = max(120, budget // max(1, len(rows) - index))
        text = row["document"][:share]
        parts.append(f"[Source {row['rank']}] {text}")
        budget -= len(text)
    return "\n\n".join(parts)


def messages(question: str, rows: list[dict], instruction: str, think: str | None = None) -> list[dict]:
    source_text = context(rows)
    if think is None:
        content = f"{question}/think\n\n{instruction}\n\nSources:\n{source_text}\n\n"
        content += "Only output <think>...</think>. Use exactly three concise bullet points beginning with ·, then close the tag.\n\n"
        content += load_text(THINK_EXPANSION_PROMPT)
        return [{"role": "system", "content": load_text(THINK_PROMPT)}, {"role": "user", "content": content}]
    content = f"Question: {question}\n\n{instruction}\n\nSources:\n{source_text}\n\nConfirmed reasoning summary:\n{think}\n\nOnly output <answer>...</answer>."
    return [{"role": "system", "content": load_text(SYSTEM_PROMPT)}, {"role": "user", "content": content}]


def extract(text: str, tag: str) -> str:
    match = re.search(fr"<{tag}>\s*(.*?)\s*</{tag}>", text, re.S | re.I)
    if match:
        return match.group(1).strip()
    partial = re.search(fr"<{tag}>\s*(.*?)(?:<answer>|$)", text, re.S | re.I)
    if partial:
        return partial.group(1).strip()
    text = re.sub(r"</?(?:think|answer)>", "", text, flags=re.I).strip()
    return text if tag == "think" and "·" in text else text if tag == "answer" else ""


def generate(generator, message_list: list[dict], options: dict, on_chunk=None) -> str:
    prompt = generator[0].apply_chat_template(message_list, tokenize=False, add_generation_prompt=True)
    inputs = {key: value.to(generator[1].device) for key, value in generator[0](prompt, return_tensors="pt").items()}
    streamer, event, errors = TextIteratorStreamer(generator[0], skip_prompt=True, skip_special_tokens=True), Event(), []

    def run() -> None:
        try:
            generator[1].generate(**inputs, streamer=streamer, stopping_criteria=StoppingCriteriaList([CancelCriteria(event)]), **options)
        except BaseException as error:
            errors.append(error)
            streamer.end()

    thread = Thread(target=run, daemon=True)
    thread.start()
    chunks = []
    try:
        for chunk in streamer:
            chunks.append(chunk)
            if on_chunk:
                on_chunk(chunk)
    except KeyboardInterrupt:
        event.set()
        thread.join()
        print("\n[ STOPPED ]")
    thread.join()
    torch.cuda.empty_cache()
    if errors:
        raise RuntimeError(str(errors[0]))
    return "".join(chunks)


def help_screen() -> None:
    print("COMMANDS\n  /sources  /continue [focus]  /suggest  /focus [focus]\n  /outline [topic]  /compare A | B  /analyze [text]\n  /think [on|off]  /top N  /status  /clear  /help  /exit")


def parse_command(text: str) -> tuple[str, str | int]:
    command, _, argument = text.partition(" ")
    if command == "/suggest":
        return "suggest", ""
    if command == "/top":
        if argument.isdigit() and 1 <= int(argument) <= 32:
            return "top", int(argument)
        return "error", "Use /top N where N is an integer from 1 to 32."
    return "query", text


def create_input_session() -> PromptSession:
    bindings = KeyBindings()

    @bindings.add("c-l")
    def clear(event) -> None:
        event.app.current_buffer.text = "/clear"
        event.app.current_buffer.validate_and_handle()

    @bindings.add("c-t")
    def toggle_think(event) -> None:
        event.app.current_buffer.text = "/think"
        event.app.current_buffer.validate_and_handle()

    return PromptSession(multiline=True, history=InMemoryHistory(), key_bindings=bindings)


def main() -> None:
    try:
        cfg = config()
        paths = asset_paths(cfg)
        required = [paths["embedding_base_model"] / "pytorch_model.bin", paths["generation_base_model"] / "config.json", paths["retrieval_adapter"] / "adapter_model.safetensors", paths["think_adapter"] / "adapter_model.safetensors", paths["database_path"] / "chroma.sqlite3"]
        if missing := [str(path) for path in required if not path.exists()]:
            raise RuntimeError("Missing asset:\n" + "\n".join(missing))
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA GPU is required for BF16 generation.")
        retriever = SentenceTransformer(str(paths["embedding_base_model"]), device="cpu", trust_remote_code=True)
        retriever.load_adapter(str(paths["retrieval_adapter"]))
        tokenizer = AutoTokenizer.from_pretrained(str(paths["generation_base_model"]), trust_remote_code=True)
        print("[ LOADING ] Qwen2.5-3B-Instruct + Mdlr1.1-think on CUDA BF16")
        model = AutoModelForCausalLM.from_pretrained(str(paths["generation_base_model"]), dtype=torch.bfloat16, device_map="cuda", trust_remote_code=True)
        model = PeftModel.from_pretrained(model, str(paths["think_adapter"])).eval()
        collection = chromadb.PersistentClient(path=str(paths["database_path"])).get_collection(cfg.get("collection_name", "theory_knowledge"))
    except Exception as error:
        print(f"MldrH could not start: {error}")
        raise SystemExit(1)

    state, generator = State(count=collection.count()), (tokenizer, model)
    print("\033[2J\033[H\n\n    MldrH\n    THEORY WORKBENCH · BF16 / PEFT · THINK ON\n" + RULE)
    help_screen()
    session = create_input_session()
    while True:
        try:
            question = session.prompt("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if question.lower() in {"/exit", "exit", "quit"}:
            break
        if question == "/clear":
            state.sources.clear(); state.question = state.answer = ""; print("\033[2J\033[H[ SESSION CLEARED ]"); continue
        if question.startswith("/think"):
            state.think = not question.endswith("off"); print(f"Think {'on' if state.think else 'off'}."); continue
        if question == "/sources":
            print("\n".join(f"{x['rank']}. {x['source']} [{x['type']}]" for x in state.sources) or "No sources yet."); continue
        if question == "/status":
            print(f"MldrH STATUS\n  Retrieval: CPU\n  Generation: Transformers + PEFT / CUDA BF16\n  Think: {'on' if state.think else 'off'}\n  Database: {state.count}"); continue
        if question == "/help": help_screen(); continue
        if not question: continue
        parsed, value = parse_command(question)
        if parsed == "suggest":
            print("FOLLOW-UP DIRECTIONS\n  1. Explain the mechanism in more detail.\n  2. Compare related concepts or opposing views.\n  3. Request theoretical grounds and examples.")
            continue
        if parsed == "top":
            state.top_k = value
            print(f"Retrieval candidates set to {state.top_k}.")
            continue
        if parsed == "error":
            print(value)
            continue
        command, _, argument = question.partition(" ")
        instruction, subject = "Answer completely and cite no invented sources.", question
        if command == "/continue" and state.question: subject, instruction = state.question, f"Continue only: {argument or 'missing theory and mechanism'}."
        elif command == "/focus" and state.question: subject, instruction = state.question, f"Focus only: {argument}."
        elif command == "/outline": subject, instruction = argument, "Create 3 to 5 research questions only."
        elif command == "/compare" and "|" in argument: subject, instruction = argument, "Compare definition, relation, difference, and common confusion."
        elif command == "/analyze": subject, instruction = argument, "Analyze central claim, concepts, argument, stance, and open questions."
        elif command.startswith("/"):
            print("Invalid command or missing argument."); continue
        vector = retriever.encode([subject], normalize_embeddings=True, show_progress_bar=False)[0].tolist()
        result = collection.query(query_embeddings=[vector], n_results=state.top_k, include=["documents", "metadatas", "distances"])
        state.sources = [{"rank": i, "document": d, "source": m.get("source", "unknown"), "type": m.get("type", "unknown"), "distance": float(distance)} for i, (d, m, distance) in enumerate(zip(result["documents"][0], result["metadatas"][0], result["distances"][0]), 1)]
        print(f"[ {len(select_sources(state.sources))} SOURCES ]\nMDLRH > ", end="")
        answer_options = {"cache_implementation": "offloaded", "max_new_tokens": 1536, "temperature": 0.7, "top_k": 60, "top_p": 0.95, "repetition_penalty": 1.15, "do_sample": True}
        if state.think:
            think_raw = generate(generator, messages(subject, state.sources, instruction), {"cache_implementation": "offloaded", "min_new_tokens": 48, "max_new_tokens": 160, "temperature": None, "top_k": None, "top_p": None, "do_sample": False})
            think = extract(think_raw, "think")
            print(f"<think>\n{think}\n</think>\n<answer>\n", end="")
            raw = generate(generator, messages(subject, state.sources, instruction, think), answer_options, on_chunk=lambda text: print(re.sub(r"</?(?:think|answer)>", "", text, flags=re.I), end="", flush=True))
        else:
            raw = generate(generator, [{"role": "system", "content": load_text(SYSTEM_PROMPT)}, {"role": "user", "content": f"Question: {subject}\n\n{instruction}\n\nSources:\n{context(state.sources)}"}], answer_options, on_chunk=lambda text: print(text, end="", flush=True))
        state.question, state.answer = subject, extract(raw, "answer")
        print("\n</answer>\n" + RULE)


if __name__ == "__main__":
    main()
