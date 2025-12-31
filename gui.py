import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import sys
import os
from converter import scan_directory, convert_file

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ConflictDialog(tk.Toplevel):
    def __init__(self, parent, filename):
        super().__init__(parent)
        self.title("File Conflict")
        self.configure(bg="#ffffff") # White background
        self.geometry("550x200")
        self.resizable(False, False)
        self.grab_set() # Modal
        
        self.result = "skip"
        self.apply_to_all = False
        
        # Center the window
        self.update_idletasks()
        width = 550
        height = 200
        x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main Container with White Background
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)
        # Force styles for this Toplevel if needed, but since we use ttk Frame, it should pick up global style.
        # However, to be safe against gray toplevel background, we set bg="#ffffff" on self.
        
        # Message Area
        # Two lines as requested: "File already exists:" then Filename
        ttk.Label(main_frame, text="File already exists:", font=("Segoe UI", 10)).pack(anchor="center", pady=(5, 2))
        
        # Filename - Highlighted (Bold)
        # Truncate middle if extremely long to avoid window expansion issues
        display_name = filename
        if len(display_name) > 50:
             display_name = display_name[:20] + "..." + display_name[-25:]
             
        ttk.Label(main_frame, text=display_name, font=("Segoe UI", 11, "bold"), foreground="#0078d4").pack(anchor="center", pady=(0, 10))
        
        # Buttons Area
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=5)
        
        # Side by side buttons
        ttk.Button(btn_frame, text="Overwrite", command=lambda: self.set_result("overwrite")).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(btn_frame, text="Rename", command=lambda: self.set_result("rename")).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(btn_frame, text="Skip", command=lambda: self.set_result("skip")).pack(side="left", fill="x", expand=True, padx=5)
        
        self.var_apply = tk.BooleanVar(value=True) # Default True per user request
        ttk.Checkbutton(main_frame, text="Apply to all remaining conflicts", variable=self.var_apply).pack(pady=(5, 0))
        
    def set_result(self, action):
        self.result = action
        self.apply_to_all = self.var_apply.get()
        self.destroy()

class ModernGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPG Converter")
        self.root.geometry("600x400")
        self.root.minsize(500, 350)
        
        # Set Icon if available
        icon_path = resource_path(os.path.join("icons", "app.ico"))
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except tk.TclError:
                pass # Linux/Mac might not support .ico directly via iconbitmap

        # Style Configuration
        self.style = ttk.Style()
        
        # Try native theme first
        available_themes = self.style.theme_names()
        if 'vista' in available_themes:
            self.style.theme_use('vista')
        elif 'clam' in available_themes:
            self.style.theme_use('clam')

        # Define modern colors (Windows 11 Light Mode vibe)
        bg_color = "#ffffff"
        text_color = "#202020"
        
        # Configure Root background
        self.root.configure(bg=bg_color)
        
        # Configure Global Styles
        self.style.configure(".", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelframe", background=bg_color, foreground=text_color)
        self.style.configure("TLabelframe.Label", background=bg_color, foreground=text_color, font=("Segoe UI", 9, "bold"))
        
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        
        self.style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#000000", background=bg_color)
        self.style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#666666", background=bg_color)

        # Layout
        main_frame = ttk.Frame(root, padding="40 30 40 30")
        main_frame.pack(fill="both", expand=True)

        # Header
        lbl_header = ttk.Label(main_frame, text="HEIC to JPG Converter", style="Header.TLabel")
        lbl_header.pack(pady=(0, 30))

        # Folder Selection
        folder_frame = ttk.LabelFrame(main_frame, text="Target Directory", padding="15")
        folder_frame.pack(fill="x", pady=(0, 25))

        self.var_dir = tk.StringVar()
        entry_dir = ttk.Entry(folder_frame, textvariable=self.var_dir)
        entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=3)
        
        btn_browse = ttk.Button(folder_frame, text="Browse...", command=self.browse_directory)
        btn_browse.pack(side="right")

        # Options Area
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="15")
        options_frame.pack(fill="x", pady=(0, 20))
        
        # Recursive
        self.var_recursive = tk.BooleanVar(value=True)
        chk_recursive = ttk.Checkbutton(options_frame, text="Recursive Scan", variable=self.var_recursive)
        chk_recursive.pack(anchor="w", pady=(0, 10))
        
        # Overwrite Policy
        lbl_overwrite = ttk.Label(options_frame, text="If file exists:")
        lbl_overwrite.pack(anchor="w", pady=(0, 5))
        
        self.combo_overwrite = ttk.Combobox(options_frame, state="readonly", values=[
            "Overwrite existing", 
            "Skip existing", 
            "Save to 'converted' folder"
        ])
        self.combo_overwrite.current(0) # Default to Overwrite (or should be Separate Folder? User said give option. Let's stick to Overwrite as index 0 or Separate as index 2. I'll pick Overwrite as default to match old behavior but Separate is cleaner. Let's stick to Overwrite being default for now unless specified.)
        self.combo_overwrite.pack(fill="x")

        # Action Area
        self.btn_start = ttk.Button(main_frame, text="Start Conversion", command=self.start_conversion_thread, state="disabled")
        self.btn_start.pack(pady=10, ipady=5, ipadx=30)
        
        # Log Area
        self.text_log = tk.Text(main_frame, height=8, bd=1, relief="solid", font=("Consolas", 9), state="disabled", bg="#f9f9f9")
        self.text_log.pack(fill="both", expand=True, pady=15)

        # Status Bar
        self.lbl_status = ttk.Label(main_frame, text="Ready.", style="Status.TLabel")
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
            
        # Get Settings
        recursive = self.var_recursive.get()
        overwrite_choice = self.combo_overwrite.get()
        
        # Map choice to policy string
        policy_map = {
            "Overwrite existing": "overwrite",
            "Skip existing": "skip",
            "Save to 'converted' folder": "subfolder"
        }
        policy = policy_map.get(overwrite_choice, "overwrite")

        self.btn_start["state"] = "disabled"
        self.lbl_status["text"] = "Scanning directory..."
        
        thread = threading.Thread(target=self.run_conversion, args=(directory, recursive, policy))
        thread.start()
        
    def run_conversion(self, directory, recursive, policy):
        try:
            files = scan_directory(directory, recursive=recursive)
            
            if not files:
                self.root.after(0, lambda: self.finish_conversion(0, 0, "No HEIC files found."))
                return
            
            self.root.after(0, lambda: self.log(f"Found {len(files)} files. Processing..."))
            
            success_count = 0
            for i, f in enumerate(files):
                pct = int(((i + 1) / len(files)) * 100)
                self.root.after(0, lambda idx=i, total=len(files): self.lbl_status.config(text=f"Converting {idx+1}/{total}"))
                
                # Standalone always preserves EXIF now (per user request)
                if convert_file(f, overwrite_policy=policy):
                    success_count += 1
                    self.root.after(0, lambda name=f: self.log(f"✓ {os.path.basename(name)}"))
                else:
                    self.root.after(0, lambda name=f: self.log(f"✗ Failed/Skipped: {os.path.basename(name)}"))
            
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
        
        # Conflict state
        self.conflict_decision_memory = None
        
        self.root.title("Converting...")
        self.root.geometry("400x150")
        self.root.resizable(False, False)
        
        # Set Icon if available
        # Use resource_path to find icon inside the generic PyInstaller bundle
        icon_path = resource_path(os.path.join("icons", "app.ico"))
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except tk.TclError:
                pass # Linux/Mac might not support .ico directly via iconbitmap

        # Style Configuration
        self.style = ttk.Style()
        
        # Try to use a native-looking theme if available
        available_themes = self.style.theme_names()
        if 'vista' in available_themes:
            self.style.theme_use('vista')
        elif 'clam' in available_themes:
            self.style.theme_use('clam')

        # Define modern colors and fonts
        bg_color = "#ffffff"  # White background for a cleaner look
        text_color = "#333333"
        accent_color = "#0078d4" # Windows Blue
        
        # Configure Root background (Tkinter standard widgets needs this)
        self.root.configure(bg=bg_color)
        
        # Configure Ttk widget styles
        self.style.configure(".", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelframe", background=bg_color, foreground=text_color)
        self.style.configure("TLabelframe.Label", background=bg_color, foreground=text_color, font=("Segoe UI", 9, "bold"))
        
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.map("TButton",
            background=[("active", "#e1e1e1"), ("!disabled", "#f0f0f0")],
            foreground=[("!disabled", "black")]
        )
        
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#000000", background=bg_color)
        self.style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#666666", background=bg_color)
        self.style.configure("Info.TLabel", font=("Segoe UI", 11), background=bg_color)

        # UI Layout
        main_frame = ttk.Frame(root, padding=30)
        main_frame.pack(fill="both", expand=True)

        self.lbl_title = ttk.Label(main_frame, text="Converting HEIC to JPG", style="Header.TLabel")
        self.lbl_title.pack(anchor="w", pady=(0, 20))

        # "Progress 15/25"
        self.lbl_counter = ttk.Label(main_frame, text="Preparing...", style="Info.TLabel")
        self.lbl_counter.pack(anchor="w", pady=(0, 5))

        # "Converting IMG_1234.HEIC"
        self.lbl_current_file = ttk.Label(main_frame, text="Scanning...", style="Status.TLabel")
        self.lbl_current_file.pack(anchor="w", pady=(0, 15))

        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(fill="x", pady=(0, 10))

        # Start automatically
        self.root.after(100, self.start_thread)

    def start_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        try:
            files = scan_directory(self.directory)
            if not files:
                self.root.after(0, lambda: self.lbl_current_file.config(text="No HEIC files found."))
                self.root.after(2000, self.root.destroy)
                return

            total_files = len(files)
            self.root.after(0, lambda: self.progress.config(maximum=total_files, value=0))
            self.root.after(0, lambda: self.lbl_counter.config(text=f"Progress 0/{total_files}"))
            
            for i, f in enumerate(files):
                filename = os.path.basename(f)
                # Update UI
                self.root.after(0, lambda name=filename: self.lbl_current_file.config(text=f"Converting {name}..."))
                self.root.after(0, lambda count=i+1: self.lbl_counter.config(text=f"Progress {count}/{total_files}"))
                
                # Use interactive policy with our callback
                convert_file(f, overwrite_policy='interactive', conflict_callback=self.resolve_conflict)
                
                self.root.after(0, lambda: self.progress.step(1))
            
            self.root.after(0, lambda: self.lbl_counter.config(text="Completed"))
            self.root.after(0, lambda: self.lbl_current_file.config(text="All files converted successfully."))
            
            if self.auto_close:
                self.root.after(1000, self.root.destroy)
                
                
        except Exception as e:
            self.root.after(0, lambda: self.lbl_current_file.config(text=f"Error: {str(e)}"))

    def resolve_conflict(self, filepath):
        """
        Called by converter when a file conflict occurs.
        Must return 'overwrite', 'skip', or 'rename'.
        """
        # If we have a stored 'apply to all' decision, use it.
        # However, 'apply to all' works best if we store the ACTION.
        if self.conflict_decision_memory:
            return self.conflict_decision_memory

        # Event to wait for UI response
        event = threading.Event()
        user_response = {} # Dictionary to store result from UI thread

        def show_dialog():
            dlg = ConflictDialog(self.root, os.path.basename(filepath))
            self.root.wait_window(dlg) # This blocks the UI thread until closed, which is fine for the UI thread logic here? 
            # Wait, run_conversion is in a background thread. show_dialog is in UI thread.
            # wait_window blocks the caller (UI thread).
            
            user_response['action'] = dlg.result
            user_response['apply'] = dlg.apply_to_all
            event.set()

        self.root.after(0, show_dialog)
        event.wait()
        
        action = user_response.get('action', 'skip')
        apply = user_response.get('apply', False)
        
        if apply:
            self.conflict_decision_memory = action
            
        return action

