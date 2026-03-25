@echo off
REM Script de Restauração do Ecossistema Opencode
REM Data: 2026-03-23

echo ============================================
echo  Restauração do Ecossistema Opencode
echo ============================================
echo.

set BACKUP_FILE=backup-opencode-todos-20260323.tar.gz
set PROJECT_DIR=%cd%

echo 1. Restaurando ~/.opencode...
cd /d %USERPROFILE%
tar -xzvf "%PROJECT_DIR%\%BACKUP_FILE%" .opencode
if %errorlevel% neq 0 (
    echo Erro ao restaurar ~/.opencode
    pause
    exit /b 1
)
echo    ✓ ~/.opencode restaurado

echo.
echo 2. Restaurando arquivos do projeto...
cd /d "%PROJECT_DIR%"
tar -xzvf "%BACKUP_FILE%" ^
  criador-de-artigo-v2 ^
  PageIndex ^
  examples ^
  .env ^
  academic-api-keys.env ^
  academic-api-config.json ^
  mcp_servers_config.json ^
  ecosystem-transformer-config.json ^
  maswos-academic-config.json ^
  maswos-academic-geospatial-config.json ^
  maswos-juridico-config.json ^
  maswos-mcp-config.json ^
  mcp-ecossistema-tese ^
  mcp-tese-completa ^
  SKILL.md ^
  SKILL_ACADEMIC.md ^
  SKILL_UNIFICADO.md
if %errorlevel% neq 0 (
    echo Erro ao restaurar arquivos do projeto
    pause
    exit /b 1
)
echo    ✓ Arquivos do projeto restaurados

echo.
echo 3. Instalando dependências do PageIndex...
cd PageIndex
if exist requirements.txt (
    pip install -r requirements.txt
    echo    ✓ Dependências do PageIndex instaladas
) else (
    echo    ⚠ requirements.txt não encontrado
)

echo.
echo 4. Verificando Node.js modules...
cd /d %USERPROFILE%\.opencode
if exist node_modules (
    echo    ✓ node_modules já presente
) else (
    echo    ⚠ node_modules não encontrado. Executar: npm install
)

echo.
echo ============================================
echo  Restauração concluída!
echo ============================================
echo.
echo Próximos passos:
echo 1. Verificar chaves de API nos arquivos .env
echo 2. Instalar opencode novamente se necessário
echo 3. Testar os MCPs e skills
echo.
pause