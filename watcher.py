import time
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InboxHandler(FileSystemEventHandler):
    """
    Handles file system events in the Inbox folder.
    """
    
    def __init__(self, vault_manager, ai_client):
        """
        Initialize the handler with vault manager and AI client.
        
        Args:
            vault_manager: Instance of VaultManager
            ai_client: Instance of AI client (ai_client module)
        """
        self.vault_manager = vault_manager
        self.ai_client = ai_client
    
    def on_created(self, event):
        """
        Handle file creation events in the monitored directory.
        
        Args:
            event: The file system event
        """
        if not event.is_directory and event.src_path.endswith('.md'):
            logger.info(f"New .md file detected: {event.src_path}")
            self.process_new_file(event.src_path)
    
    def on_moved(self, event):
        """
        Handle file move events in the monitored directory.
        
        Args:
            event: The file system event
        """
        if not event.is_directory and event.dest_path.endswith('.md'):
            logger.info(f"File moved to Inbox: {event.dest_path}")
            self.process_new_file(event.dest_path)
    
    def process_new_file(self, file_path):
        """
        Process a new file by sending it to AI for classification and summary,
        then moving it to the appropriate folder and updating the dashboard.
        
        Args:
            file_path (str): Path to the new file to process
        """
        try:
            # Wait a moment to ensure the file is fully written
            time.sleep(1)
            
            # Read the content of the new file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"Processing file: {os.path.basename(file_path)}")
            
            # Use AI to classify and summarize the content
            classification, summary = self.ai_client.classify_and_summarize(content)
            
            logger.info(f"File classified as: {classification}")
            logger.info(f"Summary: {summary}")
            
            # Move the file to the appropriate folder based on classification
            new_file_path = self.vault_manager.move_file(file_path, classification)
            
            # Append the summary to the dashboard
            self.vault_manager.append_to_dashboard(os.path.basename(file_path), summary)
            
            logger.info(f"Completed processing: {os.path.basename(file_path)}")
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")


class VaultWatcher:
    """
    Watches the Obsidian vault's Inbox folder for new .md files.
    """
    
    def __init__(self, vault_path, vault_manager, ai_client):
        """
        Initialize the watcher with the vault path.
        
        Args:
            vault_path (str): Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.inbox_path = self.vault_path / "Inbox"
        self.observer = Observer()
        self.vault_manager = vault_manager
        self.ai_client = ai_client
    
    def start_watching(self):
        """
        Start watching the Inbox folder for new files.
        """
        # Create event handler
        event_handler = InboxHandler(self.vault_manager, self.ai_client)
        
        # Schedule observer to watch the Inbox folder
        self.observer.schedule(event_handler, str(self.inbox_path), recursive=False)
        
        # Start the observer
        self.observer.start()
        logger.info(f"Started watching {self.inbox_path} for new .md files...")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            # Stop the observer when interrupted
            self.observer.stop()
            logger.info("Stopped watching for new files.")
        
        # Wait for the observer to finish
        self.observer.join()