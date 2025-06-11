import pyodbc
import os

DB_NAME = "SoundboardUserDB"

def create_database_if_not_exists():
    """
    Erstellt die Datenbank, falls sie nicht existiert.
    Diese Funktion sollte nur einmal aufgerufen werden, um die Datenbank zu erstellen.
    Wird sie erneut aufgerufen, passiert nichts, wenn die Datenbank bereits existiert.
    """
    # Verbindung zum Master-DB, um ggf. die User-DB zu erstellen
    master_conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(master_conn_str, autocommit=True)
    c = conn.cursor()
    c.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{DB_NAME}') CREATE DATABASE {DB_NAME};")
    conn.close()

# Beispiel-Connection-String (anpassen!)
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    f"DATABASE={DB_NAME};"
    "Trusted_Connection=yes;"
)

def init_db():
    """
    Initialisiert die Datenbank und erstellt die Tabelle, falls sie nicht existiert.
    Diese Funktion sollte nur einmal aufgerufen werden, um die Datenbank und Tabelle zu erstellen.
    Wird sie erneut aufgerufen, passiert nichts, wenn die Tabelle bereits existiert.
    """
    create_database_if_not_exists()  # <-- Datenbank anlegen, falls nicht vorhanden
    conn = pyodbc.connect(conn_str)
    c = conn.cursor()
    c.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            username NVARCHAR(255) PRIMARY KEY,
            password NVARCHAR(255) NOT NULL
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
    conn = pyodbc.connect(conn_str)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
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
    conn = pyodbc.connect(conn_str)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None