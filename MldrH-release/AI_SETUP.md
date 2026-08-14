# AI Setup Instructions

Use this document when giving the extracted `MldrH-release` folder to another coding agent.

## Safety Rules

1. Do not search for, copy, print, commit, upload, or request API keys, tokens, passwords, browser credentials, private source corpora, or chat logs.
2. Do not download or redistribute private model weights or private vector databases.
3. Do not overwrite `config.json` if it already exists; ask the user before changing local paths or model names.
4. Run commands one at a time and show actual failures rather than claiming success.

## Setup Goal

Configure MldrH so that:

- `base_model` points to the public BAAI/bge-m3 base model.
- `adapter_path` points to the bundled Mdlr theory LoRA adapter.
- `database_path` points to the downloaded `v1.0.0` Chroma collection named `theory_knowledge`.
- Ollama serves an Mdlr generation model imported from the official Mdlr model project.
- `.venv` contains the packages from `requirements.txt`.

## Required Steps

1. Read `INSTALL.md` and check every dependency path before editing any configuration.
2. Create `.venv` with Python 3.11 or newer and install `requirements.txt`.
3. Copy `config.example.json` to `config.json` only when it does not already exist.
4. Download the public BAAI/bge-m3 model from the link in `INSTALL.md`, then enter its full extracted folder path as `base_model`.
5. Verify the bundled `adapter\adapter_model.safetensors` file exists.
6. Download the Mdlr GGUF from https://github.com/TTT-rfk/Mdlr1.0-Qwen2.5-3B using its ModelScope link. Use that repository's `Modelfile` with `ollama create`, then set `generation_model` to the exact `ollama list` tag.
7. Run `setup_mldrh.ps1`. It downloads the verified `v1.0.0` theory database Release asset, writes `config.json`, and verifies `theory_knowledge` has 5659 entries.
8. Run `MldrH.bat` and resolve only the displayed error code.

## Do Not Invent Missing Assets

If the Mdlr generation model or knowledge base is not available, state that MldrH cannot perform full RAG until the user supplies it. Do not substitute unrelated models or download unverified files.
