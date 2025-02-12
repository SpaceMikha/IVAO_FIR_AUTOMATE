import os
import shutil
import subprocess
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()

# Get paths from .env
SECTORFILE_PATH = os.getenv("SECTORFILE_PATH")
REPO_PATH = os.getenv("REPO_PATH")

if not SECTORFILE_PATH or not REPO_PATH:
    print(Fore.RED + "Error: SECTORFILE_PATH or REPO_PATH is missing in the .env file.")
    print("Ensure the .env file contains:")
    print("  SECTORFILE_PATH=/path/to/sectorfiles")
    print("  REPO_PATH=/path/to/repo")
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

        target_dir = os.path.dirname(repo_file_path)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)

        shutil.copy2(sectorfile_path, repo_file_path)
        print(Fore.GREEN + f"Copied: {sectorfile_path} → {repo_file_path}")
        return repo_file_path
    else:
        print(Fore.YELLOW + f"Warning: '{filename}' not found in {SECTORFILE_PATH}.")
        return None

def manual_commit():
    """Manually select files, search, copy, add commit messages, and push changes."""
    os.chdir(REPO_PATH)
    modified_files = []

    print(Fore.CYAN + "\nEnter the filenames you modified (one per line). Type 'done' when finished:")

    while True:
        filename = input(Fore.BLUE + "> ").strip()
        if filename.lower() == "done":
            break

        repo_file_path = copy_file_to_repo(filename)
        if repo_file_path:
            modified_files.append(filename)

    if not modified_files:
        print(Fore.RED + "No valid files entered. Exiting...")
        return

    for file in modified_files:
        commit_message = input(Fore.MAGENTA + f"Enter commit message for '{file}': ").strip()
        try:
            subprocess.run(["git", "add", file], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print(Fore.GREEN + f"Committed '{file}' with message: {commit_message}")
        except subprocess.CalledProcessError:
            print(Fore.RED + f"Error: Failed to commit '{file}'. Skipping...")
            continue

    try:
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print(Fore.GREEN + "Changes successfully pushed to GitHub!")
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Failed to push changes to GitHub. Please check your internet connection.")

def add_new_file():
    """Manually add one or multiple new files to the repo, with individual commit messages."""
    os.chdir(REPO_PATH)
    
    files_to_add = []
    print(Fore.CYAN + "\nEnter the filenames you want to add (one per line). Type 'done' when finished:")

    while True:
        filename = input(Fore.BLUE + "> ").strip()
        if filename.lower() == "done":
            break
        file_path = os.path.join(REPO_PATH, filename)

        with open(file_path, "w") as new_file:
            new_file.write("")
        print(Fore.GREEN + f"Created new file: {file_path}")

        files_to_add.append(filename)

    if not files_to_add:
        print(Fore.RED + "No files entered. Exiting...")
        return

    try:
        print(Fore.YELLOW + "Pulling latest changes from GitHub...")
        subprocess.run(["git", "pull", "--rebase"], check=True)
    except subprocess.CalledProcessError:
        print(Fore.YELLOW + "Warning: Failed to pull latest changes. Proceeding with commit...")

    for filename in files_to_add:
        commit_message = input(Fore.MAGENTA + f"Enter commit message for '{filename}': ").strip()
        try:
            subprocess.run(["git", "add", filename], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print(Fore.GREEN + f"'{filename}' successfully pushed to GitHub!")
        except subprocess.CalledProcessError:
            print(Fore.RED + f"Error: Failed to push '{filename}'. Skipping...")

def check_git_status():
    """Check if there are any unstaged changes before proceeding."""
    try:
        status_output = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status_output.stdout.strip():
            print(Fore.GREEN + "Git working directory is clean. No changes detected.")
            return False
        return True
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to check Git status. Make sure Git is installed and configured.")
        return False

if __name__ == "__main__":
    print(Fore.CYAN + "\nChoose an option:")
    print(Fore.YELLOW + "1 Commit & push modified files")
    print(Fore.YELLOW + "2 Add new file(s) and push to the repo")

    choice = input(Fore.BLUE + "\nEnter 1 or 2: ").strip()

    if choice == "1":
        if check_git_status():
            manual_commit()
        else:
            print(Fore.YELLOW + "No modified files detected. Exiting...")
    elif choice == "2":
        add_new_file()
    else:
        print(Fore.RED + "Invalid choice. Exiting...")
