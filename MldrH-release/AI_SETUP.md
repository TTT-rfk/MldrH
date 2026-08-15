# Agent Setup Instructions for MldrH v1.1

Read this file before an agent configures MldrH.

## Safety Rules

1. Never read, print, copy, commit, or upload keys, tokens, passwords, browser credentials, private source corpora, staged vectors, logs, or conversations.
2. Never overwrite an existing `config.json` without the user explicitly approving the new paths.
3. Do not substitute another generation model, add Ollama, convert to GGUF, enable quantization, or change the PT-only database without user approval.
4. Run commands one at a time. Report actual failures and their output.

## Required Runtime

- Retrieval: public `BAAI/bge-m3` base + bundled `adapters/Mdlr-theory-embed-v1` on CPU.
- Generation: public `Qwen2.5-3B-Instruct` base + bundled `adapters/Mdlr1.1-think` with Transformers/PEFT on CUDA BF16.
- Database: v1.1 Release asset, collection `theory_knowledge`, 5089 records, metadata type `pt` only.

## Automatic Deployment

1. Inspect `config.json`. If it exists, ask before changing it.
2. Run `./setup_mldrh.ps1` in PowerShell.
3. Verify the script reports `collection=theory_knowledge`, `count=5089`, and `types=pt`.
4. Run `MldrH.bat`.
5. If startup fails, inspect only the displayed missing path or dependency. Do not search for private files or credentials.

## Manual Recovery

- Use Python 3.11 or later.
- Install `requirements.txt` into `.venv`.
- Download only the public model links listed in `INSTALL.md`.
- Keep the bundled adapters unchanged.
- Download only the v1.1 database Release asset; do not use the old v1.0.0 mixed database.

## Do Not Invent Assets

If public base models or the v1.1 database asset are unavailable, state the exact missing asset and stop. Do not substitute unrelated models or databases.
