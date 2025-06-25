@echo off
echo.
echo 🗑️ AIMD Uninstaller for Windows
echo ==============================
echo.

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

echo ⚠️  This will remove AIMD from your system
echo.
set /p confirm="Are you sure you want to uninstall AIMD? (y/N): "

if /i not "%confirm%"=="y" (
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

echo.
echo 🗑️ Removing AIMD files...

REM Remove global command
if exist "C:\Windows\System32\aimd.bat" (
    del "C:\Windows\System32\aimd.bat"
    echo ✅ Removed global aimd command
) else (
    echo ⚠️  Global aimd command not found
)

REM Remove AIMD directory
if exist "C:\Windows\System32\aimd" (
    rmdir /s /q "C:\Windows\System32\aimd"
    echo ✅ Removed AIMD directory
) else (
    echo ⚠️  AIMD directory not found
)

echo.
echo ✅ AIMD has been uninstalled successfully!
echo.
echo 💡 Note: Python dependencies were not removed
echo    If you want to remove them, run:
echo    pip uninstall certifi httpx requests pathspec tqdm
echo.
echo 🔑 Your GOOGLE_API_KEY environment variable was not removed
echo    If you want to remove it, run:
echo    reg delete "HKCU\Environment" /v GOOGLE_API_KEY /f
echo.
pause