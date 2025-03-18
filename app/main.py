import asyncio
from app.services.google_chat.send_message import send_webhook_message, send_error_message
from app.services.mysql_service.connection import create_mysql_connection
from app.utils import constants
from app.services.mysql_service.database import (
    delete_all_records,
    get_all_urls,
    get_report_from_phishing_sites,
)
from app.utils.worker import worker

async def main():
    """
    Main function to orchestrate URL scraping, analysis, and reporting.
    
    Steps:
    1. Establishes a database connection.
    2. Retrieves all URLs from the database and adds them to a queue.
    3. Spawns multiple asynchronous worker tasks to process the URLs.
    4. Gathers phishing analysis reports and sends them via webhook.
    5. Deletes all processed records from the database.
    6. Handles errors and ensures database connection closure.
    
    Raises:
        Exception: If a critical error occurs during execution.
    """
    connection = None
    try:
        connection = await create_mysql_connection()
        queue = asyncio.Queue()

        # Retrieve URLs asynchronously
        urls = await asyncio.to_thread(get_all_urls, connection)
        for url in urls:
            await queue.put(url)

        # Create worker tasks
        num_workers = min(50, len(urls))  
        tasks = [asyncio.create_task(worker(connection, queue)) for _ in range(num_workers)]

        await asyncio.gather(*tasks)  

        # Fetch and send phishing report asynchronously
        report = await asyncio.to_thread(get_report_from_phishing_sites, connection)
        await send_webhook_message(report)

        # Delete all records from the database asynchronously
        await asyncio.to_thread(delete_all_records, connection)

        constants.LOGGER.info("Process completed successfully.")
    except Exception as e:
        constants.LOGGER.critical(f"Critical error in main function: {e}", exc_info=True)
        await send_error_message("Main Function", str(e))
        raise Exception(f"Critical error in main function: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            constants.LOGGER.debug("Database connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
