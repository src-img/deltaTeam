import sqlite3
import re

class databaseManager():
    def __init__(self, database):
        self.database = database
        self.cursor = None
        self.connection = None
    
    # Connecting to database
    def connect(self):
        success = True
        error = None

        try:
            self.connection = sqlite3.connect(self.database)
        except sqlite3.Error as e:
            success = False
            error = e

        if success:
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS User(user_id INTEGER PRIMARY KEY, email VARCHAR(50), password VARCHAR(50), username VARCHAR(50))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Song(song_id INTEGER PRIMARY KEY, user_id INTEGER, song_name VARCHAR(50), length INTEGER, measures JSON)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Measure(measure_id INTEGER PRIMARY KEY, measure_number INTEGER, notes VARCHAR(50))")

        return success, error

    # Functions needed to be implemented as well as parameters after DB is figured out
    # Functions are subject to change
    
    # Adding to database
    def addUser(self, user_id, email, password, username):
        success = True
        error = None

        try:
            self.cursor.execute("INSERT INTO User(user_id, email, password, username) VALUES (?, ?, ?, ?)", (user_id, email, password, username))
            print(f"Added user with values {user_id}, {email}, {password}, {username}")
        except sqlite3.Error as e:
            success = False
            error = e

        return success, error

    def addSong(self, ID):
        pass

    def addMeasure(self):
        pass

    # Removing from database
    def removeUser(self):
        pass

    def removeSong(self):
        pass

    def removeMeasure(self):
        pass

    # Fetching from database
    def fetchUser(self): 
        pass

    def fetchSong(self):
        pass

    def fetchMeasure(self):
        pass

    def printAll(self):
        fetch = self.cursor.execute(f"SELECT * FROM User")

        for item in fetch:
            print({item})

    # Commiting changes to database 

    def commit(self):
        pass

if __name__ == "__main__":
    print("Testing databaseManager...")
    db = databaseManager("test")
    success, error = db.connect()
    print(f"db.connect() return: {success},{error}")
    db.addUser(0, "d@d", "pp", "ppp")
    db.printAll()
