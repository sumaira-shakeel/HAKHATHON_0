import subprocess
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_qwen_cli(prompt):
    """
    Call the Qwen CLI with the given prompt and return the response.
    
    Args:
        prompt (str): The prompt to send to Qwen
        
    Returns:
        str: The response from Qwen
    """
    try:
        # Prepare the command to call Qwen CLI
        # Using a mock response for demonstration since Qwen CLI might not be available
        # In a real scenario, this would be: subprocess.run(['qwen-cli', '--prompt', prompt], ...)
        
        # For this implementation, we'll simulate the Qwen response
        # In a real scenario, you would use the actual Qwen CLI command
        logger.info(f"Sending prompt to Qwen: {prompt[:50]}...")
        
        # Mock response - in real implementation, replace with actual CLI call
        # cmd = ['qwen-cli', '--prompt', prompt]
        # result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # For now, returning a simulated response based on the content
        # This is a placeholder - actual implementation would call Qwen CLI
        if "urgent" in prompt.lower() or "action" in prompt.lower():
            classification = "Needs_Action"
            summary = "This file requires immediate attention and action."
        else:
            classification = "Done"
            summary = "This file has been reviewed and can be archived."
            
        return f"Classification: {classification}\nSummary: {summary}"
        
    except subprocess.TimeoutExpired:
        logger.error("Qwen CLI call timed out")
        return "Error: Timeout"
    except Exception as e:
        logger.error(f"Error calling Qwen CLI: {str(e)}")
        return f"Error: {str(e)}"

def classify_and_summarize(content):
    """
    Ask Qwen to classify the content and generate a summary.
    
    Args:
        content (str): The content of the file to classify and summarize
        
    Returns:
        tuple: (classification, summary)
    """
    prompt = f"""
    Analyze the following content and provide:
    1. Classification: Determine if this should be categorized as "Needs_Action" or "Done"
       - Needs_Action: If the content requires follow-up, action, or processing
       - Done: If the content is informational, completed, or doesn't require action
    2. Summary: Generate a 2-3 line summary of the content
    
    Content:
    {content}
    
    Format your response as:
    Classification: [Needs_Action or Done]
    Summary: [2-3 line summary here]
    """
    
    response = call_qwen_cli(prompt)
    
    # Parse the response to extract classification and summary
    classification = "Done"  # Default
    summary = "No summary generated."  # Default
    
    lines = response.split('\n')
    for line in lines:
        if line.startswith('Classification:'):
            classification = line.replace('Classification:', '').strip()
        elif line.startswith('Summary:'):
            summary = line.replace('Summary:', '').strip()
    
    return classification, summary