from typing import Any, Generator
import pytest
import sqlite3
import pydiscordbot.database as db

@pytest.fixture(scope="function")
def mock_db(monkeypatch) -> Generator[Any, None, None]:
    """Fixture to set up an in-memory SQLite database for testing."""
    # 1. Create the in-memory database connection
    test_conn = sqlite3.connect(":memory:", check_same_thread=False)
    test_conn.row_factory = sqlite3.Row
    
    # 2. Patch the get_connection function to return our test connection
    monkeypatch.setattr(db, "get_connection", lambda connection=None: test_conn)
    
    # 3. Initialize the database schema on this connection (after patching)
    db.initialize_db()
    
    # 4. Yield the connection to the test
    yield test_conn
    
    # 5. Close the connection after the test is done
    test_conn.close()