# -*- coding: utf-8 -*-
"""Portable MldrH local theory research terminal."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import chromadb
import requests
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
PROMPT_PATH = ROOT / "system_prompt.txt"
RULE = "-" * 56
OPTIONS = {"num_gpu": -1, "num_ctx": 8192, "num_predict": 2048, "temperature": 0.7, "top_k": 60, "top_p": 0.95, "repeat_penalty": 1.15, "repeat_last_n": 128}


@dataclass
class State:
    model: str
    top_k: int = 8
    count: int = 0
    sources: list[dict] = field(default_factory=list)
    question: str = ""
    answer: str = ""


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise RuntimeError("E03 Missing config.json. Copy config.example.json to config.json and fill every empty field.")
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    missing = [key for key in ("base_model", "adapter_path", "database_path", "generation_model") if not str(config.get(key, "")).strip()]
    if missing:
        raise RuntimeError("E03 Fill config.json fields: " + ", ".join(missing))
    return config


def prompt() -> str:
    text = PROMPT_PATH.read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError("E03 system_prompt.txt is empty.")
    return text


def help_screen() -> None:
    print("COMMANDS")
    print("  /sources              查看本轮检索到的理论资料")
    print("  /continue [重点]       接着展开上一回答")
    print("  /suggest               查看 3 个可继续追问的方向")
    print("  /focus [要求]          基于上一问题重新回答，并聚焦指定角度")
    print("  /outline [主题]        生成可逐项提问的研究或写作提纲")
    print("  /compare A | B         比较两个概念、理论或观点")
    print("  /analyze [文本]        分析文本的概念、论证、立场与问题")
    print("  /status                查看模型、知识库和生成参数")
    print("  /help                  查看全部命令")
    print("  /exit                  退出 MldrH")
    print("ADVANCED")
    print("  /top N                 设置候选检索数量，范围 1-32")
    print("  /clear                 清除本次对话的资料记录")


def select_sources(rows: list[dict]) -> list[dict]:
    selected, seen = [], set()
    for row in rows:
        if row["source"] not in seen:
            selected.append(row); seen.add(row["source"])
        if len(selected) == 4:
            break
    return selected


def messages(question: str, rows: list[dict], instruction: str) -> list[dict]:
    rows = select_sources(rows)
    context = "\n\n".join(f"【资料{row['rank']}】{row['document'][:1200]}" for row in rows)
    return [{"role": "system", "content": prompt()}, {"role": "user", "content": f"问题：{question}\n\n参考资料：\n{context}\n\n{instruction}"}]


def clean(text: str) -> str:
    residue = re.compile(r"^(?:【注\d+】|【第\d+(?:节|部分)】|【正文】)\s*$")
    return "\n".join(line for line in text.splitlines() if not residue.fullmatch(line)).strip()


def main() -> None:
    try:
        cfg = load_config(); base = Path(cfg["base_model"]); adapter = Path(cfg["adapter_path"]); db = Path(cfg["database_path"])
        required = [base / "pytorch_model.bin", adapter / "adapter_model.safetensors", db / "chroma.sqlite3"]
        missing = [str(path) for path in required if not path.exists()]
        if missing: raise RuntimeError("E03 Missing required asset:\n" + "\n".join(missing))
        tags = requests.get(cfg["ollama_url"].rstrip("/") + "/api/tags", timeout=10); tags.raise_for_status()
        if cfg["generation_model"] not in {item["name"] for item in tags.json().get("models", [])}: raise RuntimeError("E02 Configured Ollama model is unavailable.")
        retriever = SentenceTransformer(str(base), device="cpu", trust_remote_code=True); retriever.load_adapter(str(adapter))
        collection = chromadb.PersistentClient(path=str(db)).get_collection(cfg.get("collection_name", "theory_knowledge"))
    except Exception as error:
        print(f"MldrH could not start: {error}"); raise SystemExit(1)
    state = State(model=cfg["generation_model"], count=collection.count())
    print("\033[2J\033[H", end=""); print("MldrH / THEORY WORKBENCH\nLocal Marxist Theory Research Terminal\n" + RULE); print("复杂议题建议分步骤提问。\n"); help_screen(); print(RULE)
    while True:
        question = input("YOU > ").strip()
        if question.lower() in {"/exit", "exit", "quit"}: break
        if not question: continue
        if question == "/help": help_screen(); continue
        if question == "/suggest":
            print("FOLLOW-UP DIRECTIONS\n  1. 进一步解释其中的作用机制。\n  2. 比较它与相关概念或相反观点的区别。\n  3. 要求给出理论依据和具体例证。"); continue
        if question == "/sources":
            print("\n".join(f"{x['rank']}. {x['source']} [{x['type']}] 距离 {x['distance']:.4f}" for x in state.sources) or "上一轮还没有检索结果。"); continue
        if question == "/status":
            print(f"MldrH STATUS\n  模型：{state.model}\n  候选资料：{state.top_k} 条\n  生成资料：最多 4 个不同来源\n  知识库：{state.count} 条"); continue
        if question == "/clear":
            state.sources.clear(); state.question = ""; state.answer = ""; print("已清除本次对话的资料记录。"); continue
        command, _, argument = question.partition(" ")
        if command == "/top":
            if argument.isdigit() and 1 <= int(argument) <= 32:
                state.top_k = int(argument); print(f"检索条数已设为：{state.top_k}")
            else:
                print("用法：/top N，N 必须是 1 到 32 的整数。")
            continue
        instruction = "请完整、分层地回答问题，使用自然段展开，不要逐字复述资料或编造出处。"
        subject = question
        if command == "/outline": subject = argument; instruction = "生成 3 到 5 个可逐项提问的研究或写作问题。不写正文、引文、页码、资料列表或虚构出处。"
        elif command == "/compare" and len(argument.split("|")) == 2: subject = argument; instruction = "比较两者的定义、关系、区别和常见混淆；不要虚构具体出处。"
        elif command == "/analyze": subject = argument; instruction = "分析文本的中心主张、核心概念、论证链、理论立场和开放问题；不要假定作者或事实真实性。"
        elif command == "/focus" and state.question: subject = state.question; instruction = f"只聚焦以下角度：{argument}。不要复述其他部分。"
        elif command == "/continue" and state.question: subject = state.question; instruction = f"只补充以下方向：{argument or '补充遗漏的理论依据、机制、区别或例证'}。不要重复已有内容。"
        elif command.startswith("/"):
            print("命令无效或缺少参数。输入 /help 查看用途和示例。"); continue
        if not subject.strip(): print("命令缺少内容。输入 /help 查看示例。"); continue
        try:
            print("[ RETRIEVING ] Searching theory sources")
            vector = retriever.encode([subject], normalize_embeddings=True, show_progress_bar=False)[0].tolist()
            result = collection.query(query_embeddings=[vector], n_results=state.top_k, include=["documents", "metadatas", "distances"])
            state.sources = [{"rank": i, "document": d, "source": m.get("source", "未知来源"), "type": m.get("type", "未知类型"), "distance": float(x)} for i, (d, m, x) in enumerate(zip(result["documents"][0], result["metadatas"][0], result["distances"][0]), 1)]
            print(f"[ {len(select_sources(state.sources))} SOURCES ] Selected distinct sources for generation\n\nMDLRH > ", end="", flush=True)
            response = requests.post(cfg["ollama_url"].rstrip("/") + "/api/chat", json={"model": state.model, "messages": messages(subject, state.sources, instruction), "stream": True, "options": OPTIONS}, timeout=600, stream=True); response.raise_for_status()
            chunks = []
            for line in response.iter_lines():
                if not line: continue
                data = json.loads(line)
                if data.get("done"): break
                text = (data.get("message") or {}).get("content", ""); chunks.append(text); print(text, end="", flush=True)
            state.question, state.answer = subject, clean("".join(chunks)); print(f"\n{RULE}\n[ NEXT ] /suggest for follow-up directions · /continue [重点] to expand\n")
        except Exception as error: print(f"E04 Generation request failed: {error}")


if __name__ == "__main__":
    main()
