from contextlib import contextmanager

import mariadb


@contextmanager
def get_db():
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
        print(f"Error connecting to database: {e}")
        raise
    finally:
        if conn:
            conn.close()