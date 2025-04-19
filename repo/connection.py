from contextlib import contextmanager
from typing import Any, Generator
import mariadb
from mariadb import Connection

from services.errors import internal_error

@contextmanager
def get_db() -> Generator[Connection, None, None]:
    """
    Establish a connection to the MariaDB database and ensure it closes after use.
    :yield: Active database connection object.
    """
    conn = None
    try:
        conn = mariadb.connect(
            host="172.245.56.116",
            port=3600,
            user="root",
            password="root",
            database="forum"
        )
        yield conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        raise internal_error
    finally:
        if conn:
            conn.close()

def read_query(query, params=()):
    """
    Executes a SQL query against the provided database connection and returns the
    fetched results or None if no data is found.
    """
    try:
        with get_db() as db:
            if db:
                cursor = db.cursor()
                cursor.execute(query, params)
                return cursor
    except Exception as e:
        print(f"Error executing read query: {e}")
        raise internal_error

def insert_query(query, params=()) -> int | None:
    """
    Executes an insert SQL query and commits the transaction to the database. Returns the
    ID of the inserted row.
    """
    try:
        with get_db() as db:
            if db:
                cursor = db.cursor()
                cursor.execute(query, params)
                db.commit()
                return cursor.lastrowid
    except Exception as e:
        print(f"Error executing insert query: {e}")
        raise internal_error

def update_query(query, params=(),) -> Any | None:
    """
    Executes an update query on the database with given parameters and commits the transaction.

    The function takes a SQL query string, optional parameters to be bound to the query,
    and a database connection object. It executes the query and commits the changes to
    the database. The function then returns the number of rows affected by the query.
    """
    try:
        with get_db() as db:
            if db:
                cursor = db.cursor()
                cursor.execute(query, params)
                db.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error executing update query: {e}")
        raise internal_error