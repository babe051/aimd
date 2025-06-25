@echo off
echo.
echo 🚀 AIMD Setup for Windows
echo ========================
echo.
cd /d "%~dp0"

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: Administrator privileges required
    echo.
    echo Please right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: Python is not installed
    echo.
    echo Please install Python from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version

REM Check if required files exist
if not exist "aimd.py" (
    echo ❌ ERROR: aimd.py not found in current directory
    pause
    exit /b 1
)

if not exist "generator.py" (
    echo ❌ ERROR: generator.py not found in current directory
    pause
    exit /b 1
)

if not exist "utils.py" (
    echo ❌ ERROR: utils.py not found in current directory
    pause
    exit /b 1
)

echo.
echo 📦 Installing Python dependencies...
pip install certifi httpx requests pathspec tqdm
if %errorLevel% neq 0 (
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Create aimd directory in System32
set AIMD_DIR=C:\Windows\System32\aimd
echo.
echo 📂 Creating AIMD directory: %AIMD_DIR%
if not exist "%AIMD_DIR%" mkdir "%AIMD_DIR%"

REM Copy files
echo 📂 Copying AIMD files...
copy aimd.py "%AIMD_DIR%\" >nul
copy generator.py "%AIMD_DIR%\" >nul
copy utils.py "%AIMD_DIR%\" >nul

REM Create the local aimd command script
echo 📝 Creating command scripts...
echo @echo off > "%AIMD_DIR%\aimd.bat"
echo python "%AIMD_DIR%\aimd.py" %%* >> "%AIMD_DIR%\aimd.bat"

REM Create global aimd command
echo @echo off > "C:\Windows\System32\aimd.bat"
echo call "%AIMD_DIR%\aimd.bat" %%* >> "C:\Windows\System32\aimd.bat"

echo.
echo ✅ Installation completed successfully!
echo.
echo 🔑 IMPORTANT: Set your Google AI API key
echo    1. Get your API key from: https://aistudio.google.com/
echo    2. Run this command in Command Prompt or PowerShell:
echo       setx GOOGLE_API_KEY "your-api-key-here"
echo    3. Restart your terminal after setting the key
echo.
echo 🚀 Usage examples:
echo    aimd C:\path\to\project
echo    aimd . -i node_modules "*.log"
echo    aimd . --output DOCS.md --max-files 100
echo.
echo 📁 Installation location: %AIMD_DIR%
echo.
pause