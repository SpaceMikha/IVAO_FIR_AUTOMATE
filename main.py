import os
import shutil
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get paths from .env
SECTORFILE_PATH = os.getenv("SECTORFILE_PATH")
REPO_PATH = os.getenv("REPO_PATH")

if not SECTORFILE_PATH or not REPO_PATH:
    print(" Error: SECTORFILE_PATH or REPO_PATH is missing in the .env file.")
    print("  Ensure the .env file contains:")
    print("   SECTORFILE_PATH=/path/to/sectorfiles")
    print("   REPO_PATH=/path/to/repo")
    exit(1)

def find_file(filename):
    """Search for the file inside SECTORFILE_PATH recursively."""
    for root, _, files in os.walk(SECTORFILE_PATH):
        if filename in files:
            return os.path.join(root, filename)
    return None  # File not found

def copy_file_to_repo(filename):
    """Find and copy a file from SECTORFILE_PATH to REPO_PATH."""
    sectorfile_path = find_file(filename)

    if sectorfile_path:
        repo_file_path = os.path.join(REPO_PATH, filename)

        # Ensure the target directory exists
        target_dir = os.path.dirname(repo_file_path)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)

        shutil.copy2(sectorfile_path, repo_file_path)  # Copy file to repo
        print(f" Copied: {sectorfile_path} → {repo_file_path}")
        return repo_file_path
    else:
        print(f" Warning: '{filename}' not found in {SECTORFILE_PATH}.")
        return None

def manual_commit():
    """Manually select files, search, copy, add commit messages, and push changes."""
    os.chdir(REPO_PATH)
    modified_files = []

    print("\n Enter the filenames you modified (one per line). Type 'done' when finished:")

    while True:
        filename = input("> ").strip()
        if filename.lower() == "done":
            break

        repo_file_path = copy_file_to_repo(filename)
        if repo_file_path:
            modified_files.append(filename)

    if not modified_files:
        print(" No valid files entered. Exiting...")
        return

    # Stage and commit files individually
    for file in modified_files:
        commit_message = input(f" Enter commit message for '{file}': ").strip()
        try:
            subprocess.run(["git", "add", file], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print(f" Committed '{file}' with message: {commit_message}")
        except subprocess.CalledProcessError:
            print(f" Error: Failed to commit '{file}'. Skipping...")
            continue

    # Push all committed changes
    try:
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("\n Changes successfully pushed to GitHub!")
    except subprocess.CalledProcessError:
        print(" Error: Failed to push changes to GitHub. Please check your internet connection.")

def add_new_file():
    """Manually add one or multiple new files to the repo, with individual commit messages."""
    os.chdir(REPO_PATH)
    
    files_to_add = []
    print("\n Enter the filenames you want to add (one per line). Type 'done' when finished:")

    while True:
        filename = input("> ").strip()
        if filename.lower() == "done":
            break
        file_path = os.path.join(REPO_PATH, filename)

        # Create the file
        with open(file_path, "w") as new_file:
            new_file.write("")  # Empty file
        print(f" Created new file: {file_path}")

        files_to_add.append(filename)

    if not files_to_add:
        print(" No files entered. Exiting...")
        return

    # Pull latest changes first to avoid conflicts
    try:
        print(" Pulling latest changes from GitHub...")
        subprocess.run(["git", "pull", "--rebase"], check=True)
    except subprocess.CalledProcessError:
        print(" Warning: Failed to pull latest changes. Proceeding with commit...")

    # Commit and push each file individually
    for filename in files_to_add:
        commit_message = input(f"\n Enter commit message for '{filename}': ").strip()
        try:
            subprocess.run(["git", "add", filename], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print(f" '{filename}' successfully pushed to GitHub!")
        except subprocess.CalledProcessError:
            print(f" Error: Failed to push '{filename}'. Skipping...")

def check_git_status():
    """Check if there are any unstaged changes before proceeding."""
    try:
        status_output = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status_output.stdout.strip():
            print(" Git working directory is clean. No changes detected.")
            return False
        return True
    except subprocess.CalledProcessError:
        print(" Error: Unable to check Git status. Make sure Git is installed and configured.")
        return False

if __name__ == "__main__":
    print("\n Choose an option:")
    print("1 Commit & push modified files")
    print("2 Add new file(s) and push to the repo")

    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        if check_git_status():
            manual_commit()
        else:
            print(" No modified files detected. Exiting...")
    elif choice == "2":
        add_new_file()
    else:
        print("❌ Invalid choice. Exiting...")
