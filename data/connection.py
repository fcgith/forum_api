from contextlib import contextmanager
from typing import Any, Generator, List, Tuple
import mariadb
from fastapi import Depends
from mariadb import Connection, ConnectionPool

pool = ConnectionPool(
    pool_name="forum_pool",
    pool_size=5,
    host="172.245.56.116",
    port=3600,
    user="root",
    password="root",
    database="forum"
)

def get_db() -> Connection:
    """
    Provides a database connection from the connection pool.
    Note: Connection should be closed by the caller or managed via context.
    """
    conn = None
    try:
        conn = pool.get_connection()
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB database: {e}")
        raise
    finally:
        if conn:
            conn.close()

def read_query(query: str, params: () = ()) -> List[Tuple] | None:
    """
    Executes a SQL query against the provided database connection.
    Returns the fetched results as a list of tuples or None if an error occurs.
    """
    with get_db() as db:
        cursor = None
        try:
            cursor = db.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error executing read query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

def affect_query(qtype: int, query: str, params: ()) -> int | None:
    with get_db() as db:
        cursor = None
        try:
            cursor = db.cursor()
            cursor.execute(query, params)
            db.commit()
            return cursor.lastrowid if qtype == 0 else cursor.rowcount
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

def insert_query(query: str, params: () = ()) -> int | None:
    """
    Executes an insert SQL query and commits the transaction to the database.
    Returns the ID of the inserted row.
    """
    return affect_query(0, query, params)

def update_query(query: str, params: () = ()) -> int | None:
    """
    Executes an update query on the database and commits the transaction.
    Returns the number of affected rows.
    """
    return affect_query(1, query, params)