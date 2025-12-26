### Project: Windows HEIC-to-JPG Converter

**Objective:** Create a standalone Windows utility that converts all `.heic` files in a target directory to `.jpg` format using the Windows Context Menu (Right-Click) or a manual folder selection.

---

### Phase 1: Environment & Dependencies

**Goal:** Prepare the development environment.

1. **Python Installation:** Ensure a modern version of Python (3.10+) is installed.
2. **Library Selection:**
* **Image Processing:** `Pillow` (The standard Python imaging library).
* **HEIC Support:** `pillow-heif` (An add-on that allows Pillow to read High Efficiency Image files).
* **GUI Framework:** `tkinter` (Built-in to Python, lightweight, no extra install required).
* **Packaging:** `PyInstaller` (To convert the Python script into a standalone `.exe` file).



### Phase 2: Core Logic Development (The Engine)

**Goal:** Create the script that actually modifies the files.

1. **File Discovery:** Write a function that accepts a `directory_path` and scans it for files ending in `.heic` (case-insensitive).
2. **Conversion Function:**
* Load the HEIC file.
* Convert color mode from RGBA (if transparency exists) to RGB (required for JPG).
* Save the file as `.jpg` in the same folder (or a subfolder called "Converted").


3. **Error Handling:** Add "Try/Except" blocks to ensure one corrupt file doesn't crash the whole process.
4. **Logging:** Implement a simple counter (e.g., "Converted 5 of 10...") to track progress.

### Phase 3: Interface Implementation (Dual-Mode)

**Goal:** Handle how the user triggers the tool.

1. **Argument Detection:**
* The script must check: *"Did the user provide a folder path when they launched me?"*


2. **Branch A: The "Right-Click" Mode (Headless/Progress Bar)**
* If a folder path **is** detected (passed from the Windows Right-Click), skip the main menu.
* Immediately run the conversion on that folder.
* *Optional:* Show a simple progress bar or a console window so the user knows it is working.


3. **Branch B: The "Standalone" Mode (GUI)**
* If **no** folder path is detected (user double-clicked the exe), open a GUI window.
* Create a "Select Folder" button.
* Create a "Start Conversion" button.
* Display a "Done" message upon completion.



### Phase 4: Packaging (Creating the Executable)

**Goal:** Detach the tool from the Python environment so it can run on any Windows machine.

1. **PyInstaller Configuration:**
* Configure the build to bundle all dependencies (`pillow-heif` is sometimes tricky here, so we will need to ensure the binaries are included).
* Build as a **Single File** (`--onefile`) for easy portability.


2. **Icon Setup (Optional):** Select an `.ico` file to make the tool look professional in the menu.

### Phase 5: System Integration (The Right-Click Menu)

**Goal:** Add the entry to the Windows Registry.

1. **Registry Structure:** Plan the registry keys needed in `HKEY_CLASSES_ROOT\Directory\shell`.
* **Key Name:** `Convert HEIC to JPG` (This is what you see in the menu).
* **Command:** The path to your new `.exe` followed by `"%1"` (This is the placeholder variable for the folder you clicked on).


2. **Registration Script:** Instead of editing the registry manually every time, we will write a `.reg` file (text file) that automates this.

### Phase 6: Testing & Quality Assurance

**Goal:** Ensure reliability.

1. **The "Space" Test:** Test on a folder path that has spaces in the name (e.g., `C:\Users\My Photos`). This is the #1 point of failure for right-click tools.
2. **The "Duplicate" Test:** Decide what happens if `image.jpg` already exists. (Skip? Overwrite? Rename to `image_copy.jpg`?).
3. **The "Large Batch" Test:** Run against a folder with 50+ images to check for memory leaks or crashes.

---

**Next Step:**
Are you ready to begin **Phase 1 and 2** (Setting up the environment and writing the core conversion logic)? I will provide the Python code for that.