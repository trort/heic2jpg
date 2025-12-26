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

1.  Download the `dist` folder.
2.  Run `install.exe` (found inside `dist`).
    *   Grant Administrator privileges when prompted.
    *   This will copy the app to your local data folder and register the right-click menu item.
3.  **Done!** Right-click any folder containing HEIC files and choose **"Convert HEIC to JPG"**.

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
