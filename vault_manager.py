import os
import shutil
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VaultManager:
    """
    Manages the Obsidian vault operations including file movement and dashboard updates.
    """
    
    def __init__(self, vault_path):
        """
        Initialize the VaultManager with the vault path.
        
        Args:
            vault_path (str): Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.inbox_path = self.vault_path / "Inbox"
        self.needs_action_path = self.vault_path / "Needs_Action"
        self.done_path = self.vault_path / "Done"
        self.dashboard_path = self.vault_path / "Dashboard.md"
        
        # Ensure directories exist
        self.inbox_path.mkdir(exist_ok=True)
        self.needs_action_path.mkdir(exist_ok=True)
        self.done_path.mkdir(exist_ok=True)
        
        # Ensure dashboard exists
        if not self.dashboard_path.exists():
            self.dashboard_path.touch()
            self.dashboard_path.write_text("# Dashboard\n\n## Summary of Processed Files\n\nThis dashboard contains summaries of files processed by the AI automation system.\n")
    
    def move_file(self, file_path, destination):
        """
        Move a file to the specified destination folder.
        
        Args:
            file_path (str): Path to the file to move
            destination (str): Destination folder ('Needs_Action' or 'Done')
        """
        source_path = Path(file_path)
        
        if destination == "Needs_Action":
            dest_folder = self.needs_action_path
        elif destination == "Done":
            dest_folder = self.done_path
        else:
            raise ValueError(f"Invalid destination: {destination}. Must be 'Needs_Action' or 'Done'")
        
        # Move the file to the destination folder
        dest_path = dest_folder / source_path.name
        shutil.move(str(source_path), str(dest_path))
        
        logger.info(f"Moved {source_path.name} to {dest_folder.name} folder")
        return str(dest_path)
    
    def append_to_dashboard(self, filename, summary):
        """
        Append a summary to the Dashboard.md file.
        
        Args:
            filename (str): Name of the processed file
            summary (str): Summary of the file content
        """
        dashboard_content = self.dashboard_path.read_text(encoding='utf-8')
        
        # Create the entry to add to the dashboard
        entry = f"\n### {filename}\n{summary}\n"
        
        # Append the entry to the dashboard
        updated_content = dashboard_content + entry
        self.dashboard_path.write_text(updated_content, encoding='utf-8')
        
        logger.info(f"Added summary for {filename} to Dashboard.md")
    
    def get_inbox_files(self):
        """
        Get a list of all .md files in the Inbox folder.
        
        Returns:
            list: List of paths to .md files in the Inbox
        """
        inbox_files = []
        for file_path in self.inbox_path.glob("*.md"):
            inbox_files.append(str(file_path))
        return inbox_files