import sys
import tkinter as tk
from converter import scan_directory, convert_file

def main():
    # Branch A: CLI Mode (Arguments provided -> Right Click Menu)
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        
        # Use simple Progress GUI instead of console print statements
        try:
            from gui import ProgressGUI
            root = tk.Tk()
            app = ProgressGUI(root, directory, auto_close=True)
            root.mainloop()
        except Exception as e:
            # Fallback to console if GUI fails
            print(f"Error launching progress GUI: {e}")
            print(f"Scanning '{directory}'...")
            files = scan_directory(directory)
            for f in files:
                convert_file(f)

    # Branch B: GUI Mode (No arguments -> Double Click)
    else:
        try:
            from gui import ModernGUI
            root = tk.Tk()
            app = ModernGUI(root)
            root.mainloop()
        except Exception as e:
            print(f"Error launching GUI: {e}")
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()
