import os
import shutil
import subprocess
import datetime
import inquirer
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
    exit(1)

def log_message(message, color=Fore.WHITE):
    """Prints a log message with a timestamp."""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(color + timestamp + " " + message)

def find_file(filename):
    """Search for the file inside SECTORFILE_PATH recursively."""
    for root, _, files in os.walk(SECTORFILE_PATH):
        if filename in files:
            return os.path.join(root, filename)
    return None

def copy_file_to_repo(filename):
    """Find and copy a file from SECTORFILE_PATH to REPO_PATH."""
    sectorfile_path = find_file(filename)

    if sectorfile_path:
        repo_file_path = os.path.join(REPO_PATH, filename)

        target_dir = os.path.dirname(repo_file_path)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)

        shutil.copy2(sectorfile_path, repo_file_path)
        log_message(f"Copied: {sectorfile_path} → {repo_file_path}", Fore.GREEN)
        return repo_file_path
    else:
        log_message(f"Warning: '{filename}' not found in {SECTORFILE_PATH}.", Fore.YELLOW)
        return None

def detect_modified_files():
    """Automatically detects modified files in the repository."""
    os.chdir(REPO_PATH)
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    
    modified_files = []
    for line in result.stdout.strip().split("\n"):
        if line:
            status, filename = line[:2], line[3:].strip()
            if status in ["M ", "A ", "??"]:  # Modified, Added, Untracked files
                modified_files.append(filename)

    return modified_files

def manual_commit():
    """Manually select a file by entering its name, then copy, commit, and push it."""
    os.chdir(REPO_PATH)

    while True:
        filename = inquirer.text(message="Enter the filename to commit (or type 'done' to finish)")
        
        if filename.lower() == "done":
            log_message("Exiting manual commit...", Fore.YELLOW)
            return

        # Find the file inside SECTORFILE_PATH
        sectorfile_path = find_file(filename)

        if not sectorfile_path:
            log_message(f"Error: File '{filename}' not found in {SECTORFILE_PATH}. Try again.", Fore.RED)
            continue

        # Copy file to repo
        repo_file_path = os.path.join(REPO_PATH, filename)
        os.makedirs(os.path.dirname(repo_file_path), exist_ok=True)
        shutil.copy2(sectorfile_path, repo_file_path)
        log_message(f"Copied: {sectorfile_path} → {repo_file_path}", Fore.GREEN)

        # Ask for commit message
        commit_message = inquirer.text(message=f"Enter commit message for '{filename}'")

        try:
            subprocess.run(["git", "add", filename], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            log_message(f"Committed '{filename}' with message: {commit_message}", Fore.GREEN)
        except subprocess.CalledProcessError:
            log_message(f"Error: Failed to commit '{filename}'. Skipping...", Fore.RED)
            continue

        # Ask if the user wants to commit another file
        another = inquirer.confirm(message="Do you want to commit another file?", default=True)
        if not another:
            break

    push_to_github()

    """Commits and pushes modified files automatically."""
    os.chdir(REPO_PATH)
    modified_files = detect_modified_files()

    if not modified_files:
        log_message("No modified files detected. Exiting...", Fore.YELLOW)
        return

    for file in modified_files:
        commit_message = inquirer.text(message=f"Enter commit message for '{file}'")
        try:
            subprocess.run(["git", "add", file], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            log_message(f"Committed '{file}' with message: {commit_message}", Fore.GREEN)
        except subprocess.CalledProcessError:
            log_message(f"Error: Failed to commit '{file}'. Skipping...", Fore.RED)
            continue

    push_to_github()

def add_new_file():
    """Allows the user to create new files and push them to GitHub."""
    os.chdir(REPO_PATH)
    
    files_to_add = []
    while True:
        filename = inquirer.text(message="Enter the name of the new file (or type 'done' to finish)")
        if filename.lower() == "done":
            break
        file_path = os.path.join(REPO_PATH, filename)

        with open(file_path, "w") as new_file:
            new_file.write("")
        log_message(f"Created new file: {file_path}", Fore.GREEN)

        files_to_add.append(filename)

    if not files_to_add:
        log_message("No files entered. Exiting...", Fore.RED)
        return

    try:
        log_message("Pulling latest changes from GitHub...", Fore.YELLOW)
        subprocess.run(["git", "pull", "--rebase"], check=True)
    except subprocess.CalledProcessError:
        log_message("Warning: Failed to pull latest changes. Proceeding with commit...", Fore.YELLOW)

    for filename in files_to_add:
        commit_message = inquirer.text(message=f"Enter commit message for '{filename}'")
        try:
            subprocess.run(["git", "add", filename], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            log_message(f"Committed and pushed '{filename}'", Fore.GREEN)
        except subprocess.CalledProcessError:
            log_message(f"Error: Failed to push '{filename}'. Skipping...", Fore.RED)

    push_to_github()

def get_current_git_branch():
    """Gets the current active Git branch."""
    os.chdir(REPO_PATH)
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip()

def push_to_github():
    """Pushes committed changes to GitHub with error handling."""
    branch = get_current_git_branch()
    try:
        subprocess.run(["git", "push", "origin", branch], check=True)
        log_message(f"Changes successfully pushed to GitHub on branch '{branch}'", Fore.GREEN)
    except subprocess.CalledProcessError:
        log_message("Error: Failed to push changes to GitHub. Please check your authentication.", Fore.RED)

def main_menu():
    """Interactive menu for user selection."""
    questions = [
        inquirer.List(
            "action",
            message="Choose an action",
            choices=[
                "Commit & push modified files automatically",
                "Add new file(s) and push to the repo",
                "Exit"
            ],
        )
    ]
    
    answer = inquirer.prompt(questions)["action"]
    
    if answer == "Commit & push modified files automatically":
        manual_commit()
    elif answer == "Add new file(s) and push to the repo":
        add_new_file()
    else:
        log_message("Exiting...", Fore.YELLOW)
        exit(0)

if __name__ == "__main__":
    main_menu()
