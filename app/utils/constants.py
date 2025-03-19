import logging
import time
import uuid
import hashlib

def generate_unique_filename(url: str) -> str:
    """
    Generates a unique filename based on the URL, timestamp, and UUID.

    Args:
        url (str): The URL to be hashed for uniqueness.

    Returns:
        str: A unique filename in the format 'static/screenshot-{timestamp}-{unique_id}.png'.
    """
    # Hash the URL to ensure uniqueness
    url_hash = str(hashlib.md5(url.encode()).hexdigest()[:8])  # Short hash for readability
    
    # Get the current timestamp in nanoseconds
    timestamp = str(time.time_ns())
    
    # Generate a random UUID
    unique_id = str(uuid.uuid4().hex)
    
    # Combine all parts into a unique filename
    return f'static/screenshot-{url_hash}-{timestamp}-{unique_id}.png'

logging.basicConfig(
    level=getattr(logging, "INFO", logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

# Constants of prompt template
SUPPORT_PROMPT = "\n\nPlease strictly return a well-formed JSON object in the following format. Only provide the JSON structure, no extra text, just the raw JSON. not need Please strictly return a well-formed JSON object in the following format. Only provide the JSON structure, no extra text, just the raw JSON. not need ```json ``` or any other formatting."

# Logger
LOGGER = logging.getLogger(__name__)

# OpenAI API endpoint
GPT_API = "https://api.openai.com/v1/chat/completions"

# web page content types
VALID_CONTENT_TYPE = "application/json"

# message template
REPORT_TEMPLATE = """
📊 **Analysis Summary**

1️⃣ **Content Type**  
- 🗳️ Not Political Content: {not_political}  
- 💥 Political Content: {political}  

2️⃣ **Location Relevance**  
- 🌐 Not Related to LK: {not_related_to_lk}  
- 🏝️ Related to LK: {related_to_lk}  

3️⃣ **Security Assessment**  
- 🛡️ Not Phishing Site: {not_phishing}  
- ⚠️ Phishing Site: {phishing}  

✅ **Total Sites Scanned**: {total_sites_scanned}  

🔗 [View Google Sheet]({google_sheet_url})
"""

# Maximum token limit for OpenAI API
max_token_limit = 127000 

# web page content types
VALID_CONTENT_TYPES = {
    "application/json",
}