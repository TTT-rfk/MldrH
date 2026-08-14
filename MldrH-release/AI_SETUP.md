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
- `adapter_path` points to the separately released Mdlr theory LoRA adapter.
- `database_path` points to a compatible Chroma collection named `theory_knowledge`.
- Ollama serves an Mdlr generation model imported from the official Mdlr model project.
- `.venv` contains the packages from `requirements.txt`.

## Required Steps

1. Read `INSTALL.md` and check every dependency path before editing any configuration.
2. Create `.venv` with Python 3.11 or newer and install `requirements.txt`.
3. Copy `config.example.json` to `config.json` only when it does not already exist.
4. Download the public BAAI/bge-m3 model from the link in `INSTALL.md`, then enter its full extracted folder path as `base_model`.
5. Obtain the separately released adapter, verify `adapter_model.safetensors` exists, then enter its full folder path as `adapter_path`.
6. Download the Mdlr GGUF from https://github.com/TTT-rfk/Mdlr1.0-Qwen2.5-3B using its ModelScope link. Use that repository's `Modelfile` with `ollama create`, then set `generation_model` to the exact `ollama list` tag.
7. Obtain the compatible vector database linked from the Mdlr model repository, verify `chroma.sqlite3` exists, then set `database_path` and `collection_name`.
8. Run `MldrH.bat` and resolve only the displayed error code.

## Do Not Invent Missing Assets

If the Mdlr generation model or knowledge base is not available, state that MldrH cannot perform full RAG until the user supplies it. Do not substitute unrelated models or download unverified files.
