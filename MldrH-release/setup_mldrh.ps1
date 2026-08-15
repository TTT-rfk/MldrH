param(
    [string]$Python = "python",
    [string]$ReleaseTag = "v1.1.0"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venv = Join-Path $root ".venv"
$venvPython = Join-Path $venv "Scripts\python.exe"
$assets = Join-Path $root "assets"
$embeddingBase = Join-Path $assets "BAAI-bge-m3"
$generationBase = Join-Path $assets "Qwen2.5-3B-Instruct"
$retrievalAdapter = Join-Path $root "adapters\Mdlr-theory-embed-v1"
$thinkAdapter = Join-Path $root "adapters\Mdlr1.1-think"
$database = Join-Path $root "knowledge_db_theory_v1"
$databaseZip = Join-Path $env:TEMP "MldrH-theory-knowledge-db-v1.1.0.zip"
$databaseUrl = "https://github.com/TTT-rfk/MldrH/releases/download/$ReleaseTag/MldrH-theory-knowledge-db-v1.1.0.zip"

if (-not (Test-Path -LiteralPath $venvPython)) {
    & $Python -m venv $venv
}
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $root "requirements.txt")

foreach ($path in @($retrievalAdapter, $thinkAdapter)) {
    if (-not (Test-Path -LiteralPath (Join-Path $path "adapter_model.safetensors"))) {
        throw "Bundled adapter missing: $path"
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $embeddingBase "pytorch_model.bin"))) {
    New-Item -ItemType Directory -Path $assets -Force | Out-Null
    & $venvPython -m pip install "modelscope>=1.30,<2.0"
    & (Join-Path $venv "Scripts\modelscope.exe") download --model "BAAI/bge-m3" --local_dir $embeddingBase
}

if (-not (Test-Path -LiteralPath (Join-Path $generationBase "config.json"))) {
    New-Item -ItemType Directory -Path $assets -Force | Out-Null
    & $venvPython -m pip install "modelscope>=1.30,<2.0"
    & (Join-Path $venv "Scripts\modelscope.exe") download --model "Qwen/Qwen2.5-3B-Instruct" --local_dir $generationBase
}

if (-not (Test-Path -LiteralPath (Join-Path $database "chroma.sqlite3"))) {
    Invoke-WebRequest -Uri $databaseUrl -OutFile $databaseZip
    Expand-Archive -LiteralPath $databaseZip -DestinationPath $root -Force
    Remove-Item -LiteralPath $databaseZip -Force
}

$configPath = Join-Path $root "config.json"
if (-not (Test-Path -LiteralPath $configPath)) {
    @{
        embedding_base_model = $embeddingBase
        generation_base_model = $generationBase
        retrieval_adapter = $retrievalAdapter
        think_adapter = $thinkAdapter
        database_path = $database
        collection_name = "theory_knowledge"
    } | ConvertTo-Json | Set-Content -LiteralPath $configPath -Encoding utf8
}

& $venvPython -c "import chromadb; c=chromadb.PersistentClient(path=r'$database').get_collection('theory_knowledge'); d=c.get(include=['metadatas']); assert c.count() == 5089; assert all(m.get('type') == 'pt' for m in d['metadatas']); print('collection=theory_knowledge'); print('count=5089'); print('types=pt'); print('MldrH v1.1 setup complete.')"
