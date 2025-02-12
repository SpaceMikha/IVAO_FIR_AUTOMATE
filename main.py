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

def manual_commit():
    """Manually select files, search, copy, add commit messages, and push changes."""
    os.chdir(REPO_PATH)
    modified_files = []

    print("\n🔹 **Enter the filenames you modified (one per line). Type 'done' when finished:**")

    while True:
        filename = input("> ")
        if filename.lower() == "done":
            break
        
        # Search for the file in SECTORFILE_PATH
        sectorfile_path = find_file(filename)

        if sectorfile_path:
            repo_file_path = os.path.join(REPO_PATH, filename)
            os.makedirs(os.path.dirname(repo_file_path), exist_ok=True)  # Ensure directory exists
            shutil.copy2(sectorfile_path, repo_file_path)  # Copy file to repo
            modified_files.append(filename)
            print(f"✅ Copied: {sectorfile_path} → {repo_file_path}")
        else:
            print(f"⚠️ Warning: '{filename}' not found in {SECTORFILE_PATH}.")

    if not modified_files:
        print("No valid files entered. Exiting...")
        return

    # Stage files one by one with commit messages
    for file in modified_files:
        commit_message = input(f"💬 Enter commit message for '{file}': ")
        subprocess.run(["git", "add", file], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

    # Push all committed changes
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("\n✅ Changes successfully pushed to GitHub!")

if __name__ == "__main__":
    manual_commit()
