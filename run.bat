@echo off
set "venv_dir=venv"
set "activate_cmd=venv\Scripts\activate"

:: Check if virtual environment exists
if not exist %venv_dir% (
    echo Virtual environment not found. Setting up virtual environment...
    python -m venv %venv_dir%
    echo Virtual environment created.
    echo Installing dependencies...
    call %activate_cmd%
    pip install -r requirements.txt
    echo Dependencies installed.
) else (
    echo Virtual environment found.
)

:: Activate virtual environment
echo Activating virtual environment...
call %activate_cmd%

:: Run the Python script
echo Running script...
python main.py

:: Deactivate virtual environment
echo Deactivating virtual environment...
deactivate

pause
