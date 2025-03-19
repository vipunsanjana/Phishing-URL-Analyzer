import asyncio
from app.utils.process_url import process_url

async def worker(connection, queue: asyncio.Queue):
    """Worker function to process URLs from the queue."""
    while not queue.empty():
        url = await queue.get()
        await process_url(connection, url)
        queue.task_done()
        