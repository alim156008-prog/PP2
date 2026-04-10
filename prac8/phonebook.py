import psycopg2
from config import load_config

def get_connection():
    """Создает соединение, используя словарь DB_CONFIG из config.py"""
    return psycopg2.connect(**load_config())

def call_search(pattern):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
            return cur.fetchall()

def call_upsert(name, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
            conn.commit()
            print(f"Contact '{name}' processed.")
    except Exception as e:
        print(f"Error in upsert: {e}")

def call_bulk_insert(names_list, phones_list):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL bulk_insert_contacts(%s, %s);", (names_list, phones_list))
            conn.commit()
            print("Bulk insert finished. Check DB for valid entries.")
    except Exception as e:
        print(f"Error in bulk insert: {e}")

def call_pagination(limit, offset):
    """
    limit: сколько записей выгрузить
    offset: сколько записей пропустить
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paged(%s, %s);", (limit, offset))
            return cur.fetchall()

def call_delete(target):
    """Удаляет по имени или номеру телефона"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s);", (target,))
            conn.commit()
            print(f"Delete operation for '{target}' completed.")
    except Exception as e:
        print(f"Error in delete: {e}")

if __name__ == "__main__":

    call_upsert("John Doe", "87071112233")

    call_bulk_insert(["Alice", "BadPhone"], ["87475556677", "12"]) 

    print("\nSearch result for 'John':", call_search("John"))

    print("\nFirst 2 contacts (Pagination):", call_pagination(2, 0))

    call_delete("John Doe")
    
    print("\nFinal check (Pagination after delete):", call_pagination(10, 0))