
from app.services.google_chat.send_message import send_error_message
from app.services.google_sheet.sheet import add_data_to_sheet
from app.services.mysql_service.database import save_only_phishing
from app.utils import constants
from app.utils.scraper_page import scrape_website

async def process_url(connection, url: str, retries: int = 1):
    """
    Process a single URL by scraping, analyzing, and saving phishing data with retry logic.
    
    Args:
        connection: Database connection object.
        url (str): The URL to be processed.
        retries (int, optional): Number of retry attempts in case of failure. Defaults to 2.
    
    Raises:
        Exception: If all retries fail, logs the error and sends an error message.
    """
    try:
        constants.LOGGER.info(f"Processing URL: {url}")
        result = await scrape_website(url)

        if not result["gpt_response"]["Phishing"]:
            save_only_phishing(connection, result, url)
            add_data_to_sheet(url, result)
    except Exception as e:
        if retries > 0:
            constants.LOGGER.warning(f"Retrying URL {url} due to error: {e}") 
            await process_url(connection, url, retries - 1)  
        else:
            constants.LOGGER.error(f"Error processing URL {url}: {e}", exc_info=True)
            send_error_message(url, str(e))
