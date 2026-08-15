# MldrH v1.1.0 Complete Configuration and Release Guide

This document is the single release and configuration reference for MldrH v1.1.0.

## 1. What v1.1.0 Contains

MldrH v1.1.0 is a local Marxist theory research terminal.

- Retrieval runtime: `BAAI/bge-m3` plus `Mdlr-theory-embed-v1` adapter on CPU.
- Generation runtime: `Qwen2.5-3B-Instruct` plus `Mdlr1.1-think` adapter through Transformers and PEFT on CUDA BF16.
- Database: Chroma collection `theory_knowledge`, exactly 5089 entries, all metadata type `pt`.
- Think mode: enabled by default; it generates an internal three-item reasoning summary, then an answer.

v1.1.0 does not use Ollama, GGUF, 4-bit quantization, 8-bit quantization, or bitsandbytes.

## 2. GitHub Release Upload

Release page:

```text
https://github.com/TTT-rfk/MldrH/releases/edit/v1.1.0
```

Keep the existing v1.0.0 Release unchanged. Do not delete it and do not replace its assets.

For v1.1.0, attach these three assets:

| Asset | Local path | Purpose |
|---|---|---|
| `MldrH-release-v1.1.0.zip` | Release build output directory | Complete terminal package with both adapters. |
| `MldrH-theory-knowledge-db-v1.1.0.zip` | Release build output directory | PT-only Chroma knowledge database. |
| `SHA256SUMS-v1.1.0.txt` | Release build output directory | Asset and adapter checksums. |

The first file is about 234MB because it includes the `Mdlr1.1-think` LoRA adapter. This is valid for a GitHub Release asset. GitHub's 100MB limit applies to individual files sent through normal Git push, not Release assets.

Use this Release title:

```text
MldrH v1.1.0
```

Use tag:

```text
v1.1.0
```

Use this Release description:

```markdown
## MldrH v1.1.0

- Transformers + PEFT local CUDA BF16 generation with Mdlr1.1-think.
- CPU retrieval using BAAI/bge-m3 + Mdlr-theory-embed-v1.
- PT-only theory knowledge database: 5,089 entries in `theory_knowledge`.
- Think/Answer terminal workflow, editable prompt input, Ctrl+C interruption, and automated setup.

### Assets

- `MldrH-release-v1.1.0.zip`: terminal sources, both adapters, prompts, installer, and docs.
- `MldrH-theory-knowledge-db-v1.1.0.zip`: PT-only Chroma database.
- `SHA256SUMS-v1.1.0.txt`: SHA-256 verification manifest.

Base model weights and raw training data are not included.
```

After uploading assets, click **Update release**. If a file with the same name already appears, do not upload a duplicate. Keep one copy of each asset only.

## 3. Package Layout After Extraction

Extract `MldrH-release-v1.1.0.zip`. The folder should contain:

```text
MldrH-release/
  MldrH.py
  MldrH.bat
  setup_mldrh.ps1
  requirements.txt
  config.example.json
  system_prompt.txt
  think_system_prompt.txt
  think_expansion_prompt.txt
  adapters/
    Mdlr1.1-think/
    Mdlr-theory-embed-v1/
  README.md
  INSTALL.md
  AI_SETUP.md
  RELEASE-ASSETS.md
```

It intentionally does not contain base-model weights, a database, raw corpus files, user configuration, API keys, tokens, conversations, logs, staged SFT vectors, or local absolute paths.

## 4. Runtime Requirements

- Windows 10 or later.
- Python 3.11 or later.
- NVIDIA CUDA GPU with BF16 support.
- Approximately 8GB VRAM or more for Qwen2.5-3B BF16 generation.
- System memory for CPU-offloaded KV cache.
- Internet access to ModelScope and GitHub Releases during initial setup.

Public base models are downloaded separately and are not redistributed:

- Retrieval base: https://modelscope.cn/models/BAAI/bge-m3
- Generation base: https://modelscope.cn/models/Qwen/Qwen2.5-3B-Instruct

## 5. Automatic Installation

In PowerShell, inside the extracted `MldrH-release` folder:

```powershell
.\setup_mldrh.ps1
```

The setup script:

1. Creates `.venv`.
2. Installs `requirements.txt`.
3. Downloads `BAAI/bge-m3` to `assets\BAAI-bge-m3` when missing.
4. Downloads `Qwen2.5-3B-Instruct` to `assets\Qwen2.5-3B-Instruct` when missing.
5. Downloads and extracts the matching `MldrH-theory-knowledge-db-v1.1.0.zip` Release asset when missing.
6. Creates `config.json` only if it does not already exist.
7. Verifies collection `theory_knowledge`, count `5089`, and metadata type `pt` only.

Launch after setup:

```text
MldrH.bat
```

## 6. config.json Reference

Copy `config.example.json` to `config.json` only when automatic setup has not already created it.

Default portable configuration:

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

Relative paths are resolved from the MldrH release folder. Absolute paths are also supported.

| Setting | Required value |
|---|---|
| `embedding_base_model` | Folder containing `BAAI/bge-m3` files. Must include `pytorch_model.bin`. |
| `generation_base_model` | Folder containing `Qwen2.5-3B-Instruct`. Must include `config.json`. |
| `retrieval_adapter` | Bundled `adapters\Mdlr-theory-embed-v1` folder. Must include `adapter_model.safetensors`. |
| `think_adapter` | Bundled `adapters\Mdlr1.1-think` folder. Must include `adapter_model.safetensors`. |
| `database_path` | Extracted `knowledge_db_theory_v1` folder. Must include `chroma.sqlite3`. |
| `collection_name` | Exactly `theory_knowledge`. |

Do not change adapters, database type, collection name, or model architecture unless deliberately retraining and rebuilding the whole release.

## 7. Terminal Behavior and Controls

Generation has two stages when Think mode is enabled:

1. Think stage: greedy generation, 48 to 160 new tokens, exactly three concise `·` bullet points.
2. Answer stage: streaming answer generation, up to 1536 new tokens, temperature 0.7, top-k 60, top-p 0.95.

Both stages use CPU-offloaded KV cache. Model weights and adapters remain on GPU in BF16.

| Control | Action |
|---|---|
| Enter | Submit question or command. |
| Alt+Enter | Insert newline. |
| Ctrl+C | Safely stop current Think or Answer generation. |
| Ctrl+L | Clear session and terminal display. |
| Ctrl+T | Toggle Think mode. |
| `/think` | Toggle Think mode. |
| `/think on` | Enable Think mode. |
| `/think off` | Disable Think mode. |
| `/sources` | Display retrieved theory sources. |
| `/suggest` | Display follow-up directions. |
| `/top N` | Set retrieval candidate count from 1 to 32. |
| `/continue [focus]` | Continue the previous question in a selected direction. |
| `/focus [focus]` | Re-answer previous question with a selected focus. |
| `/outline [topic]` | Create research questions. |
| `/compare A | B` | Compare two concepts. |
| `/analyze [text]` | Analyze a text. |
| `/status` | Show runtime and database status. |
| `/clear` | Clear local session. |
| `/help` | Show commands. |
| `/exit` | Exit MldrH. |

## 8. Integrity Verification

Download `SHA256SUMS-v1.1.0.txt` with both ZIP files. In PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 .\MldrH-release-v1.1.0.zip
Get-FileHash -Algorithm SHA256 .\MldrH-theory-knowledge-db-v1.1.0.zip
```

Expected values:

```text
09F70C5CCC3B2C7B72307A2132CF5CBB2336C0203C45B1B2795BD98E68E48E5B  MldrH-release-v1.1.0.zip
04521821BEA890874FC03E755BA22B889F47A478F055A0CB346CB02F082A54BA  MldrH-theory-knowledge-db-v1.1.0.zip
9961C4F914A36ADA9AA3CC090C23845A1BAD8FD45833C741F84A266B1D4065E0  adapters/Mdlr1.1-think/adapter_model.safetensors
F10536BEA1E3026CB4D22D5BB0678B706718AAF10D7575F83D21B7968DC7836F  adapters/Mdlr-theory-embed-v1/adapter_model.safetensors
```

## 9. What Must Not Be Published

Never upload or commit:

- Qwen or BGE base model weights.
- Raw PT corpus, raw SFT corpus, training JSONL, or chat records.
- Staged 570 conversational SFT vectors.
- `config.json` containing a person's local paths.
- `.venv`, `assets`, `knowledge_db_theory_v1` inside the terminal source repository.
- API keys, GitHub tokens, passwords, cookies, credentials, logs, cache files, or private archives.

The allowed published database is only `MldrH-theory-knowledge-db-v1.1.0.zip`, whose collection contains 5089 PT records only.

## 10. Release Verification Checklist

Before announcing the Release, check:

- GitHub main branch includes commit `65c4333`.
- Tag `v1.1.0` exists.
- v1.0.0 still exists and is unchanged.
- v1.1.0 has exactly these assets: terminal ZIP, PT-only database ZIP, checksum manifest.
- Terminal ZIP includes both adapters and does not include base weights or `config.json`.
- Database ZIP extracts to `knowledge_db_theory_v1`.
- `theory_knowledge` has 5089 records, each with metadata type `pt`.
- Release checksums match `SHA256SUMS-v1.1.0.txt`.

## 11. Troubleshooting

### CUDA GPU is required for BF16 generation

MldrH v1.1 uses Qwen2.5-3B in CUDA BF16. Install a compatible NVIDIA driver and run it on a BF16-capable CUDA GPU. Do not silently replace this runtime with Ollama, GGUF, quantization, or another model.

### Missing asset error

Check the exact path displayed by MldrH. Required files are:

```text
assets\BAAI-bge-m3\pytorch_model.bin
assets\Qwen2.5-3B-Instruct\config.json
adapters\Mdlr-theory-embed-v1\adapter_model.safetensors
adapters\Mdlr1.1-think\adapter_model.safetensors
knowledge_db_theory_v1\chroma.sqlite3
```

### Database validation fails

Use only the v1.1.0 database asset. It must contain `theory_knowledge` with 5089 PT-only records. Do not substitute the older v1.0.0 mixed database.

### GitHub Release upload fails

The terminal ZIP is a valid Release asset even though it is above 100MB. Do not try to `git push` the ZIP. Upload it through the GitHub Release editor. If the browser upload fails, retry after network recovery; do not create another Release or duplicate assets.
