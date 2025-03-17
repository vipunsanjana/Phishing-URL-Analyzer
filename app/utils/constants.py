import logging
import time

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

# Path to save the screenshot
screenshot_path = 'static/screenshot-' + str(time.time()) + '.png'

# GPT-4o model parameters
chunk_size=1000
overlap=200

# Maximum token limit for OpenAI API
max_token_limit = 127000 

# web page content types
VALID_CONTENT_TYPES = {
    "application/json",
}