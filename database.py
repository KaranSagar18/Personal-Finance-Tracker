import sqlite3

db_file = "transactions.db"

def create_transaction_table():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            description TEXT
            );'''
        )

def add_transaction(date,amount,type,description):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (date,amount,type,description) VALUES (? , ? , ? ,?)",(date,amount,type,description))
        return cursor.lastrowid

def get_transactions(start_date, end_date) -> list[tuple]:
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE date BETWEEN ? and ?",(start_date,end_date))
        return cursor.fetchall()

def delete_transaction(id_to_delete):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?",(id_to_delete,))
        return cursor.rowcount == 1