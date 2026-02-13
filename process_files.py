#!/usr/bin/env python3
"""
Test script to process existing files without starting the file watcher.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_client import classify_and_summarize
from vault_manager import VaultManager


def process_existing_files(vault_manager):
    """
    Process any existing files in the Inbox folder.
    
    Args:
        vault_manager: Instance of VaultManager
    """
    print("Checking for existing files in Inbox...")
    inbox_files = vault_manager.get_inbox_files()
    
    if inbox_files:
        print(f"Found {len(inbox_files)} existing file(s) in Inbox. Processing...")
        
        for file_path in inbox_files:
            process_single_file(file_path, vault_manager)
    else:
        print("No existing files found in Inbox.")


def process_single_file(file_path, vault_manager):
    """
    Process a single file by classifying it and moving it to the appropriate folder.
    
    Args:
        file_path (str): Path to the file to process
        vault_manager: Instance of VaultManager
    """
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Processing file: {os.path.basename(file_path)}")
        
        # Use AI to classify and summarize the content
        classification, summary = classify_and_summarize(content)
        
        print(f"Classified as: {classification}")
        print(f"Summary: {summary}")
        
        # Move the file to the appropriate folder based on classification
        new_file_path = vault_manager.move_file(file_path, classification)
        
        # Append the summary to the dashboard
        vault_manager.append_to_dashboard(os.path.basename(file_path), summary)
        
        print(f"Completed processing: {os.path.basename(file_path)}")
        
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")


def main():
    vault_path = "./Obsidian_Vault"
    vault_manager = VaultManager(Path(vault_path))
    process_existing_files(vault_manager)
    print("Finished processing all files in Inbox.")


if __name__ == "__main__":
    main()