import pymysql

DB_NAME = "SoundboardUserDB"

def create_database_if_not_exists():
    """
    Erstellt die Datenbank, falls sie nicht existiert.
    Diese Funktion sollte nur einmal aufgerufen werden, um die Datenbank zu erstellen.
    Wird sie erneut aufgerufen, passiert nichts, wenn die Datenbank bereits existiert.
    """
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="chsasake2007",
        database="mysql",
        charset="utf8mb4"
    )
    c = conn.cursor()
    c.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.close()

conn_params = {
    "host": "localhost",
    "user": "root",
    "password": "chsasake2007",
    "database": DB_NAME,
    "charset": "utf8mb4"
}

def init_db():
    """
    Initialisiert die Datenbank und erstellt die Tabelle, falls sie nicht existiert.
    Diese Funktion sollte nur einmal aufgerufen werden, um die Datenbank und Tabelle zu erstellen.
    Wird sie erneut aufgerufen, passiert nichts, wenn die Tabelle bereits existiert.
    """
    create_database_if_not_exists()
    conn = pymysql.connect(**conn_params)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    """
    Fügt einen neuen Benutzer zur Datenbank hinzu.
    Gibt True zurück, wenn der Benutzer erfolgreich hinzugefügt wurde,
    oder False, wenn der Benutzername bereits existiert.
    """
    conn = pymysql.connect(**conn_params)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def check_user(username, password):
    """
    Überprüft, ob ein Benutzer mit dem angegebenen Benutzernamen und Passwort existiert.
    Gibt True zurück, wenn der Benutzer existiert, andernfalls False.
    """
    conn = pymysql.connect(**conn_params)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None