import psycopg2
from psycopg2.extras import DictCursor

from data.config import DB_NAME, DB_PASSWORD

conn = psycopg2.connect(
    user="postgres",
    dbname=DB_NAME,
    password=DB_PASSWORD,
    host="localhost",
    port=5432,
    cursor_factory=DictCursor
)
cur = conn.cursor()


def startup_table():
    query = '''
    CREATE TABLE IF NOT EXISTS users(
        id BIGSERIAL PRIMARY KEY,
        telegram_id VARCHAR(60) UNIQUE,
        created_at TIMESTAMP DEFAULT now()
        )
    '''
    channel_query = '''
    CREATE TABLE IF NOT EXISTS channels(
        id BIGSERIAL PRIMARY KEY,
        username VARCHAR(128) NOT NULL,
        channel_id VARCHAR(128) UNIQUE,
        is_order BOOLEAN DEFAULT False,
        created_at TIMESTAMP DEFAULT now()
    )
    '''
    link_query = '''
    CREATE TABLE IF NOT EXISTS links(
        id BIGSERIAL PRIMARY KEY,
        link VARCHAR(500) UNIQUE,
        created_at TIMESTAMP DEFAULT now()
    )
    '''
    media_query = '''
    CREATE TABLE IF NOT EXISTS movies(
        id BIGSERIAL PRIMARY KEY,
        post_id INT NOT NULL,
        url VARCHAR(500) NOT NULL,
        file_id VARCHAR(800) NOT NULL,
        caption TEXT,
        created_at TIMESTAMP DEFAULT now()
    )
    '''
    join_request = '''
    CREATE TABLE IF NOT EXISTS join_requests(
        id BIGSERIAL PRIMARY KEY,
        channel_id VARCHAR(800) not null,
        user_id VARCHAR(800) not null,
        created_at TIMESTAMP DEFAULT now()
    )
    '''
    cur.execute(query)
    cur.execute(channel_query)
    cur.execute(link_query)
    cur.execute(media_query)
    cur.execute(join_request)
    conn.commit()
