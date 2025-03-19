import logging
import time
import uuid

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

# Generate a unique filename
timestamp = str(time.time_ns())  # Nanoseconds precision for better uniqueness
unique_id = str(uuid.uuid4().hex)  # Add a random UUID for extra uniqueness
screenshot_path = f'static/screenshot-{timestamp}-{unique_id}.png'

# Maximum token limit for OpenAI API
max_token_limit = 127500

# web page content types
VALID_CONTENT_TYPES = {
    "application/json",
}