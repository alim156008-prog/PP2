import psycopg2
from config import load_config

def connect():
    """Проверка соединения с БД"""
    config = load_config()
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        
        cur.execute('SELECT version()')
        print(f'PostgreSQL version: {cur.fetchone()}')
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection error: {error}")
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    connect()