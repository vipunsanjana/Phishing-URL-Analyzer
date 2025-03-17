import asyncio
from app.utils import constants
from app.utils.process_url import process_url

async def worker(connection, queue: asyncio.Queue):
    """Worker function to process URLs from the queue."""
    while not queue.empty():
        url = await queue.get()
        try:
            await process_url(connection, url)
        except Exception as e:
            constants.LOGGER.error(f"Error processing URL {url}: {e}",exc_info=True)
        queue.task_done()
        