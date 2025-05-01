@echo off
echo Building Todo List Manager...

REM Generate icon if not exists
if not exist todo_icon.ico (
    echo Generating icon...
    python todo_icon.py
)

REM Install required packages if missing
echo Checking and installing required packages...
pip install pillow pyinstaller PyQt5

REM Build the executable with PyInstaller
echo Building executable with PyInstaller...
pyinstaller --onefile --windowed --icon=todo_icon.ico --add-data "todo.py;." todo_gui.py

REM Check if executable was created
if not exist "dist\todo_gui.exe" (
    echo.
    echo Error: PyInstaller failed to create the executable.
    echo Please check if all required packages are installed.
    echo Run: pip install PyQt5 pillow
    pause
    exit /b 1
)

REM Check if Inno Setup is installed
set "InnoSetupPath=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%InnoSetupPath%" (
    echo.
    echo Inno Setup not found at: %InnoSetupPath%
    echo Please download and install Inno Setup from: https://jrsoftware.org/isdl.php
    echo.
    echo Alternative paths to check:
    echo - C:\Program Files\Inno Setup 6\ISCC.exe
    echo - C:\Program Files (x86)\Inno Setup\ISCC.exe
    echo.
    echo After installation, run this script again to build the installer.
    echo.
    pause
    exit /b 1
)

REM Build the installer with Inno Setup
echo Building installer with Inno Setup...
"%InnoSetupPath%" todo_setup.iss

echo.
if exist "Output\TodoListManager_Setup.exe" (
    echo Build successful! The installer is located at: Output\TodoListManager_Setup.exe
) else (
    echo Build failed. Please check the logs above for errors.
)

pause 