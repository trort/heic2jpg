# Project To-Do List

Based on `design_doc.md`.

- [ ] **Phase 1: Environment & Dependencies**
    - [ ] Create virtual environment
    - [ ] Install dependencies: `Pillow`, `pillow-heif`, `tkinter` (std lib), `PyInstaller`
    - [ ] Create `requirements.txt`

- [ ] **Phase 2: Core Logic Development**
    - [ ] Implement `scan_directory(path)` function
    - [ ] Implement `convert_heic_to_jpg(file_path)` function
        - Include RGBA -> RGB conversion
    - [ ] Add error handling (try/except) for corrupt files
    - [ ] Add simple logging/print statements

- [ ] **Phase 3: Interface Implementation**
    - [ ] Implement logic to detect CLI arguments vs GUI launch
    - [ ] **Branch A (CLI/Context Menu):**
        - [ ] Execute conversion on provided folder path
        - [ ] (Optional) Show progress bar/console
    - [ ] **Branch B (GUI):**
        - [ ] Create Tkinter window
        - [ ] Add "Select Folder" button
        - [ ] Add "Start" button
        - [ ] Show completion message

- [ ] **Phase 4: Packaging**
    - [ ] Create PyInstaller spec/command
    - [ ] Ensure `pillow-heif` binaries are included
    - [ ] Build `--onefile` executable

- [ ] **Phase 5: System Integration**
    - [ ] Create `.reg` file for Windows Context Menu integration

- [ ] **Phase 6: Testing**
    - [ ] Test with paths containing spaces
    - [ ] Test with duplicate filenames
    - [ ] Test with large batch of images
