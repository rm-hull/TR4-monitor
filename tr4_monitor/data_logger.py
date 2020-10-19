from datetime import datetime
import threading
import time


class DataLogger:
    def __init__(self, supplier, interval: int = 1, max_entries: int = 64):
        self.entries = []
        self.max_entries = max_entries
        self._keep_going = True
        self._thread = None
        self._interval = interval
        self._supplier = supplier

    def _capture(self):
        while (self._keep_going):
            try:
                self.entries.append(dict(timestamp=datetime.now(), value=self._supplier()))
            except:  # noqa: E722
                pass

            if len(self.entries) > self.max_entries:
                self.entries.pop(0)

            for _ in range(10):
                time.sleep(self._interval / 10)
                if not self._keep_going:
                    return

    def start(self):
        if self._thread:
            raise Exception('Data logger is already running')

        self._keep_going = True
        self._thread = threading.Thread(name='DataLogger-Thread', target=self._capture, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        if not self._thread:
            raise Exception('Data logger is not running')

        self._keep_going = False
        self._thread.join()
        self._thread = None
