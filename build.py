import PyInstaller.__main__
import shutil
import os

def build():
    print("Starting build process...")
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    print("Building Main Application (HEIC2JPG.exe)...")
    PyInstaller.__main__.run([
        'main.py',
        '--name=HEIC2JPG',
        '--onefile',
        '--noconsole',  # Hide black window (we now have a GUI progress bar)
        '--icon=icons/app.ico',
        # Embed icon file so gui.py can find it via resource_path
        '--add-data=icons/app.ico:icons',
        '--collect-all=pillow_heif',
        '--clean',
    ])
    
    print("\nBuilding Installer (install.exe)...")
    PyInstaller.__main__.run([
        'install.py',
        '--name=install',
        '--onefile',
        '--console',  # Installer still needs console for now/simplicity or can be GUI too, keeping console for debug feedback
        '--icon=icons/install.ico',
        '--clean',
    ])
    
    print("\nBuild complete. Check the 'dist' folder.")
    print("You will see: HEIC2JPG.exe and install.exe")

if __name__ == "__main__":
    build()
