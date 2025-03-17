import json
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread
from app.utils import config, constants

def initialize_google_sheets():
    """
    Initializes the Google Sheets client with the service account credentials.

    Returns:
        gspread.models.Worksheet: The first sheet of the Google Spreadsheet.
    
    Raises:
        Exception: If there is an error during initialization.
    """
    try:
        sheet_id = config.SHEET_ID
        # Create credentials object
        credentials = Credentials.from_service_account_info(config.google_creds, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        # Initialize the Google Sheets client
        client = gspread.authorize(credentials)
        # Open the spreadsheet by ID
        workbook = client.open_by_key(sheet_id)
        sheet = workbook.sheet1 
        constants.LOGGER.info("Google Sheets initialized successfully")
        return sheet
    except Exception as e:
        raise Exception(f"Error initializing Google Sheets: {e}")

def add_data_to_sheet(url: str, extracted_data: dict):
    """
    Adds extracted data to the Google Sheet.

    Args:
        url (str): The URL associated with the data entry.
        extracted_data (dict): The extracted data containing 'gpt_response' and 'downloadable_screenshot_path'.

    Raises:
        json.JSONDecodeError: If the extracted data cannot be parsed into JSON format.
        Exception: If there is an error while adding data to the sheet.
    """

    res = extracted_data.get("gpt_response")
    screen_shot_url = extracted_data.get("downloadable_screenshot_path")

    try:
        sheet = initialize_google_sheets()

        # Flatten the response data dictionary
        response_data_flat = []

        for key, value in res.items():
            if isinstance(value, (dict, list)):
                response_data_flat.append(json.dumps(value)) 
            else:
                response_data_flat.append(str(value)) 

        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare the row to be appended with current date and time
        row = [url] + [screen_shot_url] + response_data_flat + [current_datetime] + [json.dumps(extracted_data, ensure_ascii=False)]

        # Get the current row count and determine where to start appending
        current_row = len(sheet.get_all_values()) + 1

        # Append the row starting from row 3
        sheet.insert_row(row, current_row)

    except json.JSONDecodeError:
        constants.LOGGER.error("Failed to parse response_data; it is not valid JSON.")
        raise Exception("Failed to parse response_data; it is not valid JSON.")
    except Exception as e:
        constants.LOGGER.error(f"Error adding data to Google Sheet: {e}")
        raise Exception(f"Error adding data to Google Sheet: {e}")
