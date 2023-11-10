# Step 1: Setting Up the Database
# Using SQLite


import sqlite3

DATABASE_NAME = 'gas_usage.db'

def create_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS gas_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_hash TEXT NOT NULL,
            gas_used INTEGER NOT NULL,
            timestamp INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_transaction(tx_hash, gas_used, timestamp):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO gas_usage (tx_hash, gas_used, timestamp) VALUES (?, ?, ?)',
              (tx_hash, gas_used, timestamp))
    conn.commit()
    conn.close()

def get_average_gas_usage():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('SELECT AVG(gas_used) FROM gas_usage')
    avg_gas = c.fetchone()[0]
    conn.close()
    return avg_gas if avg_gas is not None else 0

# Missing features need to add: Error Handling, Connection Management, Efficiency,
#                       CRUD (Create, Read, Update, Delete) capability and Security.
