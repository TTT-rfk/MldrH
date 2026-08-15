# MldrH v1.1

MldrH is a local Marxist theory research terminal. It retrieves PT theory material on CPU with `BAAI/bge-m3 + Mdlr-theory-embed-v1` and generates locally with `Qwen2.5-3B-Instruct + Mdlr1.1-think` through Transformers and PEFT.

## v1.1 Changes

- Replaced Ollama/GGUF generation with local Transformers + PEFT CUDA BF16 inference.
- Added Mdlr1.1-think, two-stage Think/Answer generation, and CPU-offloaded KV cache.
- Added a terminal editor with normal cursor editing, history, mouse caret placement, Ctrl+C interruption, and `/clear` session clearing.
- Updated the database asset to 5089 PT-only records. Conversational SFT vectors are excluded.

## Included

- `MldrH.py` and `MldrH.bat`.
- `adapters/Mdlr1.1-think` generation LoRA adapter.
- `adapters/Mdlr-theory-embed-v1` retrieval LoRA adapter.
- Prompt files, setup script, configuration template, and agent-readable setup instructions.

## Not Included

- Qwen2.5-3B-Instruct or BAAI/bge-m3 base weights.
- Raw PT/SFT corpora or staged conversational SFT vectors.
- The database itself; download it as the matching v1.1 Release asset.
- Local paths, `config.json`, virtual environments, cache files, logs, credentials, tokens, and conversations.

## Quick Start

Run `setup_mldrh.ps1`, then run `MldrH.bat`. Read [INSTALL.md](INSTALL.md) for requirements and [AI_SETUP.md](AI_SETUP.md) for safe agent automation.

## License

Code is released under the MIT License. Adapter files retain their upstream and training-output terms.
