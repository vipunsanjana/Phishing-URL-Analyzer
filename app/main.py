import asyncio
from app.services.google_chat.send_message import send_webhook_message, send_error_message
from app.services.mysql_service.connection import create_mysql_connection
from app.utils import constants
from app.services.mysql_service.database import (
    delete_all_records,
    get_all_urls,
    get_report_from_phishing_sites,
)
from queue import Queue
from app.utils.worker import worker

async def main():
    connection = None
    try:
        connection = create_mysql_connection()
        queue = Queue()

        # Retrieve URLs synchronously
        urls = get_all_urls(connection)
        for url in urls:
            queue.put(url)

        # Process URLs sequentially
        await worker(connection, queue)

        # Fetch and send phishing report
        report = get_report_from_phishing_sites(connection)
        send_webhook_message(report)

        # Delete all records
        delete_all_records(connection)

        constants.LOGGER.info("Process completed successfully.")
    except Exception as e:
        constants.LOGGER.critical(f"Critical error in main function: {e}", exc_info=True)
        send_error_message("Main Function", str(e))
        raise Exception(f"Critical error in main function: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            constants.LOGGER.debug("Database connection closed.")

if __name__ == "__main__":
    asyncio.run(main())  # ✅ Properly run the async main function