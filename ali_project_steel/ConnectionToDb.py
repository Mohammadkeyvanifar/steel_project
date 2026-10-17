# database_connection.py

import psycopg2
from psycopg2 import Error
from config import DB_CONFIG

def get_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        return None
