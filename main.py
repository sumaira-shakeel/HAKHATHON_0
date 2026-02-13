#!/usr/bin/env python3
"""
AI-Powered Obsidian Vault Automation System

This script creates an automated Obsidian vault system that:
- Monitors the Inbox folder for new .md files
- Uses AI to classify files as "Needs_Action" or "Done"
- Generates summaries of file content
- Moves files to appropriate folders
- Updates the dashboard with file summaries
"""

import sys
import os
import argparse
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_client import classify_and_summarize
from vault_manager import VaultManager
from watcher import VaultWatcher


def main():
    """
    Main entry point for the Obsidian Vault Automation system.
    """
    parser = argparse.ArgumentParser(description="AI-Powered Obsidian Vault Automation")
    parser.add_argument(
        "--vault-path", 
        type=str, 
        default="./Obsidian_Vault", 
        help="Path to the Obsidian vault (default: ./Obsidian_Vault)"
    )
    
    args = parser.parse_args()
    
    # Validate vault path
    vault_path = Path(args.vault_path)
    if not vault_path.exists():
        print(f"Error: Vault path '{args.vault_path}' does not exist.")
        sys.exit(1)
    
    print(f"Starting AI-Powered Obsidian Vault Automation...")
    print(f"Vault path: {vault_path.absolute()}")
    
    # Initialize components
    vault_manager = VaultManager(vault_path)
    
    # Create a module-like object to pass to the watcher
    class ai_client_module:
        """Mock module to hold the classify_and_summarize function"""
        classify_and_summarize = staticmethod(classify_and_summarize)
    
    watcher = VaultWatcher(vault_path, vault_manager, ai_client_module)
    
    # Process any existing files in the Inbox before starting the watcher
    process_existing_files(vault_manager)
    
    # Start watching for new files
    try:
        watcher.start_watching()
    except KeyboardInterrupt:
        print("\nShutting down the Obsidian Vault Automation system...")
        sys.exit(0)


def process_existing_files(vault_manager):
    """
    Process any existing files in the Inbox folder before starting the watcher.
    
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


if __name__ == "__main__":
    main()