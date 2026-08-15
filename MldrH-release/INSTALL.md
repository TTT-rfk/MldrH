# Install MldrH v1.1 on Windows

## Requirements

- Windows 10 or later.
- Python 3.11 or later.
- A CUDA-capable GPU supporting BF16. Qwen2.5-3B BF16 requires about 8GB VRAM; CPU-offloaded KV cache reduces generation peak pressure but system memory is also required.
- Internet access to ModelScope for public base model downloads and GitHub for the v1.1 database asset.

## Automatic Setup

Open PowerShell in this directory and run:

```powershell
.\setup_mldrh.ps1
```

The script creates `.venv`, installs dependencies, downloads public base models, downloads the matching v1.1 PT-only database Release asset, writes `config.json`, and verifies the collection.

## Manual Setup

1. Create a Python environment and install requirements:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

2. Download public base models:

- Retrieval base: [BAAI/bge-m3](https://modelscope.cn/models/BAAI/bge-m3)
- Generation base: [Qwen/Qwen2.5-3B-Instruct](https://modelscope.cn/models/Qwen/Qwen2.5-3B-Instruct)

3. Download `MldrH-theory-knowledge-db-v1.1.0.zip` from the matching GitHub Release, extract it in this folder, and verify it contains `knowledge_db_theory_v1\chroma.sqlite3`.

4. Copy `config.example.json` to `config.json`. The default relative paths work when all assets remain in the release folder.

5. Launch:

```text
MldrH.bat
```

## Terminal Controls

- Enter: submit a question or slash command.
- Alt+Enter: insert a newline.
- Ctrl+C: stop current Think or Answer generation safely.
- Ctrl+L: clear current local session.
- Ctrl+T: toggle Think mode.
- `/clear`: clear local session and terminal display.

## Security

Never add credentials, raw source corpora, staged vectors, logs, or `config.json` to a public release.
