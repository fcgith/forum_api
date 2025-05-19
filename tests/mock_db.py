from unittest.mock import MagicMock
from typing import List, Tuple, Any

class MockCursor:
    def __init__(self):
        self.lastrowid = 1
        self.rowcount = 1
        self._results = []
        self._execute_calls = []

    def execute(self, query: str, params: tuple = ()) -> None:
        self._execute_calls.append((query, params))
        # You can add specific query handling here if needed
        pass

    def fetchall(self) -> List[Tuple]:
        return self._results

    def close(self) -> None:
        pass

    def set_results(self, results: List[Tuple]) -> None:
        self._results = results

    def get_execute_calls(self) -> List[Tuple[str, tuple]]:
        return self._execute_calls

class MockConnection:
    def __init__(self):
        self.cursor = MockCursor()
        self._closed = False

    def commit(self) -> None:
        pass

    def close(self) -> None:
        self._closed = True

    def is_closed(self) -> bool:
        return self._closed

class MockConnectionPool:
    def __init__(self):
        self.connections = []

    def get_connection(self) -> MockConnection:
        conn = MockConnection()
        self.connections.append(conn)
        return conn

    def close(self) -> None:
        for conn in self.connections:
            conn.close() 