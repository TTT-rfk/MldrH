param(
    [Parameter(Mandatory = $true)]
    [string]$DatabaseSource,

    [string]$Python = "python",

    [string]$OutputDirectory = (Split-Path -Parent $MyInvocation.MyCommand.Path)
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$staging = Join-Path $env:TEMP "MldrH-v1.1.0-build"
$terminalZip = Join-Path $OutputDirectory "MldrH-release-v1.1.0.zip"
$databaseZip = Join-Path $OutputDirectory "MldrH-theory-knowledge-db-v1.1.0.zip"
$manifest = Join-Path $OutputDirectory "SHA256SUMS-v1.1.0.txt"

if (-not (Test-Path -LiteralPath (Join-Path $root "adapters\Mdlr1.1-think\adapter_model.safetensors"))) { throw "Mdlr1.1-think adapter is missing." }
if (-not (Test-Path -LiteralPath (Join-Path $root "adapters\Mdlr-theory-embed-v1\adapter_model.safetensors"))) { throw "Mdlr-theory-embed-v1 adapter is missing." }
if (-not (Test-Path -LiteralPath (Join-Path $DatabaseSource "chroma.sqlite3"))) { throw "PT database is missing chroma.sqlite3." }

Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $staging -Force | Out-Null
$package = Join-Path $staging "MldrH-release"
New-Item -ItemType Directory -Path $package -Force | Out-Null

Get-ChildItem -LiteralPath $root -Force | Where-Object {
    $_.Name -notin @("adapter", "assets", "knowledge_db_theory_v1", ".venv", "__pycache__", "build_release_assets.ps1", "SHA256SUMS.txt")
} | Copy-Item -Destination $package -Recurse -Force

Get-ChildItem -LiteralPath (Join-Path $package "adapters\Mdlr1.1-think") -Directory -Filter "checkpoint-*" | Remove-Item -Recurse -Force

& $Python -c "import chromadb; c=chromadb.PersistentClient(path=r'$DatabaseSource').get_collection('theory_knowledge'); d=c.get(include=['metadatas']); assert c.count()==5089; assert all(m.get('type')=='pt' for m in d['metadatas']); print('collection=theory_knowledge count=5089 types=pt')"

Remove-Item -LiteralPath $terminalZip -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $databaseZip -Force -ErrorAction SilentlyContinue
Compress-Archive -LiteralPath $package -DestinationPath $terminalZip -CompressionLevel Optimal
Compress-Archive -LiteralPath $DatabaseSource -DestinationPath $databaseZip -CompressionLevel Optimal
if (-not (Test-Path -LiteralPath $terminalZip) -or -not (Test-Path -LiteralPath $databaseZip)) { throw "Release ZIP creation failed." }

$hashes = @(
    "# MldrH v1.1.0 SHA-256",
    "$( (Get-FileHash -Algorithm SHA256 -LiteralPath $terminalZip).Hash )  $(Split-Path -Leaf $terminalZip)",
    "$( (Get-FileHash -Algorithm SHA256 -LiteralPath $databaseZip).Hash )  $(Split-Path -Leaf $databaseZip)",
    "$( (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root 'adapters\Mdlr1.1-think\adapter_model.safetensors')).Hash )  adapters/Mdlr1.1-think/adapter_model.safetensors",
    "$( (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root 'adapters\Mdlr-theory-embed-v1\adapter_model.safetensors')).Hash )  adapters/Mdlr-theory-embed-v1/adapter_model.safetensors"
)
$hashes | Set-Content -LiteralPath $manifest -Encoding utf8
Get-Content -LiteralPath $manifest
