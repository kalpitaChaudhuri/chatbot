import psycopg2
from psycopg2 import sql

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="chatbot_db",  
        user="postgres",
        password="123" 
    )
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            brand VARCHAR(255),
            price DECIMAL,
            category VARCHAR(255),
            description TEXT,
            supplier_id INTEGER
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            contact_info TEXT,
            product_categories TEXT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
