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
    print("Error: SECTORFILE_PATH or REPO_PATH is not set in .env file.")
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
        os.makedirs(os.path.dirname(repo_file_path), exist_ok=True)  # Ensure directory exists
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

    print("\n🔹 **Enter the filenames you modified (one per line). Type 'done' when finished:**")

    while True:
        filename = input("> ")
        if filename.lower() == "done":
            break
        
        repo_file_path = copy_file_to_repo(filename)

        if repo_file_path:
            modified_files.append(filename)

    if not modified_files:
        print("No valid files entered. Exiting...")
        return

    # Stage files one by one with commit messages
    for file in modified_files:
        commit_message = input(f" Enter commit message for '{file}': ")
        subprocess.run(["git", "add", file], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

    # Push all committed changes
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("\n Changes successfully pushed to GitHub!")

def add_new_file():
    """Manually add a new file to the repo."""
    os.chdir(REPO_PATH)

    filename = input("\n🔹 Enter the name of the new file you want to add: ")
    file_path = os.path.join(REPO_PATH, filename)

    # Create the file
    with open(file_path, "w") as new_file:
        new_file.write("")  # Empty file
    print(f"Created new file: {file_path}")

    # Pull latest changes first to avoid conflicts
    print(" Pulling latest changes from GitHub...")
    subprocess.run(["git", "pull", "--rebase"], check=True)

    # Commit and push
    commit_message = input(f"Enter commit message for '{filename}': ")
    subprocess.run(["git", "add", filename], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("\n New file successfully pushed to GitHub!")

    """Manually add a new file to the repo."""
    os.chdir(REPO_PATH)

    filename = input("\n🔹 Enter the name of the new file you want to add: ")
    file_path = os.path.join(REPO_PATH, filename)

    # Create the file
    with open(file_path, "w") as new_file:
        new_file.write("")  # Empty file
    print(f" Created new file: {file_path}")

    # Commit and push
    commit_message = input(f" Enter commit message for '{filename}': ")
    subprocess.run(["git", "add", filename], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("\nNew file successfully pushed to GitHub!")

if __name__ == "__main__":
    print("\nChoose an option:")
    print("1 Commit & push modified files")
    print("2 Add a new file and push it to the repo")

    choice = input("\nEnter 1 or 2: ")

    if choice == "1":
        manual_commit()
    elif choice == "2":
        add_new_file()
    else:
        print(" Invalid choice. Exiting...")
