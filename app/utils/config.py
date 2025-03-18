import os
from dotenv import load_dotenv
from app.utils import constants

# Load environment variables
load_dotenv(override=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Firebase Configuration
BUCKET_NAME = os.getenv("BUCKET_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# GPT Model Configuration
GPT_MODEL=os.getenv("GPT_MODEL")
TEMPERATURE=os.getenv("TEMPERATURE")

# Google Sheet URL
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

# Google Chat Webhook URL
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Database Configuration
MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST")
MYSQL_DB_USER = os.getenv("MYSQL_DB_USER")
MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD")
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")
MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT")

private_key = os.getenv("GOOGLE_SHEETS_PRIVATE_KEY")
if private_key:
    private_key = private_key.replace(r"\n", "\n")  # This will replace the literal '\n' with actual newlines

google_creds = {
    "type": os.getenv("GOOGLE_SHEETS_TYPE"),
    "project_id": os.getenv("GOOGLE_SHEETS_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_SHEETS_PRIVATE_KEY_ID"),
    "private_key": private_key,  # Use the cleaned up private_key here
    "client_email": os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_SHEETS_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_SHEETS_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_SHEETS_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_SHEETS_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_SHEETS_CLIENT_CERT_URL"),
    "universe_domain": os.getenv("GOOGLE_SHEETS_UNIVERSE_DOMAIN"),
}


# Google Sheet ID
SHEET_ID = os.getenv("SHEET_ID")

# Firebase Service Account Credentials
FIREBASE_CREDENTIALS = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"), 
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
}

# List of all required environment variables
required_vars = [
    "OPENAI_API_KEY",
    "BUCKET_NAME",
    "COLLECTION_NAME",
    "FIREBASE_TYPE",
    "FIREBASE_PROJECT_ID",
    "FIREBASE_PRIVATE_KEY_ID",
    "FIREBASE_PRIVATE_KEY",
    "FIREBASE_CLIENT_EMAIL",
    "FIREBASE_CLIENT_ID",
    "FIREBASE_AUTH_URI",
    "FIREBASE_TOKEN_URI",
    "FIREBASE_AUTH_PROVIDER_X509_CERT_URL",
    "FIREBASE_CLIENT_X509_CERT_URL",
    "FIREBASE_UNIVERSE_DOMAIN",
    "MYSQL_DB_HOST",
    "MYSQL_DB_USER",
    "MYSQL_DB_PASSWORD",
    "MYSQL_DB_NAME",
    "MYSQL_DB_PORT",
    "SHEET_ID",
    "GOOGLE_SHEETS_TYPE",
    "GOOGLE_SHEETS_PROJECT_ID",
    "GOOGLE_SHEETS_PRIVATE_KEY_ID",
    "GOOGLE_SHEETS_PRIVATE_KEY",
    "GOOGLE_SHEETS_CLIENT_EMAIL",
    "GOOGLE_SHEETS_CLIENT_ID",
    "GOOGLE_SHEETS_AUTH_URI",
    "GOOGLE_SHEETS_TOKEN_URI",
    "GOOGLE_SHEETS_AUTH_PROVIDER_CERT_URL",
    "GOOGLE_SHEETS_CLIENT_CERT_URL",
    "GOOGLE_SHEETS_UNIVERSE_DOMAIN",
    "GOOGLE_SHEET_URL",
    "WEBHOOK_URL",
    "GPT_MODEL",
    "TEMPERATURE",
]

# Check for missing environment variables
missing_vars = [var_name for var_name in required_vars if not os.getenv(var_name)]

if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )