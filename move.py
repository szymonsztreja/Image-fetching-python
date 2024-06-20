import os
import shutil

def move_files_to_target(root_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            shutil.move(file_path, target_dir)
            print(f"Moved: {file_path} -> {target_dir}")

# Define your root directory and target directory
root_directory = 'movie_backdrops'
target_directory = 'all_images'

# Move files
move_files_to_target(root_directory, target_directory)
