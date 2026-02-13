# AI-Powered Obsidian Vault Automation

This project creates an automated Obsidian vault system that uses AI to classify and process markdown files.

## Prerequisites

- Python 3.7 or higher
- Qwen CLI (for actual AI functionality)

## Setup Instructions

1. Clone or download this repository to your local machine.

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Make sure you have Qwen CLI installed and accessible from your command line.

## Configuration

The system expects the following folder structure:
```
Obsidian_Vault/
    Dashboard.md
    Company_Handbook.md
    Inbox/
    Needs_Action/
    Done/
```

This structure is created automatically when you run the main script.

## Usage

To start the automation system:

```
python main.py --vault-path ./Obsidian_Vault
```

The system will:
1. Process any existing files in the Inbox folder
2. Start monitoring the Inbox folder for new .md files
3. For each new file:
   - Send the content to Qwen for classification and summarization
   - Move the file to either "Needs_Action" or "Done" folder based on AI classification
   - Add a summary of the file to Dashboard.md

## How It Works

1. **File Monitoring**: The system uses the watchdog library to monitor the Inbox folder for new .md files.

2. **AI Processing**: When a new file is detected, the content is sent to Qwen CLI with a prompt asking it to:
   - Classify the file as "Needs_Action" or "Done"
   - Generate a 2-3 line summary

3. **File Management**: Based on the AI's classification, the file is moved to the appropriate folder.

4. **Dashboard Updates**: A summary of each processed file is appended to Dashboard.md.

## Example Workflow

1. Place a new .md file in the Inbox folder
2. The system detects the new file
3. The file content is sent to Qwen for analysis
4. Qwen responds with a classification and summary
5. The file is moved to the appropriate folder
6. The summary is added to Dashboard.md

## Customization

You can customize the system by modifying:
- The prompts in `ai_client.py` to change how Qwen analyzes the content
- The folder structure in `vault_manager.py` to suit your needs
- The processing logic in `watcher.py` to add additional functionality

## Troubleshooting

- If the system doesn't detect new files, ensure the watchdog library is properly installed
- If Qwen CLI is not recognized, ensure it's installed and in your system PATH
- Check the logs for any error messages if files aren't being processed correctly