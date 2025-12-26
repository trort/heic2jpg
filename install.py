import sys
import os
import ctypes
import shutil
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install():
    # 1. Setup Paths
    # Current location of the installer/exe
    if getattr(sys, 'frozen', False):
        current_dir = os.path.dirname(sys.executable)
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    exe_name = "HEIC2JPG.exe"
    source_exe = os.path.join(current_dir, exe_name)
    
    # Target location: %LOCALAPPDATA%\HEIC2JPG
    local_app_data = os.environ.get('LOCALAPPDATA')
    if not local_app_data:
        print("Error: Could not find LOCALAPPDATA environment variable.")
        input("Press Enter to exit...")
        return

    install_dir = os.path.join(local_app_data, "HEIC2JPG")
    target_exe = os.path.join(install_dir, exe_name)

    print(f"Installing to: {install_dir}")

    # 2. Copy Files
    try:
        if not os.path.exists(source_exe):
            print(f"Error: Could not find {exe_name} in current directory.")
            print("Please ensure install.exe and HEIC2JPG.exe are in the same folder.")
            input("Press Enter to exit...")
            return

        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        
        shutil.copy2(source_exe, target_exe)
        print("  [OK] Copied executable.")
        
    except Exception as e:
        print(f"Error copying files: {e}")
        input("Press Enter to exit...")
        return

    # 3. Registry Integration
    try:
        key_path = r"Directory\shell\Convert HEIC to JPG"
        
        # Create Key
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
        # Set Icon (uses the exe itself as the icon source)
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, target_exe)
        winreg.CloseKey(key)
        
        # Set Command
        command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
        # Command format: "C:\Path\To\Exe" "%1"
        winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{target_exe}" "%1"')
        winreg.CloseKey(command_key)
        
        print("  [OK] Registry keys added.")
        
    except Exception as e:
        print(f"Error modifying registry: {e}")
        input("Press Enter to exit...")
        return

    print("\nInstallation Complete!")
    print("You can now right-click any folder and select 'Convert HEIC to JPG'.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    if is_admin():
        install()
    else:
        # Re-run the program with admin rights
        print("Requesting administrator privileges...")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except Exception as e:
            print(f"Error requesting admin rights: {e}")
            input("Press Enter to exit...")
