import mysql.connector
from datetime import datetime
import json
import os

from platformdirs import *
def create_connection():
    global my_db
    print(user_config_dir)
    path = user_config_dir('soundboard','Gruppe-B') + '\\soundboard.ini'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    while True:
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
                host = config['host']
                user = config['user']
                password = config['password']
                my_db = mysql.connector.connect(
                    host=host, user=user, password=password,
                )
                my_db.cursor()
                break
        except:
            with open(path, "w", encoding="utf-8") as f:
                config = {}
                config['host'] = input("DB Host:")
                host = config['host']
                config['user'] = input("User: ")
                user = config['user']
                config['password'] = input("Passwort: ")
                password = config['password']
                json.dump(config, f, indent=4)


def create_database():
    sql = """
            CREATE DATABASE IF NOT EXISTS sounds;
        """
    my_cursor.execute(sql)
    my_cursor.fetchall()
    my_cursor.nextset()
    my_db.commit()



def create_tables():
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
    try: my_cursor.nextset()
    except : pass
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
    try: my_cursor.nextset() 
    except: pass
    # Änderungen an der Datenbank festschreiben
    my_db.commit()

def get_users(username):
    my_cursor.execute('use sounds')
    my_cursor.execute(f"SELECT username, password FROM user where username = '{username}'")
    result = my_cursor.fetchall()
    user_dic = {}
    for entry in result:
        user_dic[entry[0]] = entry[1]
    return user_dic

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

my_db = None
create_connection()
my_cursor = my_db.cursor()
create_database()
create_tables()
if __name__ == '__main__':
    users = get_users()
