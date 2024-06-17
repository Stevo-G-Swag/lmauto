import shelve
import threading
from contextlib import contextmanager


class ExternalMemory:
    def __init__(self, filename="memory_db"):
        self.filename = filename
        self.lock = threading.Lock()

    @contextmanager
    def shelve_open(self):
        with self.lock:
            with shelve.open(self.filename, writeback=True) as shelf:
                yield shelf

    def save_data(self, key, data):
        try:
            with self.shelve_open() as shelf:
                shelf[key] = data
                shelf.sync()  # Ensure data is written
            print(f"Data saved under key: {key}")
        except Exception as e:
            print(f"Failed to save data: {str(e)}")
            raise

    def retrieve_data(self, key):
        try:
            with self.shelve_open() as shelf:
                data = shelf.get(key, None)
            print(f"Data retrieved for key: {key}")
            return data
        except Exception as e:
            print(f"Failed to retrieve data: {str(e)}")
            raise

# Example usage within the module for testing
if __name__ == "__main__":
    em = ExternalMemory()
    em.save_data("test_key", {"data": "test_value"})
    retrieved_data = em.retrieve_data("test_key")
    print(retrieved_data)