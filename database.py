import sqlite3
import time, json
from os.path import isfile

def connect_db(dbname: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connects to the Kuko database or creates it if it doens't exist.

    Requires:
    dbname (str): the name of the database file.
    Ensures:
    Connecting to the Kuko database file or creating it if it doesn't exist 
    and returning the Connection and Cursor objects of the database.
    """
    db_is_created = isfile(dbname)
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if not db_is_created:
        # Execute queries and commit
        with open('database.sql', 'r') as f:
            cursor.executescript(f.read())
        # Populate database
        ini_questions = [
            (1, 'Qual a capital de Portugal?', 'Lisboa;Madrid;Paris;Roma', 1),
            (2, 'Qual a capital de Alemanha?', 'Frankfurt am Main;Berlim;Colónia;Munique', 2),
            (3, 'Qual a capital de Finlândia?', 'Oslo;Malmö;Estocolmo;Reiquiavique;Helsínquia', 5),
            (4, 'Qual a capital de Suiça?', 'Geneva;Innsbruck;Berna;Zurique;Vienna;Munique', 3),
            (5, 'Qual a capital da República Checa?', 'Brno;Varsóvia;Praga;Budapeste;Belgrade;Vílnius', 3)
        ]
        ini_qset = (1, json.dumps([1,2,3,4,5]))
        ini_quiz = (1, 1, 
        json.dumps([(1, 10),(2, 10),(3, 10),(4, 10),(5, 10)]), 
        "PREPARED", round(time.time()), 0, 1, json.dumps([]))
        # Insert all rows
        cursor.executemany('INSERT INTO question VALUES (?, ?, ?, ?)', ini_questions)
        cursor.execute('INSERT INTO qset VALUES (?, ?)', ini_qset)
        cursor.execute('INSERT INTO quiz VALUES (?, ?, ?, ?, ?, ?, ?, ?)', ini_quiz)
        connection.commit()
    return connection, cursor
