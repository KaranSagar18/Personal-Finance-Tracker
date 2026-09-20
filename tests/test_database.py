import pytest
import database
from database import create_transaction_table,add_transaction,get_transactions,delete_transaction
import sqlite3

@pytest.fixture
def temp_db(monkeypatch,tmp_path):
    db = tmp_path/"trans.db"
    monkeypatch.setattr(database, "db_file",db)
    return db

@pytest.fixture
def db_with_table(monkeypatch,tmp_path):
    db = tmp_path/"trans.db"
    monkeypatch.setattr(database, "db_file",db)
    create_transaction_table()
    return db

def test_create_transaction_table(temp_db):
    create_transaction_table()
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
        assert result.fetchone() is not None

def test_add_transaction(db_with_table):
    add_transaction("2026-09-01", 50000, "credit","Salary")
    with sqlite3.connect(db_with_table) as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM transactions").fetchone()
        assert isinstance(result[0],int)
        assert result[1] == "2026-09-01"
        assert result[2] == 50000
        assert result[3] == "credit" 
        assert result[4] == "Salary"

def test_get_transactions(db_with_table):
    add_transaction("2026-09-01", 50000, "credit","Salary")
    add_transaction("2026-09-02", 5000, "debit","EMI")
    add_transaction("2026-09-07", 1000, "debit","Food")

    result = get_transactions("2026-09-01", "2026-09-05")
    assert len(result)==2
    assert result[0][1] == "2026-09-01"
    assert result[0][2] == 50000
    assert result[0][3] == "credit"
    assert result[0][4] == "Salary"
    assert result[1][1] == "2026-09-02"
    assert result[1][2] == 5000
    assert result[1][3] == "debit"
    assert result[1][4] == "EMI"

def test_get_transactions_no_match(db_with_table):
    add_transaction("2026-09-01", 50000, "credit","Salary")
    add_transaction("2026-09-02", 5000, "debit","EMI")
    add_transaction("2026-09-07", 1000, "debit","Food")
    
    result = get_transactions("2026-09-05", "2026-09-05")
    assert len(result)==0

def test_get_transactions_exact_date(db_with_table):
    add_transaction("2026-09-01", 50000, "credit","Salary")
    add_transaction("2026-09-02", 5000, "debit","EMI")
    add_transaction("2026-09-07", 1000, "debit","Food")
    
    result = get_transactions("2026-09-02", "2026-09-02")
    assert len(result)==1
    assert result[0][1] == '2026-09-02'

def test_get_transactions_multiple_transactions_on_same_date(db_with_table):
    add_transaction("2026-09-02", 50000, "credit","Salary")
    add_transaction("2026-09-02", 5000, "debit","EMI")
    add_transaction("2026-09-02", 1000, "debit","Food")
    
    result = get_transactions("2026-09-02", "2026-09-02")
    assert len(result)==3

def test_delete_transaction_id_exists(db_with_table):
    add_transaction("2026-09-02", 50000, "credit","Salary")
    assert delete_transaction(1) == True
    with sqlite3.connect(db_with_table) as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM transactions WHERE id = 1').fetchone()
        assert result is None

def test_delete_transaction_id_doesnt_exist(db_with_table):
    assert delete_transaction(1) == False