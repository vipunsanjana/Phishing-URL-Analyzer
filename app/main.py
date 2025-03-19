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
    connection = None
    try:
        connection = create_mysql_connection()
        queue = asyncio.Queue()

        # Retrieve URLs asynchronously (correctly awaiting)
        urls = await asyncio.to_thread(get_all_urls, connection)  # ✅ Await here
        for url in urls:
            await queue.put(url)

        # Create worker tasks
        num_workers = min(50, len(urls))  
        tasks = [asyncio.create_task(worker(connection, queue)) for _ in range(num_workers)]
        await asyncio.gather(*tasks)  

        # Fetch and send phishing report asynchronously
        report = await asyncio.to_thread(get_report_from_phishing_sites, connection)  # ✅ Await here
        send_webhook_message(report) 

        # Delete all records asynchronously
        await asyncio.to_thread(delete_all_records, connection)  # ✅ Await here

        constants.LOGGER.info("Process completed successfully.")
    except Exception as e:
        constants.LOGGER.critical(f"Critical error in main function: {e}", exc_info=True)
        send_error_message("Main Function", str(e))  # Ensure this is async
        raise Exception(f"Critical error in main function: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            constants.LOGGER.debug("Database connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
