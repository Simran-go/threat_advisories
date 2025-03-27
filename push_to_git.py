import os
import json
import time
import subprocess

# GitHub Repository URL
GITHUB_REPO_URL = "https://github.com/Simran-go/threat_advisories.git"

# File containing IOCs
JSON_FILENAME = "iocs.json"

# Commit message
COMMIT_MESSAGE = "Updated IOCs data"

def initialize_repo():
    """Initialize or load the local Git repository."""
    if not os.path.exists(".git"):  # Check if repo is initialized
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO_URL], check=True)
        print("Initialized new Git repository.")
    else:
        print("Repository already initialized.")

def create_json_file():
    """Create the JSON file if it doesn't exist."""
    if not os.path.exists(JSON_FILENAME):
        with open(JSON_FILENAME, "w") as f:
            json.dump([], f, indent=4)
        print(f"Created {JSON_FILENAME} with an empty list.")

def add_and_push_json():
    """Add the JSON file to Git, commit changes, and push to GitHub."""
    try:
        # Stage all changes, including deletions and untracked files
        subprocess.run(["git", "add", "-A"], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)

        # Pull latest changes with rebase
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)

        # Push changes to the remote repository
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print(f"Pushed {JSON_FILENAME} to GitHub.")
    except subprocess.CalledProcessError as e:
        print("Git command failed:", e)

def monitor_changes():
    """Monitor the JSON file and push updates when changes are detected."""
    last_modified_time = os.path.getmtime(JSON_FILENAME)

    while True:
        time.sleep(10)  # Check every 10 seconds
        new_modified_time = os.path.getmtime(JSON_FILENAME)

        if new_modified_time != last_modified_time:  # File modification time change indicates update
            print("Detected changes in JSON file. Updating GitHub...")
            add_and_push_json()
            last_modified_time = new_modified_time

if __name__ == "__main__":
    initialize_repo()
    create_json_file()
    add_and_push_json()
    print("Monitoring JSON file for changes...")
    monitor_changes()