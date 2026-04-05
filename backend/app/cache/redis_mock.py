import threading
from typing import Any


class MockRedisCache:
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}
        self._lock = threading.Lock()

    def get_and_set(self, key: str, updater) -> Any:
        """
        Atomically read, transform, and write in a single lock acquisition.
        Prevents stale reads when concurrent requests check the same partner_id.
        """
        with self._lock:
            current = self._store.get(key)
            new_value = updater(current)
            self._store[key] = new_value
            return new_value


cache = MockRedisCache()
