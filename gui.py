import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from converter import scan_directory, convert_file

class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPG Converter")
        self.root.geometry("500x300")
        
        # Directory Selection
        self.dir_frame = tk.Frame(root, pady=20)
        self.dir_frame.pack(fill="x", padx=20)
        
        self.lbl_dir = tk.Label(self.dir_frame, text="Select Folder:")
        self.lbl_dir.pack(side="left")
        
        self.entry_dir = tk.Entry(self.dir_frame, width=40)
        self.entry_dir.pack(side="left", padx=10)
        
        self.btn_browse = tk.Button(self.dir_frame, text="Browse", command=self.browse_directory)
        self.btn_browse.pack(side="left")
        
        # Start Button
        self.btn_start = tk.Button(root, text="Start Conversion", state="disabled", command=self.start_conversion_thread)
        self.btn_start.pack(pady=10)
        
        # Status Log
        self.lbl_status = tk.Label(root, text="Ready")
        self.lbl_status.pack(pady=5)
        
        self.text_log = tk.Text(root, height=10, width=55, state="disabled")
        self.text_log.pack(padx=20, pady=10)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, directory)
            self.btn_start["state"] = "normal"
            self.log(f"Selected: {directory}")

    def log(self, message):
        self.text_log.config(state="normal")
        self.text_log.insert(tk.END, message + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state="disabled")

    def start_conversion_thread(self):
        directory = self.entry_dir.get()
        if not directory:
            return
            
        self.btn_start["state"] = "disabled"
        self.btn_browse["state"] = "disabled"
        self.lbl_status["text"] = "Scanning..."
        
        thread = threading.Thread(target=self.run_conversion, args=(directory,))
        thread.start()
        
    def run_conversion(self, directory):
        try:
            files = scan_directory(directory)
            
            if not files:
                self.root.after(0, lambda: self.finish_conversion(0, 0, "No HEIC files found."))
                return

            self.root.after(0, lambda: self.log(f"Found {len(files)} files. Starting..."))
            
            success_count = 0
            for i, f in enumerate(files):
                self.root.after(0, lambda idx=i, total=len(files): self.update_status(f"Converting {idx+1}/{total}"))
                if convert_file(f):
                    success_count += 1
                    self.root.after(0, lambda name=f: self.log(f"✓ {name}"))
                else:
                    self.root.after(0, lambda name=f: self.log(f"✗ Failed: {name}"))
            
            self.root.after(0, lambda: self.finish_conversion(success_count, len(files)))
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error: {e}"))
            self.root.after(0, lambda: self.finish_conversion(0, 0, "Error occurred."))

    def update_status(self, text):
        self.lbl_status["text"] = text

    def finish_conversion(self, success, total, message=None):
        self.btn_start["state"] = "normal"
        self.btn_browse["state"] = "normal"
        if message:
            self.lbl_status["text"] = message
            self.log(message)
        else:
            self.lbl_status["text"] = "Done"
            self.log(f"Finished: {success}/{total} converted successfully.")
            messagebox.showinfo("Complete", f"Converted {success} of {total} files.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()
