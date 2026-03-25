# Script de Restauração do Ecossistema Opencode - PowerShell
# Data: 2026-03-23

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Restauração do Ecossistema Opencode" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$backupFile = "backup-opencode-todos-20260323.tar.gz"
$projectDir = Get-Location

# 1. Restaurar ~/.opencode
Write-Host "1. Restaurando ~/.opencode..." -ForegroundColor Yellow
Set-Location $env:USERPROFILE
& tar -xzvf "$projectDir\$backupFile" ".opencode"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao restaurar ~/.opencode" -ForegroundColor Red
    exit 1
}
Write-Host "   ✓ ~/.opencode restaurado" -ForegroundColor Green

# 2. Restaurar arquivos do projeto
Write-Host ""
Write-Host "2. Restaurando arquivos do projeto..." -ForegroundColor Yellow
Set-Location $projectDir
$filesToRestore = @(
    "criador-de-artigo-v2",
    "PageIndex",
    "examples",
    ".env",
    "academic-api-keys.env",
    "academic-api-config.json",
    "mcp_servers_config.json",
    "ecosystem-transformer-config.json",
    "maswos-academic-config.json",
    "maswos-academic-geospatial-config.json",
    "maswos-juridico-config.json",
    "maswos-mcp-config.json",
    "mcp-ecossistema-tese",
    "mcp-tese-completa",
    "SKILL.md",
    "SKILL_ACADEMIC.md",
    "SKILL_UNIFICADO.md"
)

& tar -xzvf $backupFile $filesToRestore
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao restaurar arquivos do projeto" -ForegroundColor Red
    exit 1
}
Write-Host "   ✓ Arquivos do projeto restaurados" -ForegroundColor Green

# 3. Instalar dependências do PageIndex
Write-Host ""
Write-Host "3. Instalando dependências do PageIndex..." -ForegroundColor Yellow
Set-Location "$projectDir\PageIndex"
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "   ✓ Dependências do PageIndex instaladas" -ForegroundColor Green
} else {
    Write-Host "   ⚠ requirements.txt não encontrado" -ForegroundColor Yellow
}

# 4. Verificar Node.js modules
Write-Host ""
Write-Host "4. Verificando Node.js modules..." -ForegroundColor Yellow
Set-Location "$env:USERPROFILE\.opencode"
if (Test-Path "node_modules") {
    Write-Host "   ✓ node_modules já presente" -ForegroundColor Green
} else {
    Write-Host "   ⚠ node_modules não encontrado. Executar: npm install" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Restauração concluída!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor White
Write-Host "1. Verificar chaves de API nos arquivos .env" -ForegroundColor White
Write-Host "2. Instalar opencode novamente se necessário" -ForegroundColor White
Write-Host "3. Testar os MCPs e skills" -ForegroundColor White
Write-Host ""
Read-Host "Pressione Enter para continuar"