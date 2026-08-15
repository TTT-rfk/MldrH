# MldrH v1.1

**MldrH** is a local Marxist theory research terminal for Windows. It retrieves PT theory material with `BAAI/bge-m3 + Mdlr-theory-embed-v1` on CPU and generates locally with `Qwen2.5-3B-Instruct + Mdlr1.1-think` through Transformers and PEFT on CUDA BF16.

It does **not** use Ollama, GGUF, bitsandbytes, 4-bit quantization, or 8-bit quantization.

> Complex topics are more stable when asked step by step.

## v1.1 Highlights

- Local Transformers + PEFT generation with the bundled `Mdlr1.1-think` LoRA adapter.
- Two-stage Think/Answer workflow: a concise three-item reasoning summary, then a streaming answer.
- CPU retrieval using `BAAI/bge-m3 + Mdlr-theory-embed-v1`.
- PT-only Chroma knowledge base: collection `theory_knowledge`, 5089 records, metadata type `pt` only.
- CPU-offloaded KV cache to reduce peak GPU-memory pressure during generation.
- Editable terminal input with history and mouse caret placement.
- Ctrl+C safe generation interruption, Ctrl+L session clear, Ctrl+T Think toggle, and slash commands.
- Automated Windows setup script for public base models and the matching v1.1 database asset.

## Download

Download the matching assets from the [v1.1.0 Release](https://github.com/TTT-rfk/MldrH/releases/tag/v1.1.0):

- `MldrH-release-v1.1.0.zip`: terminal, both adapters, prompts, installer, and documentation.
- `MldrH-theory-knowledge-db-v1.1.0.zip`: PT-only Chroma database.
- `SHA256SUMS-v1.1.0.txt`: SHA-256 verification manifest.

The terminal ZIP includes both adapters but intentionally excludes public base-model weights, raw corpora, private materials, local configuration, logs, and credentials.

## Quick Start

1. Extract `MldrH-release-v1.1.0.zip`.
2. Open PowerShell in the extracted `MldrH-release` folder.
3. Run:

```powershell
.\setup_mldrh.ps1
```

4. Launch:

```text
MldrH.bat
```

The installer creates `.venv`, downloads public base models from ModelScope when needed, downloads the matching v1.1 database asset, writes `config.json` only when it is missing, and verifies the PT-only collection.

## Runtime Requirements

- Windows 10 or later.
- Python 3.11 or later.
- NVIDIA CUDA GPU with BF16 support. Qwen2.5-3B BF16 typically requires about 8GB VRAM.
- Internet access for the first-time public model and database download.

Public base models:

- Retrieval: [BAAI/bge-m3 on ModelScope](https://modelscope.cn/models/BAAI/bge-m3)
- Generation: [Qwen/Qwen2.5-3B-Instruct on ModelScope](https://modelscope.cn/models/Qwen/Qwen2.5-3B-Instruct)

## Commands

| Command | Purpose |
|---|---|
| `/sources` | Show theory sources retrieved for the previous answer. |
| `/continue [focus]` | Continue the previous question in a selected direction. |
| `/suggest` | Show follow-up directions without calling the model. |
| `/focus [focus]` | Re-answer the previous question with a selected focus. |
| `/outline [topic]` | Generate research questions. |
| `/compare A | B` | Compare two concepts, theories, or views. |
| `/analyze [text]` | Analyze a text's concepts, argument, stance, and open questions. |
| `/think [on|off]` | Toggle Think mode. Think mode is enabled by default. |
| `/top N` | Set retrieval candidates from 1 to 32. |
| `/status` | Show retrieval, generation, Think, and database status. |
| `/clear` | Clear the local session and terminal display. |
| `/help` | Show all terminal commands. |
| `/exit` | Exit MldrH. |

Terminal shortcuts:

- Enter: submit.
- Alt+Enter: newline.
- Ctrl+C: stop current generation safely.
- Ctrl+L: clear session.
- Ctrl+T: toggle Think mode.

## Configuration

The default `config.example.json` uses paths relative to the release folder:

```json
{
  "embedding_base_model": "assets\\BAAI-bge-m3",
  "generation_base_model": "assets\\Qwen2.5-3B-Instruct",
  "retrieval_adapter": "adapters\\Mdlr-theory-embed-v1",
  "think_adapter": "adapters\\Mdlr1.1-think",
  "database_path": "knowledge_db_theory_v1",
  "collection_name": "theory_knowledge"
}
```

See [INSTALL.md](MldrH-release/INSTALL.md) for standard installation, [AI_SETUP.md](MldrH-release/AI_SETUP.md) for agent-safe setup, and [MANUAL_RELEASE_GUIDE.md](MldrH-release/MANUAL_RELEASE_GUIDE.md) for complete release, configuration, verification, and troubleshooting instructions.

## Privacy and Safety

- MldrH runs locally.
- Do not commit or publish API keys, tokens, passwords, browser credentials, local `config.json`, logs, chat records, raw source corpus files, staged vectors, or private archives.
- Do not publish base-model weights through this repository or its Release assets.
- The published v1.1 database is limited to the 5089 PT-only records in `theory_knowledge`.

## License

The MldrH code is released under the [MIT License](MldrH-release/LICENSE). Base models and adapter assets retain their own applicable terms.
