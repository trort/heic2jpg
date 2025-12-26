import os
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIC opener with Pillow
register_heif_opener()

def scan_directory(directory_path: str) -> list[str]:
    """
    Scans the given directory for files ending in .heic (case-insensitive).
    Returns a list of absolute file paths.
    """
    heic_files = []
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return []

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(".heic"):
                full_path = os.path.join(root, file)
                heic_files.append(os.path.abspath(full_path))
    
    return heic_files

def convert_file(file_path: str) -> bool:
    """
    Converts a single HEIC file to JPG.
    Returns True on success, False on failure.
    """
    try:
        # Open the image
        image = Image.open(file_path)
        
        # Convert to RGB (remove alpha channel if present)
        image = image.convert("RGB")
        
        # Prepare new filename (replace extension)
        base, _ = os.path.splitext(file_path)
        new_path = f"{base}.jpg"
        
        # Save as JPG
        image.save(new_path, "JPEG", quality=95)
        print(f"Converted: {file_path} -> {new_path}")
        return True
        
    except Exception as e:
        print(f"Failed to convert {file_path}: {e}")
        return False
