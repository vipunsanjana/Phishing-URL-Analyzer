from queue import Queue

from app.utils import process_url

def worker(connection, queue: Queue):
    """Worker function to process URLs from the queue."""
    while not queue.empty():
        url = queue.get()
        process_url(connection, url)
        queue.task_done()