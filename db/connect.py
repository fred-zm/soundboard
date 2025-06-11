import mysql.connector
from datetime import datetime

def create_connection():
    global my_db


    host = input("Host (e.g.: localhost): ")
    user = input("User: ")
    password = input("Password: ")

    if host == "":
        host = 'localhost'
    if user == "":
        user = 'root'
    if password == "":
        password = "admin123!.A"
    

    my_db = mysql.connector.connect(
        host=host, user=user, password=password,
    )

create_connection()

my_cursor = my_db.cursor()

def create_database():
    # my_cursor = my_db.cursor()
    sql = """
        DROP DATABASE IF EXISTS sounds;
        CREATE DATABASE sounds;
        """
    my_cursor.execute(sql)
    my_cursor.fetchall()
    # my_cursor.close()


create_database()

def create_tables():
    # my_cursor = my_db.cursor()
    # Tabelle 'sounds' definieren
    # Annahme: 'sounds' benötigt mindestens eine Spalte wie 'id' und einen 'name' oder 'path'.
    # Bitte passe die Spalten und Datentypen an deine tatsächlichen Anforderungen an.
    sql_sound_table = """
        USE sounds;
        CREATE TABLE sound (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            filepath VARCHAR(512) UNIQUE NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    my_cursor.execute(sql_sound_table)
    my_cursor.fetchall()
    # Tabelle 'user' definieren
    sql_user_table = """
        USE sounds;
        CREATE TABLE user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """
    my_cursor.execute(sql_user_table)
    my_cursor.fetchall()
    # Änderungen an der Datenbank festschreiben
    my_db.commit()
    # my_cursor.close()


create_tables()

# def insert_from_user_input():

#     name = input("Name: ")
#     genre = input("Genre: ")

#     val = f"'{datetime.now().strftime('%Y-%m-%d')}', '{name}', '{genre}'"
#     sql = f"INSERT INTO sound VALUE ({val})"

#     my_cursor.execute(sql)
#     my_db.commit()


# def update_sound():
#     old_sound = input("Welcher Sound soll ersetzt werden? ")
#     new_sound = input("Welcher Sound soll stattdessen eingetragen werden? ")

#     sql = f"UPDATE sound SET name = '{new_sound}' WHERE name = '{old_sound}'"

#     my_cursor.execute(sql)
#     my_db.commit()


# def show_all_data():
#     my_cursor.execute("SELECT * FROM sound")
#     result = my_cursor.fetchall()

#     for item in result:
#         print(item)


# update_sound()
# show_all_data()

