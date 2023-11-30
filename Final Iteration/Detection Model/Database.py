import psycopg2
from psycopg2 import sql, DatabaseError

DATABASE_NAME = 'gas_usage'
USER = 'Aman_Mittal'
PASSWORD = 'Password@123'
HOST = 'localhost'  

# Function to create the current_transactions table
def create_current_transactions_table():
    try:
        with psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL('''
                    CREATE TABLE IF NOT EXISTS current_transactions (
                        id SERIAL PRIMARY KEY,
                        tx_hash TEXT NOT NULL,
                        gas_used INTEGER NOT NULL,
                        timestamp TIMESTAMP NOT NULL
                    )
                '''))
    except (Exception, DatabaseError) as e:
        print(f"Database error occurred: {e}")

# Function to create the historical_transactions table
def create_historical_transactions_table():
    try:
        with psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL('''
                    CREATE TABLE IF NOT EXISTS historical_transactions (
                        id SERIAL PRIMARY KEY,
                        tx_hash TEXT NOT NULL,
                        gas_used INTEGER NOT NULL,
                        timestamp TIMESTAMP NOT NULL
                    )
                '''))
    except (Exception, DatabaseError) as e:
        print(f"Database error occurred: {e}")

# Function to insert transaction data into current_transactions
def insert_current_transaction(tx_hash, gas_used, timestamp):
    try:
        with psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL('''
                    INSERT INTO current_transactions (tx_hash, gas_used, timestamp)
                    VALUES (%s, %s, %s)
                '''), (tx_hash, gas_used, timestamp))
    except (Exception, DatabaseError) as e:
        print(f"Database error occurred: {e}")

# Function to store the last N transactions in historical_transactions
def store_historical_transactions(n):
    try:
        with psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL('''
                    INSERT INTO historical_transactions (tx_hash, gas_used, timestamp)
                    SELECT tx_hash, gas_used, timestamp FROM current_transactions
                    ORDER BY timestamp DESC LIMIT %s
                '''), (n,))
    except (Exception, DatabaseError) as e:
        print(f"Database error occurred: {e}")

# Function to insert anomaly data
def insert_anomaly(tx_hash, gas_used):
    try:
        with psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL('''
                    INSERT INTO anomalies (tx_hash, gas_used)
                    VALUES (%s, %s)
                '''), (tx_hash, gas_used))
    except (Exception, DatabaseError) as e:
        print(f"Database error occurred: {e}")

# Function to get anomaly history
def get_anomaly_history():
    try:
        with psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL('SELECT * FROM anomalies'))
                anomalies = cur.fetchall()
                return anomalies
    except (Exception, DatabaseError) as e:
        print(f"Database error occurred: {e}")
        return []

# Function to get the previous gas usage
def get_historical_gas_usage():
    try:
        with psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL('SELECT * FROM historical_transactions'))
                historical_transactions = cur.fetchall()
                return historical_transactions
    except (Exception, DatabaseError) as e:
        print(f"Database error occurred: {e}")
        return []

# Function to get current gas usage
def get_gas_usage_data():
    try:
        with psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL('SELECT * FROM current_transactions'))
                current_transactions = cur.fetchall()
                return current_transactions
    except (Exception, DatabaseError) as e:
        print(f"Database error occurred: {e}")
        return []

# Main 
if __name__ == "__main__":
    create_current_transactions_table()
    create_historical_transactions_table()
