@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "LOG_DIR=%~dp0logs"
set "LOG_FILE=%LOG_DIR%\flow.log"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

call :log "Flow started"

set "VENV_ACTIVATED=0"
if exist env\Scripts\activate.bat (
    call :log "Activating virtual environment"
    call env\Scripts\activate.bat
    set "VENV_ACTIVATED=1"
) else (
    call :log "Virtual environment not found, using system Python"
)

call :log "Running main2.py"
python main2.py
set "PYTHON_EXIT_CODE=!errorlevel!"
call :log "main2.py finished with exit code !PYTHON_EXIT_CODE!"

if "!VENV_ACTIVATED!"=="1" (
    call :log "Deactivating virtual environment"
    call env\Scripts\deactivate.bat
)

call :log "Starting git push sequence"
git add .
if errorlevel 1 (
    call :log "git add failed with exit code !errorlevel!"
    exit /b 1
)

git commit -m "Auto commit from flow.bat"
set "COMMIT_EXIT_CODE=!errorlevel!"
if not "!COMMIT_EXIT_CODE!"=="0" (
    call :log "git commit exit code !COMMIT_EXIT_CODE!"
)

git push origin main
set "PUSH_EXIT_CODE=!errorlevel!"
call :log "git push finished with exit code !PUSH_EXIT_CODE!"

call :log "Flow finished"
exit /b !PUSH_EXIT_CODE!

:log
set "LOG_TIMESTAMP=%date% %time%"
echo [!LOG_TIMESTAMP!] %~1
>> "%LOG_FILE%" echo [!LOG_TIMESTAMP!] %~1
exit /b 0


