import json
import shutil
from pathlib import Path
from datetime import datetime

def get_unique_path(path):
    if not path.exists():
        return path
    
    counter = 1
    while path.with_name(f"{path.stem}_{counter}{path.suffix}").exists():
        counter += 1
    
    return path.with_name(f"{path.stem}_{counter}{path.suffix}")

def organize_files():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found!")
        return

    source_path = Path(config['source_dir'])
    
    for item in source_path.iterdir():
        if item.is_dir(): 
            continue
            
        file_ext = item.suffix.lower()
        moved = False

        if config['archive_settings']['move_old_files_to_archive']:
            file_time = datetime.fromtimestamp(item.stat().st_mtime)
            age = datetime.now() - file_time
            
            if age.days > config['archive_settings']['days_threshold']:
                dest_folder = source_path / config['archive_settings'].get('archive_folder_name', 'Archive')
                dest_folder.mkdir(exist_ok=True)
                
                target_path = get_unique_path(dest_folder / item.name)
                shutil.move(item, target_path)
                print(f"Archived: {item.name}")
                continue 

        for folder_name, extensions in config['folders'].items():
            if file_ext in extensions:
                dest_folder = source_path / folder_name
                dest_folder.mkdir(exist_ok=True)
                
                target_path = get_unique_path(dest_folder / item.name)
                shutil.move(item, target_path)
                print(f"Moved {item.name} to {folder_name}")
                moved = True
                break

        if not moved:
            others_folder = source_path / "Others"
            others_folder.mkdir(exist_ok=True)
            target_path = get_unique_path(others_folder / item.name)
            shutil.move(item, target_path)
            print(f"Moved {item.name} to Others")

if __name__ == "__main__":
    organize_files()