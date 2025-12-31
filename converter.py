import os
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIC opener with Pillow
register_heif_opener()



def scan_directory(directory_path: str, recursive: bool = True) -> list[str]:
    """
    Scans the given directory for files ending in .heic (case-insensitive).
    Returns a list of absolute file paths.
    """
    heic_files = []
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return []

    if recursive:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith(".heic"):
                    full_path = os.path.join(root, file)
                    heic_files.append(os.path.abspath(full_path))
    else:
        for file in os.listdir(directory_path):
            if file.lower().endswith(".heic"):
                full_path = os.path.join(directory_path, file)
                if os.path.isfile(full_path):
                    heic_files.append(os.path.abspath(full_path))
    
    return heic_files

def get_unique_filename(filepath: str) -> str:
    """
    Returns a unique filename by appending (1), (2), etc. if the file exists.
    """
    if not os.path.exists(filepath):
        return filepath
    
    base, ext = os.path.splitext(filepath)
    counter = 1
    while True:
        new_path = f"{base} ({counter}){ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def convert_file(file_path: str, overwrite_policy: str = 'overwrite', conflict_callback=None) -> bool:
    """
    Converts a single HEIC file to JPG.
    params:
        overwrite_policy: 'overwrite', 'skip', 'subfolder', 'interactive'
        conflict_callback: function(existing_file_path) -> 'overwrite' | 'skip' | 'rename'
    Returns True on success, False on failure or skip.
    """
    try:
        base_dir = os.path.dirname(file_path)
        base_name, _ = os.path.splitext(os.path.basename(file_path))
        
        target_dir = base_dir
        if overwrite_policy == 'subfolder':
            target_dir = os.path.join(base_dir, 'converted')
            os.makedirs(target_dir, exist_ok=True)
            
        new_path = os.path.join(target_dir, f"{base_name}.jpg")
        
        if os.path.exists(new_path):
            action = overwrite_policy
            
            if overwrite_policy == 'interactive':
                if conflict_callback:
                    action = conflict_callback(new_path)
                else:
                    # Default fallback if no callback provided
                    action = 'skip'
            elif overwrite_policy == 'subfolder':
                # Subfolder mode usually implies overwriting within that subfolder, 
                # or we could default to 'overwrite'.
                action = 'overwrite'

            if action == 'skip':
                print(f"Skipping (exists): {file_path}")
                return False
            elif action == 'rename':
                new_path = get_unique_filename(new_path)
            # elif action == 'overwrite': pass (proceed to save)
        
        # Open the image
        image = Image.open(file_path)
        
        # Always preserve EXIF if available
        exif_data = image.info.get('exif')
        
        # Convert to RGB (remove alpha channel if present)
        image = image.convert("RGB")
        
        # Save as JPG
        save_kwargs = {"quality": 95}
        if exif_data:
            save_kwargs["exif"] = exif_data
            
        image.save(new_path, "JPEG", **save_kwargs)
        print(f"Converted: {file_path} -> {new_path}")
        return True
        
    except Exception as e:
        print(f"Failed to convert {file_path}: {e}")
        return False
