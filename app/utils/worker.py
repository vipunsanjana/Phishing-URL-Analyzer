from queue import Queue

from app.utils.process_url import process_url

async def worker(connection, queue: Queue):
    """Worker function to process URLs from the queue."""
    while not queue.empty():
        url = queue.get()
        await process_url(connection, url)
        queue.task_done()