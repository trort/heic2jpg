# Project To-Do List

Based on `design_doc.md`.

- [x] **Phase 1: Environment & Dependencies**
    - [x] Create virtual environment
    - [x] Install dependencies: `Pillow`, `pillow-heif`, `tkinter` (std lib), `PyInstaller`
    - [x] Create `requirements.txt`

- [x] **Phase 2: Core Logic Development**
    - [x] Implement `scan_directory(path)` function
    - [x] Implement `convert_heic_to_jpg(file_path)` function
        - [x] Include RGBA -> RGB conversion
    - [x] Add error handling (try/except) for corrupt files
    - [x] Add simple logging/print statements

- [x] **Phase 3: Interface Implementation**
    - [x] Implement logic to detect CLI arguments vs GUI launch
    - [x] **Branch A (CLI/Context Menu):**
        - [x] Execute conversion on provided folder path
        - [x] (Optional) Show progress bar/console
    - [x] **Branch B (GUI):**
        - [x] Create Tkinter window
        - [x] Add "Select Folder" button
        - [x] Add "Start" button
        - [x] Show completion message

- [x] **Phase 4: Packaging**
    - [x] Create PyInstaller spec/command
    - [x] Ensure `pillow-heif` binaries are included
    - [x] Build `--onefile` executable

- [x] **Phase 5: System Integration (Installer)**
    - [x] Create `install.py` using `winreg` and `ctypes` (for admin elevation)
    - [x] Build `install.exe` that sets up registry keys automatically

- [x] **Phase 6: Testing**
    - [x] Test with paths containing spaces
    - [x] Test with duplicate filenames
    - [x] Test with large batch of images
    - [x] Test with non-English (Unicode) characters

- [x] **Phase 7: Distribution (CI/CD)**
    - [x] Create `.github/workflows/build.yml`
    - [x] Automate Windows binary build and upload

- [x] **Phase 8: UI Polish & Icons**
    - [x] Remove background from icons and convert to `.ico`
    - [x] Upgrade GUI to modern Windows style (ttk/ttkbootstrap)
    - [x] Implement "Progress Only" GUI mode for Right-Click
    - [x] Update build to use icons and hide console
