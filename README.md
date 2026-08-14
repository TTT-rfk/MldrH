# MldrH

**MldrH** is a local Marxist theory research terminal designed for the Mdlr model family and Ollama. It combines CPU retrieval with GPU generation, keeps theory materials inspectable, and provides a restrained command-line workbench for direct questions, comparison, text analysis, focused re-answers, and research outlines.

> Complex topics are more stable when asked step by step.

## What It Does

- Runs locally on Windows with Ollama generation and CPU retrieval.
- Retrieves theory materials through `BAAI/bge-m3` plus an Mdlr theory embedding adapter.
- Streams answers directly in the terminal.
- Keeps retrieval transparent with `/sources`.
- Avoids sending repeated chunks from the same source file into generation context.
- Includes practical commands for new and experienced users without forcing a guided workflow.

## Commands

| Command | Purpose |
|---|---|
| `/sources` | View theory materials retrieved for the previous answer. |
| `/continue [focus]` | Expand the previous answer in a specified direction. |
| `/suggest` | Show three follow-up question directions without calling the model. |
| `/focus [focus]` | Re-answer the previous question while focusing on one angle. |
| `/outline [topic]` | Generate a question-shaped research or writing outline. |
| `/compare A | B` | Compare two concepts, theories, or views. |
| `/analyze [text]` | Analyze a text's concepts, argument, stance, and open questions. |
| `/status` | Show active model, retrieval, and generation status. |
| `/help` | Show all terminal commands. |

## Download And Setup

The portable source release is in [`MldrH-release/`](MldrH-release/).

1. Read [INSTALL.md](MldrH-release/INSTALL.md).
2. Install Python and Ollama from their official sources.
3. Create a Python virtual environment and install `requirements.txt`.
4. Copy `config.example.json` to `config.json`.
5. Fill your own local paths for the embedding base model, adapter, compatible Chroma knowledge base, Ollama URL, and Mdlr generation model tag.
6. Launch `MldrH.bat`.

For coding agents or AI-assisted setup, read [AI_SETUP.md](MldrH-release/AI_SETUP.md).

## Required Assets

MldrH is intentionally a source and configuration release. It does **not** include local model weights, the embedding adapter binary, a knowledge base, training data, or private materials.

You need to obtain and configure:

- Public embedding base model: [BAAI/bge-m3 on Hugging Face](https://huggingface.co/BAAI/bge-m3) or [ModelScope](https://modelscope.cn/models/BAAI/bge-m3).
- A separately distributed Mdlr Ollama generation model.
- A separately distributed Mdlr theory embedding adapter.
- A lawful compatible Chroma knowledge base with the configured collection name.

This separation keeps the repository small, reproducible, and free of private corpus material.

## Privacy And Safety

- MldrH is designed to run locally.
- Never put API keys, tokens, passwords, private documents, chat logs, model weights, or knowledge databases into this public repository.
- The terminal uses retrieved materials as evidence for source-specific details; it may reason beyond excerpts but should not invent citations, page numbers, titles, authors, or quotations.

## Current Scope

- Windows-focused console terminal.
- Local Ollama server at a user-configured URL.
- CPU embedding retrieval and GPU Ollama generation.
- No web UI, telemetry, account system, cloud API, or automatic model downloader.

## License

The MldrH code is released under the [MIT License](MldrH-release/LICENSE). Model and adapter assets retain their own applicable terms.
