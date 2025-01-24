import os

def print_directory_structure(root_dir, ignore_dirs=None, ignore_files=None):
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []

    for root, dirs, files in os.walk(root_dir):
        # Remove ignored directories from traversal
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        # Print the current directory
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}Directory: {os.path.basename(root)}")

        # Print files in the current directory
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            if file not in ignore_files:
                print(f"{sub_indent}File: {file}")

# Usage example
root_directory = os.getcwd()  # Adjust the directory path as needed
ignored_directories = ['venv', '__pycache__', '.git', '.ipynb_checkpoints']
ignored_files = []  # Add specific files to ignore if needed

print_directory_structure(root_directory, ignored_directories, ignored_files)
