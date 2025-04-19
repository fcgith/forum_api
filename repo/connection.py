from typing import Any
import mariadb
from mariadb import Cursor, Connection

def get_db() -> Connection | None:
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
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        raise

def read_query(query, params=()):
    """
    Executes a SQL query against the provided database connection and returns the
    fetched results or None if no data is found.
    """
    try:
        db = get_db()
        if db:
            cursor = db.cursor()
            cursor.execute(query, params)
            return cursor
    except mariadb.Error as e:
        print(f"Error executing read query: {e}")
        raise

def insert_query(query, params=()) -> int | None:
    """
    Executes an insert SQL query and commits the transaction to the database. Returns the
    ID of the inserted row.
    """
    try:
        db = get_db()
        if db:
            cursor = db.cursor()
            cursor.execute(query, params)
            db.commit()
            return cursor.lastrowid
    except mariadb.Error as e:
        print(f"Error executing insert query: {e}")
        raise

def update_query(query, params=(),) -> Any | None:
    """
    Executes an update query on the database with given parameters and commits the transaction.

    The function takes a SQL query string, optional parameters to be bound to the query,
    and a database connection object. It executes the query and commits the changes to
    the database. The function then returns the number of rows affected by the query.
    """
    try:
        db = get_db()
        if db:
            cursor = db.cursor()
            cursor.execute(query, params)
            db.commit()
            return cursor.rowcount
    except mariadb.Error as e:
        print(f"Error executing update query: {e}")
        raise