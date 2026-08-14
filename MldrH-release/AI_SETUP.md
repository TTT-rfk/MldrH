# AI Setup Instructions

Use this document when giving the extracted `MldrH-release` folder to another coding agent.

## Safety Rules

1. Do not search for, copy, print, commit, upload, or request API keys, tokens, passwords, browser credentials, private source corpora, or chat logs.
2. Do not download or redistribute private model weights or private vector databases.
3. Do not overwrite `config.json` if it already exists; ask the user before changing local paths or model names.
4. Run commands one at a time and show actual failures rather than claiming success.

## Setup Goal

Configure MldrH so that:

- `models/BAAI-bge-m3` contains the public BAAI/bge-m3 base model.
- `models/Mdlr-theory-embed-v1` contains the supplied LoRA adapter.
- `knowledge_db_theory_v1` contains a compatible Chroma collection named `theory_knowledge`.
- Ollama serves the separately obtained Mdlr generation model.
- `.venv` contains the packages from `requirements.txt`.

## Required Steps

1. Read `INSTALL.md` and check every dependency path before editing any configuration.
2. Create `.venv` with Python 3.11 or newer and install `requirements.txt`.
3. Copy `config.example.json` to `config.json` only when it does not already exist.
4. Download the public BAAI/bge-m3 model from the link in `INSTALL.md` into `models/BAAI-bge-m3`.
5. Obtain the separately released adapter and place it in `models/Mdlr-theory-embed-v1`.
6. Ask the user to provide or build a lawful compatible Chroma knowledge base. MldrH cannot retrieve without it.
7. Install Ollama from its official website and ask the user to import or pull the separately distributed Mdlr generation model.
8. Run `MldrH.bat` and resolve only the displayed error code.

## Do Not Invent Missing Assets

If the Mdlr generation model or knowledge base is not available, state that MldrH cannot perform full RAG until the user supplies it. Do not substitute unrelated models or download unverified files.
