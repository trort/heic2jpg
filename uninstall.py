
import sys
import os
import ctypes
import shutil
import winreg
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def uninstall():
    print("HEIC to JPG Converter Uninstaller")
    print("---------------------------------")
    
    # 1. Remove Registry Keys
    print("Removing Registry keys...")
    key_path = r"Directory\shell\Convert HEIC to JPG"
    try:
        # Try to delete command key first
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
        except FileNotFoundError:
            pass
            
        # Try to delete main key
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        except FileNotFoundError:
            pass
            
        print("  [OK] Registry keys removed.")
    except Exception as e:
        print(f"  [ERROR] Failed to remove registry keys: {e}")
        
    # 2. Remove Files
    # Target location: %LOCALAPPDATA%\HEIC2JPG
    local_app_data = os.environ.get('LOCALAPPDATA')
    if local_app_data:
        install_dir = os.path.join(local_app_data, "HEIC2JPG")
        
        if os.path.exists(install_dir):
            print(f"Removing files from {install_dir}...")
            # Self-deletion is tricky. 
            # If this script is running from that folder, we can't delete the folder easily.
            # Usually uninstaller copies itself to temp, runs from there, deletes original, then schedules its own deletion.
            # For simplicity, we will try to delete everything ELSE in that folder, and tell user to remove the folder manually if it fails.
            
            try:
                # Iterate and remove inputs
                for item in os.listdir(install_dir):
                    item_path = os.path.join(install_dir, item)
                    try:
                        if item_path == sys.executable or item_path == os.path.abspath(sys.argv[0]):
                            continue # Don't delete self yet
                        
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception as e:
                        print(f"  Could not delete {item}: {e}")
                
                print("  [OK] Files cleaned up.")
                
            except Exception as e:
                print(f"  [ERROR] removing files: {e}")
                
            print("\nNOTE: The uninstaller executable itself and the folder may remain.")
            print("You can manually delete this folder now.")
        else:
            print("  Installation folder not found (already removed?).")

    print("\nUninstallation Complete.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    if is_admin():
        uninstall()
    else:
        # Re-run with admin rights
        print("Requesting administrator privileges...")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except Exception as e:
            print(f"Error requesting admin rights: {e}")
            input("Press Enter to exit...")
