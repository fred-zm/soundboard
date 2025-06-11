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
            sound_data LONGBLOB  NOT NULL,
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
    sql_usersound_table = """
            USE sounds;
            CREATE TABLE usersound (
                user_id INT NOT NULL,
                sound_id INT NOT NULL,
                button_name VARCHAR(255),
                PRIMARY KEY (user_id, sound_id),
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (sound_id) REFERENCES sound(id)
            )
        """
    my_cursor.execute(sql_usersound_table)
    my_cursor.fetchall()
    try: my_cursor.nextset() 
    except: pass
    # Änderungen an der Datenbank festschreiben
    my_db.commit()

def get_users(username):
    my_cursor.execute('use sounds')
    my_cursor.execute(f"SELECT id, username, password FROM user where username = '{username}'")
    result = my_cursor.fetchall()
    user_dic = {}
    for entry in result:
        user_dic['id'] = entry[0]
        user_dic['username'] = entry[1]
        user_dic['password'] = entry[2]
    return user_dic

my_db = None
create_connection()
my_cursor = my_db.cursor()
create_database()
create_tables()

def add_sound(file_path, user_id):
    with open(file_path, 'rb') as file:
        sound_blob = file.read()
    my_cursor.execute("use sounds")
    sql = "INSERT INTO sound (sound_data) VALUES (%s)"
    my_cursor.execute(sql, (sound_blob,))
    sql = "INSERT INTO usersound (user_id, sound_id, button_name) VALUES (%s, LAST_INSERT_ID(), 'test')"
    my_cursor.execute(sql, (user_id,))
    my_db.commit()
    return sound_blob 

def load_sounds(user_id):
    my_cursor.execute("use sounds")
    sql = "SELECT sound_data FROM sound s JOIN usersound us on s.id = us.sound_id WHERE us.user_id = %s"
    my_cursor.execute(sql, (user_id,))
    sounds = []
    for sound in my_cursor.fetchall():
        sounds.append(sound)
    return sounds

def save_sounds():
    pass