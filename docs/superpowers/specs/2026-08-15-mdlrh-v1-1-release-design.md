# MldrH v1.1 Release Design

## Release Goal

Publish MldrH v1.1 as an additive update to `TTT-rfk/MldrH`. Preserve repository history and the existing v1.0.0 Release. Replace the default release package with the current local Transformers/PEFT terminal system.

## Public Package

The v1.1 release package includes:

- Portable MldrH terminal using Transformers, PyTorch CUDA BF16, PEFT, and prompt_toolkit.
- `Mdlr1.1-think` generation LoRA adapter.
- `Mdlr-theory-embed-v1` retrieval LoRA adapter.
- System prompt, Think system prompt, and Think expansion prompt.
- Windows launcher and automated PowerShell setup script.
- Installation instructions, agent-readable setup instructions, requirements, release hash manifest, and configuration template.

The v1.1 database Release asset includes:

- `knowledge_db_theory_v1` collection `theory_knowledge`.
- 5089 records with metadata type `pt` only.

## Exclusions

Do not publish:

- Qwen2.5-3B-Instruct base weights.
- BAAI/bge-m3 base weights.
- Raw PT or SFT source corpora.
- The staged 570 conversational SFT vectors.
- Local absolute paths, config.json, virtual environments, cache files, logs, API keys, tokens, passwords, or chat history.

## Runtime

- Retrieval: BAAI/bge-m3 plus bundled `Mdlr-theory-embed-v1` adapter on CPU.
- Generation: user-downloaded Qwen2.5-3B-Instruct plus bundled `Mdlr1.1-think` adapter on CUDA BF16.
- Generation uses CPU-offloaded KV cache and requires a CUDA-capable GPU.
- Think mode is default-on, uses two local generation stages, and has a command to disable it.

## Automated Agent Setup

`AI_SETUP.md` directs agents to:

1. Inspect current files and never overwrite user `config.json` without confirmation.
2. Create a Python virtual environment and install requirements.
3. Download only public base models using specified ModelScope links.
4. Download the matching v1.1 database asset and verify its SHA-256, collection name, record count, and `pt`-only metadata.
5. Write local paths to config.json.
6. Run the terminal verification command.

## Release Process

- Build local ZIP assets and verify their contents and SHA-256.
- Commit only the portable release source, adapters, docs, and asset manifest.
- Push as an update to the existing repository without force-push or history rewriting.
- Publish a new `v1.1.0` GitHub Release; retain v1.0.0 unchanged.
