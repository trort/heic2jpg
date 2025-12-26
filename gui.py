import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import sys
import os
from converter import scan_directory, convert_file

class ModernGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPG Converter")
        self.root.geometry("600x400")
        self.root.minsize(500, 350)
        
        # Set Icon if available
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "app.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except tk.TclError:
                pass # Linux/Mac might not support .ico directly via iconbitmap

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam' is usually cleaner than default on Windows
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TLabel", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        self.style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#666")

        # Layout
        main_frame = ttk.Frame(root, padding="30 30 30 20")
        main_frame.pack(fill="both", expand=True)

        # Header
        lbl_header = ttk.Label(main_frame, text="HEIC to JPG Converter", style="Header.TLabel")
        lbl_header.pack(pady=(0, 20))

        # Folder Selection
        folder_frame = ttk.LabelFrame(main_frame, text="Target Directory", padding="15 15 15 15")
        folder_frame.pack(fill="x", pady=(0, 20))

        self.var_dir = tk.StringVar()
        entry_dir = ttk.Entry(folder_frame, textvariable=self.var_dir)
        entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_browse = ttk.Button(folder_frame, text="Browse Folder", command=self.browse_directory)
        btn_browse.pack(side="right")

        # Action Area
        self.btn_start = ttk.Button(main_frame, text="Start Conversion", command=self.start_conversion_thread, state="disabled")
        self.btn_start.pack(pady=10, ipady=5, ipadx=20)
        
        # Log Area
        self.text_log = tk.Text(main_frame, height=8, width=50, bd=1, relief="solid", font=("Consolas", 9), state="disabled")
        self.text_log.pack(fill="both", expand=True, pady=10)

        # Status Bar
        self.lbl_status = ttk.Label(main_frame, text="Ready to start.", style="Status.TLabel")
        self.lbl_status.pack(anchor="w")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.var_dir.set(directory)
            self.btn_start["state"] = "normal"
            self.log(f"Selected: {directory}")

    def log(self, message):
        self.text_log.config(state="normal")
        self.text_log.insert(tk.END, message + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state="disabled")

    def start_conversion_thread(self):
        directory = self.var_dir.get()
        if not directory:
            return
            
        self.btn_start["state"] = "disabled"
        self.lbl_status["text"] = "Scanning directory..."
        
        thread = threading.Thread(target=self.run_conversion, args=(directory,))
        thread.start()
        
    def run_conversion(self, directory):
        try:
            files = scan_directory(directory)
            
            if not files:
                self.root.after(0, lambda: self.finish_conversion(0, 0, "No HEIC files found."))
                return

            self.root.after(0, lambda: self.log(f"Found {len(files)} files. Processing..."))
            
            success_count = 0
            for i, f in enumerate(files):
                pct = int(((i + 1) / len(files)) * 100)
                self.root.after(0, lambda idx=i, total=len(files): self.lbl_status.config(text=f"Converting {idx+1}/{total}"))
                
                if convert_file(f):
                    success_count += 1
                    self.root.after(0, lambda name=f: self.log(f"✓ {os.path.basename(name)}"))
                else:
                    self.root.after(0, lambda name=f: self.log(f"✗ Failed: {os.path.basename(name)}"))
            
            self.root.after(0, lambda: self.finish_conversion(success_count, len(files)))
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error: {e}"))
            self.root.after(0, lambda: self.finish_conversion(0, 0, "Error occurred."))

    def finish_conversion(self, success, total, message=None):
        self.btn_start["state"] = "normal"
        if message:
            self.lbl_status["text"] = message
            self.log(message)
        else:
            self.lbl_status["text"] = "Completed."
            self.log(f"Finished: {success}/{total} converted.")
            messagebox.showinfo("Complete", f"Converted {success} of {total} files.")


class ProgressGUI:
    """Minimal GUI for the Right-Click Context Menu mode."""
    def __init__(self, root, directory, auto_close=True):
        self.root = root
        self.directory = directory
        self.auto_close = auto_close
        
        self.root.title("Converting...")
        self.root.geometry("400x150")
        self.root.resizable(False, False)
        
        # Set Icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "app.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except tk.TclError:
                pass

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Segoe UI", 10))

        # UI
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        self.lbl_title = ttk.Label(main_frame, text="Converting HEIC to JPG", font=("Segoe UI", 12, "bold"))
        self.lbl_title.pack(anchor="w", pady=(0, 10))

        self.lbl_status = ttk.Label(main_frame, text=f"Scanning {os.path.basename(directory)}...")
        self.lbl_status.pack(anchor="w", pady=(0, 5))

        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=10)

        # Start automatically
        self.root.after(100, self.start_thread)

    def start_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        try:
            files = scan_directory(self.directory)
            if not files:
                self.root.after(0, lambda: self.lbl_status.config(text="No HEIC files found."))
                self.root.after(2000, self.root.destroy)
                return

            self.root.after(0, lambda: self.progress.config(maximum=len(files), value=0))
            
            for i, f in enumerate(files):
                self.root.after(0, lambda name=f: self.lbl_status.config(text=f"Converting: {os.path.basename(name)}"))
                convert_file(f)
                self.root.after(0, lambda: self.progress.step(1))
            
            self.root.after(0, lambda: self.lbl_status.config(text="Done!"))
            
            if self.auto_close:
                # Close after 1 second
                self.root.after(1000, self.root.destroy)
                
        except Exception as e:
            self.root.after(0, lambda: self.lbl_status.config(text=f"Error: {str(e)}"))
