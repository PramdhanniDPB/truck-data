@echo off

@REM Activate virtual environment if exists
if exist env\Scripts\activate (
    call env\Scripts\activate
)
@REM Run the main Python script
python main.py

@REM Deactivate virtual environment if it was activated
if exist env\Scripts\activate (
    call env\Scripts\deactivate
)

@REM Push to github
git add .
git commit -m "Auto commit from flow.bat"
git push origin main


