# HEIC to JPG Converter

A robust, standalone Windows utility to convert `.heic` files to `.jpg`.

## Features
*   **Dual Mode:**
    *   **GUI:** Launch without arguments (double-click) to open the user interface.
    *   **Context Menu:** Right-click any folder and select "Convert HEIC to JPG" to process it immediately.
*   **Robust Conversion:**
    *   Handles **Unicode** file paths (Chinese, Korean, emoji, etc.).
    *   Handles paths with **Spaces**.
    *   Skips corrupt files without crashing.
*   **Standalone:** No Python required on the target machine (after building).

## How to Install (End User)

### Option A: Download from GitHub (Recommended)
1.  Go to the **Actions** tab in this repository.
2.  Click on the latest "Build Windows Executable" run.
3.  Scroll down to **Artifacts** and download `Windows-Binaries`.
4.  Extract the zip file.
5.  Run `install.exe` (Run as Admin).

### Option B: Build from Source
If you prefer to build it yourself:
1.  Download the `dist` folder (after building locally).
2.  Run `install.exe`.


## How to Build (Developer)

If you want to modify the code and rebuild:

1.  **Install Python 3.10+**.
2.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
3.  **Run Build Script**:
    ```powershell
    python build.py
    ```
4.  **Output**:
    The executables will be generated in the `dist/` folder.
