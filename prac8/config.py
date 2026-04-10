DB_CONFIG = {
    "dbname": "phonebook_db",
    "user": "postgres",
    "password": "123456", 
    "host": "localhost",
    "port": "5432"
}

def load_config():
    return DB_CONFIG

if __name__ == '__main__':
    config = load_config()
    print("Config loaded successfully:", config['dbname'])