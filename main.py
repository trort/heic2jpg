import sys
from converter import scan_directory, convert_file

def main():
    # Branch A: CLI Mode (Arguments provided)
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        print(f"Scanning '{directory}' for .heic files...")
        
        files = scan_directory(directory)
        if not files:
            print("No .heic files found.")
            return

        print(f"Found {len(files)} files. Starting conversion...")
        
        success_count = 0
        for f in files:
            if convert_file(f):
                success_count += 1
                
        print(f"Done. Successfully converted {success_count}/{len(files)} files.")
        
        # Keep window open briefly if launched via double-click/context menu (optional behavior check)
        # For now, we just exit.

    # Branch B: GUI Mode (No arguments)
    else:
        try:
            import tkinter as tk
            from gui import ConverterGUI
            root = tk.Tk()
            app = ConverterGUI(root)
            root.mainloop()
        except ImportError:
            print("Error: Tkinter not found. Cannot launch GUI.")
        except Exception as e:
            print(f"Error launching GUI: {e}")

if __name__ == "__main__":
    main()
