import psycopg2
from psycopg2.extras import DictCursor
from data.config import DB_NAME, DB_PASSWORD

# PostgreSQL connection
conn = psycopg2.connect(
    user="postgres",
    dbname=DB_NAME,
    password=DB_PASSWORD,
    host="localhost",
    port=5432,
    cursor_factory=DictCursor
)
cur = conn.cursor()

# SQL table definitions
TABLES = {
    "users": '''
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL PRIMARY KEY,
            telegram_id VARCHAR(60) UNIQUE,
            created_at TIMESTAMP DEFAULT now()
        )
    ''',
    "channels": '''
        CREATE TABLE IF NOT EXISTS channels (
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR(128) NOT NULL,
            channel_id VARCHAR(128) UNIQUE,
            is_order BOOLEAN DEFAULT False,
            created_at TIMESTAMP DEFAULT now()
        )
    ''',
    "links": '''
        CREATE TABLE IF NOT EXISTS links (
            id BIGSERIAL PRIMARY KEY,
            link VARCHAR(500) UNIQUE,
            created_at TIMESTAMP DEFAULT now()
        )
    ''',
    "movies": '''
        CREATE TABLE IF NOT EXISTS movies (
            id BIGSERIAL PRIMARY KEY,
            post_id INT NOT NULL,
            url VARCHAR(500) NOT NULL,
            file_id VARCHAR(800) NOT NULL,
            caption TEXT,
            created_at TIMESTAMP DEFAULT now()
        )
    ''',
    "join_requests": '''
        CREATE TABLE IF NOT EXISTS join_requests (
            id BIGSERIAL PRIMARY KEY,
            channel_id VARCHAR(800) NOT NULL,
            user_id VARCHAR(800) NOT NULL,
            created_at TIMESTAMP DEFAULT now()
        )
    '''
}

def startup_table():
    """
    Creates all necessary tables if they do not exist.
    """
    try:
        for table_name, query in TABLES.items():
            cur.execute(query)
            print(f"Table '{table_name}' ensured.")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
