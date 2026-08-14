param(
    [string]$Python = "python",
    [string]$GenerationModel = "Mdlr1.0-Qwen2.5-3B:f16"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $root ".venv\Scripts\python.exe"
$baseModel = Join-Path $root "assets\BAAI-bge-m3"
$adapter = Join-Path $root "adapter"
$database = Join-Path $root "knowledge_db_theory_v1"
$databaseZip = Join-Path $env:TEMP "MldrH-theory-knowledge-db-v1.zip"
$databaseUrl = "https://github.com/TTT-rfk/MldrH/releases/download/v1.0.0/MldrH-theory-knowledge-db-v1.zip"
$baseModelUrl = "https://modelscope.cn/models/BAAI/bge-m3"

if (-not (Test-Path -LiteralPath $venvPython)) {
    & $Python -m venv (Join-Path $root ".venv")
}
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $root "requirements.txt")

if (-not (Test-Path -LiteralPath (Join-Path $adapter "adapter_model.safetensors"))) {
    throw "Adapter is missing. Re-download the MldrH repository so the adapter folder is present."
}

if (-not (Test-Path -LiteralPath (Join-Path $baseModel "pytorch_model.bin"))) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $baseModel) -Force | Out-Null
    & $venvPython -m pip install "modelscope>=1.30,<2.0"
    & (Join-Path $root ".venv\Scripts\modelscope.exe") download --model "BAAI/bge-m3" --local_dir $baseModel
    if (-not (Test-Path -LiteralPath (Join-Path $baseModel "pytorch_model.bin"))) {
        throw "BAAI/bge-m3 download did not produce pytorch_model.bin. Download it manually from $baseModelUrl and place it at $baseModel."
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $database "chroma.sqlite3"))) {
    Invoke-WebRequest -Uri $databaseUrl -OutFile $databaseZip
    Expand-Archive -LiteralPath $databaseZip -DestinationPath $root -Force
    Remove-Item -LiteralPath $databaseZip -Force
}

$tags = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get
if ($GenerationModel -notin @($tags.models | ForEach-Object name)) {
    throw "Ollama model '$GenerationModel' is missing. Download and import it from https://github.com/TTT-rfk/Mdlr1.0-Qwen2.5-3B, then rerun this script."
}

$config = @{
    base_model = $baseModel
    adapter_path = $adapter
    database_path = $database
    collection_name = "theory_knowledge"
    ollama_url = "http://localhost:11434"
    generation_model = $GenerationModel
} | ConvertTo-Json
$config | Set-Content -LiteralPath (Join-Path $root "config.json") -Encoding utf8

& $venvPython -c "import chromadb; c=chromadb.PersistentClient(path=r'$database').get_collection('theory_knowledge'); assert c.count() == 5659; print('MldrH setup complete.')"
