# Install MldrH on Windows

## 1. Prerequisites

Install these official dependencies first:

- Python 3.11 or newer: https://www.python.org/downloads/windows/
- Ollama for Windows: https://ollama.com/download/windows
- Git for Windows, optional but recommended: https://git-scm.com/download/win

Open PowerShell in the extracted MldrH folder after installation.

## 2. Create the Python Environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `py -3.11` is unavailable, replace it with the full path to a Python 3.11+ executable.

## 3. Configure Paths

Copy the template once:

```powershell
Copy-Item config.example.json config.json
```

Open `config.json` and fill every empty string. This release intentionally contains no machine-specific path, model, adapter, or knowledge-base asset.

| Field | What to enter | How to verify |
|---|---|---|
| `base_model` | Full folder path containing the downloaded `BAAI/bge-m3` files. | The folder contains `pytorch_model.bin`. |
| `adapter_path` | Full folder path containing the separately released Mldr theory adapter. | The folder contains `adapter_model.safetensors`. |
| `database_path` | Full folder path of your compatible Chroma database. | The folder contains `chroma.sqlite3`. |
| `collection_name` | Chroma collection name. | Default is `theory_knowledge`. Change only if your database uses another name. |
| `ollama_url` | Usually `http://localhost:11434`. | Open `http://localhost:11434/api/tags` after starting Ollama. |
| `generation_model` | The exact tag shown by `ollama list`. | Example only: `Mdlr1.0-Qwen2.5-3B:f16`. |

Example only. Do not copy these paths unless they exist on your computer:

```json
{
  "base_model": "D:\\Models\\BAAI-bge-m3",
  "adapter_path": "D:\\Models\\Mdlr-theory-embed-v1",
  "database_path": "D:\\Data\\knowledge_db_theory_v1",
  "collection_name": "theory_knowledge",
  "ollama_url": "http://localhost:11434",
  "generation_model": "Mdlr1.0-Qwen2.5-3B:f16"
}
```

## 4. Download the Public Embedding Base Model

Download `BAAI/bge-m3` from one of these public sources, extract it anywhere on your computer, then set that folder as `base_model` in `config.json`.

Links:

- Hugging Face: https://huggingface.co/BAAI/bge-m3
- ModelScope: https://modelscope.cn/models/BAAI/bge-m3

Do not place the base model inside the adapter folder.

## 5. Install the Mdlr Generation Model

Download the Mdlr model from [TTT-rfk/Mdlr1.0-Qwen2.5-3B](https://github.com/TTT-rfk/Mdlr1.0-Qwen2.5-3B). Its README links the public ModelScope files:

- Q8_0 GGUF, about 3.3 GB, recommended on most consumer GPUs.
- F16 GGUF, about 6.2 GB, higher disk and VRAM use.

Install Ollama, start it, then use the `Modelfile` from that repository to import the downloaded GGUF. From the folder containing the model repository's `Modelfile` and GGUF file, run:

```powershell
ollama create Mdlr1.0-Qwen2.5-3B -f Modelfile
ollama run Mdlr1.0-Qwen2.5-3B
```

Set `generation_model` in `config.json` to the exact tag printed by `ollama list`. The default expected tag is:

```text
Mdlr1.0-Qwen2.5-3B:f16
```

If you have a GGUF model file, import it with a Modelfile supplied by the model distributor. Do not claim a model is installed until this command lists it:

```powershell
ollama list
```

## 6. Provide a Compatible Knowledge Base

MldrH does not ship the theory corpus or Chroma database. The matching standard vector-database project is linked from the [Mdlr model repository](https://github.com/TTT-rfk/Mdlr1.0-Qwen2.5-3B). Obtain or build a lawful compatible Chroma database, then set its folder as `database_path`. It must contain a Chroma collection named `theory_knowledge` unless you changed `collection_name`. Without this asset, MldrH will show a startup error rather than silently answer without retrieval.

## 7. Launch

Double-click:

```text
MldrH.bat
```

or run it from PowerShell:

```powershell
.\MldrH.bat
```

## Troubleshooting

| Error | Meaning | Action |
|---|---|---|
| `E01` | Ollama is unavailable. | Start Ollama and verify `http://localhost:11434/api/tags` opens. |
| `E02` | The configured Mdlr model is unavailable. | Check `ollama list`, then import or use the correct model tag. |
| `E03` | A local model, adapter, prompt, or database asset is missing. | Check `config.json` and the required folder paths. |
| `E04` | A generation request failed. | Retry once, then inspect Ollama logs and GPU memory. |

## Security

Never put API keys, tokens, passwords, private training data, or personal documents in this folder before publishing it.
