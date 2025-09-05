#!/usr/bin/env python3
"""
BLOGIIIIII Auto-Update System
Simple script to update blog and push to GitHub
"""

import os
import subprocess
import sys
from datetime import datetime
def run_command(command, description):
    """Run a command and return success status"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Success: {description}")
            return True
        else:
            print(f"Error: {description}")
            print(f"Error details: {result.stderr}")
            return False
    except Exception as e:
        print(f"Exception: {description} - {e}")
        return False

def main():
    """Main function"""
    print("BLOGIIIIII Auto-Update System")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("index.html"):
        print("ERROR: Please run this from the blogii folder")
        return False
    
    # Step 1: Update blog content
    print("\n[1/3] Updating blog content...")
    if not run_command("python update_blog.py", "Update blog content"):
        return False
    
    # Step 2: Add files to Git
    print("\n[2/3] Adding files to Git...")
    if not run_command('"C:\\Program Files\\Git\\bin\\git.exe" add .', "Add files to Git"):
        return False
    
    # Step 3: Commit and push
    print("\n[3/3] Committing and pushing to GitHub...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Update blog - {timestamp}"
    
    # Try to commit
    commit_success = run_command(f'"C:\\Program Files\\Git\\bin\\git.exe" commit -m "{commit_message}"', "Commit changes")
    
    if not commit_success:
        print("WARNING: Nothing to commit (no changes detected)")
    else:
        print("Changes committed successfully")
    
    # Push to GitHub
    if not run_command('"C:\\Program Files\\Git\\bin\\git.exe" push origin main', "Push to GitHub"):
        print("ERROR: Failed to push to GitHub")
        print("Please check your internet connection and GitHub repository settings")
        return False
    
    print("\n" + "=" * 40)
    print("UPDATE COMPLETE!")
    print("=" * 40)
    print("\nYour blog has been updated and uploaded to GitHub!")
    print("It will be live at: https://A1motoro.github.io")
    print("\nChanges should be visible in 2-5 minutes.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nUpdate failed. Check the errors above.")
        sys.exit(1)
    
    print("\nPress Enter to exit...")
    input()
