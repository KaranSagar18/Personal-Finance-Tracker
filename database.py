import sqlite3
from contextlib import contextmanager
from typing import Generator

db_file = "transactions.db"

@contextmanager
def get_db() -> Generator [sqlite3.Connection,None,None]:
    conn = sqlite3.connect(db_file)
    try:
        with conn:
            yield conn
    except sqlite3.DatabaseError as e:
        print (f"Database error encountered: {e}")
        raise
    finally:
        conn.close()

def create_transaction_table() -> None:
    with get_db() as conn:
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            description TEXT
            );'''
        )

def id_exists(id :int) -> tuple | None:
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM transactions WHERE id = ?',(id,))
        return cursor.fetchone()

def add_transaction(date: str, amount: float, type: str,description: str) -> int | None:
    with get_db() as conn:
        cursor = conn.execute("INSERT INTO transactions (date,amount,type,description) VALUES (? , ? , ? ,?)",(date,amount,type,description))
        return cursor.lastrowid        

def get_transactions(start_date, end_date) -> list[tuple]:
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM transactions WHERE date BETWEEN ? and ?",(start_date,end_date))
        return cursor.fetchall()

def delete_transaction(id_to_delete) -> bool:
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM transactions WHERE id = ?",(id_to_delete,))
        return cursor.rowcount == 1

def update_transaction(id: int,date: str, amount: float, type: str, description: str) -> bool:
    with get_db() as conn:
        cursor = conn.execute('UPDATE transactions SET date = ?, amount = ?, type = ?, description =? WHERE id = ?',(date,amount,type,description,id))
        return cursor.rowcount == 1