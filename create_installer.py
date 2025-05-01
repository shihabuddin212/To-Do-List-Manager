#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a Python package using pip"""
    print(f"Installing {package_name}...")
    subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)

def find_inno_setup():
    """Find the Inno Setup compiler executable"""
    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup\ISCC.exe",
        r"C:\Program Files\Inno Setup\ISCC.exe"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def main():
    print("===== Todo List Manager Installer Creator =====")
    
    # Check and install required packages
    required_packages = ["PyQt5", "pillow", "pyinstaller"]
    for package in required_packages:
        if not check_package(package):
            print(f"{package} not found. Installing...")
            try:
                install_package(package)
                print(f"{package} installed successfully!")
            except subprocess.CalledProcessError:
                print(f"Error installing {package}. Please install it manually with: pip install {package}")
                input("Press Enter to exit...")
                return
    
    # Generate icon if not exists
    if not os.path.exists("todo_icon.ico"):
        print("Generating application icon...")
        try:
            subprocess.run([sys.executable, "todo_icon.py"], check=True)
        except subprocess.CalledProcessError:
            print("Error generating icon. Continuing anyway...")
    
    # Clean previous build
    if os.path.exists("dist"):
        print("Cleaning previous build...")
        shutil.rmtree("dist", ignore_errors=True)
    if os.path.exists("build"):
        shutil.rmtree("build", ignore_errors=True)
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__", ignore_errors=True)
    if os.path.exists("todo_gui.spec"):
        os.remove("todo_gui.spec")
    
    # Build executable
    print("\nBuilding executable with PyInstaller...")
    try:
        subprocess.run([
            sys.executable, "-m", "pyinstaller",
            "--onefile", "--windowed",
            "--icon=todo_icon.ico",
            "--add-data", f"todo.py{os.pathsep}.",
            "todo_gui.py"
        ], check=True)
    except subprocess.CalledProcessError:
        print("Error building executable. Check if all dependencies are installed.")
        input("Press Enter to exit...")
        return
    
    # Verify executable was created
    if not os.path.exists(os.path.join("dist", "todo_gui.exe")):
        print("Error: PyInstaller failed to create the executable.")
        input("Press Enter to exit...")
        return
    
    # Create Output directory if it doesn't exist
    os.makedirs("Output", exist_ok=True)
    
    # Find Inno Setup
    inno_setup_path = find_inno_setup()
    if not inno_setup_path:
        print("\nInno Setup not found. Please download and install Inno Setup from: https://jrsoftware.org/isdl.php")
        print("After installation, run this script again to build the installer.")
        input("Press Enter to exit...")
        return
    
    # Build installer
    print("\nBuilding installer with Inno Setup...")
    try:
        subprocess.run([inno_setup_path, "todo_setup.iss"], check=True)
    except subprocess.CalledProcessError:
        print("Error building installer. Check the Inno Setup script for errors.")
        input("Press Enter to exit...")
        return
    
    # Verify installer was created
    installer_path = os.path.join("Output", "TodoListManager_Setup.exe")
    if os.path.exists(installer_path):
        print(f"\nBuild successful! The installer is located at: {installer_path}")
        
        # Ask if user wants to open the output folder
        open_folder = input("\nDo you want to open the Output folder? (y/n): ").strip().lower()
        if open_folder == 'y':
            os.startfile(os.path.abspath("Output"))
        
        # Ask if user wants to run the installer
        run_installer = input("Do you want to run the installer now? (y/n): ").strip().lower()
        if run_installer == 'y':
            print("\nLaunching installer...")
            subprocess.Popen([installer_path])
    else:
        print("\nBuild failed. The installer was not created.")
    
    print("\nDone!")

if __name__ == "__main__":
    main() 