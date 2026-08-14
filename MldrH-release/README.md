# MldrH

MldrH is a local Marxist theory research terminal for the `Mdlr1.0-Qwen2.5-3B` Ollama model. It retrieves theory materials on CPU with the `Mdlr-theory-embed-v1` LoRA adapter and generates answers with Ollama on GPU.

## What Is Included

- MldrH Windows terminal and launcher.
- The system prompt and a portable configuration template.
- The verified `Mdlr-theory-embed-v1` LoRA adapter and runtime files.
- Installation, configuration, troubleshooting, and AI-assisted setup instructions.

## What Is Not Included

The repository intentionally does not distribute:

- Mdlr generation-model weights.
- BAAI/bge-m3 base-model weights.
- The private theory vector database or its source corpus.
- The Chroma database binary files. They are distributed as the `v1.0.0` GitHub Release asset.
- Training data, build logs, cache files, API keys, tokens, passwords, or user conversations.

You must obtain the public model dependencies and prepare a compatible knowledge base before MldrH can answer with retrieval.

## Quick Start

Read [INSTALL.md](INSTALL.md) from top to bottom. After placing the public BGE-M3 base model and importing the Mdlr Ollama model, run `setup_mldrh.ps1`, then launch `MldrH.bat`.

## Main Commands

| Command | Purpose |
|---|---|
| `/sources` | View the theory materials retrieved for the previous answer. |
| `/continue [focus]` | Expand the previous answer in a specified direction. |
| `/suggest` | Show three follow-up question directions without calling the model. |
| `/focus [focus]` | Re-answer the previous question while focusing on one angle. |
| `/outline [topic]` | Generate a question-shaped research or writing outline. |
| `/compare A | B` | Compare two concepts, theories, or views. |
| `/analyze [text]` | Analyze a text's concepts, argument, stance, and open questions. |
| `/status` | Show active model, retrieval, and generation status. |
| `/help` | Show all available commands. |

## License

Code in this repository is released under the MIT License. Model and adapter files retain their respective upstream or training-output terms.
