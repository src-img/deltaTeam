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
            print("There was an error")
            success = False
            error = e

        if success:
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS User(user_id INTEGER PRIMARY KEY AUTOINCREMENT, email VARCHAR(50), password VARCHAR(50), username VARCHAR(50))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Song(song_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, song_name VARCHAR(50), length INTEGER, measures TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Measure(measure_id INTEGER PRIMARY KEY AUTOINCREMENT, measure_number INTEGER, notes VARCHAR(50))")

        return success, error

    # Functions needed to be implemented as well as parameters after DB is figured out
    # Functions are subject to change
    
    # Adding to database
    def addUser(self, email, password, username):
        success = True
        error = None

        try:
            self.cursor.execute("INSERT INTO User(email, password, username) VALUES (?, ?, ?)", (email, password, username))
            print(f"Added user with values, '{email}', '{password}', '{username}'")
        except sqlite3.Error as e:
            print("There was an error")
            success = False
            error = e
         
        id = self.cursor.lastrowid
        #print(id)
        return success, error, id 

    def addSong(self, user_id, song_name):
        success = True
        error = None

        try:
            self.cursor.execute("INSERT INTO Song(user_id, song_name) VALUES (?, ?)", (user_id, song_name))
            print(f"Added song with values, {user_id}, '{song_name}'")
        except sqlite3.Error as e:
            print("There was an error")
            success = False
            error = e



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
        success = True
        error = None

        try:
            self.connection.commit()
        except sqlite3.Error as e:
            print("There was an error")
            success = False
            error = e
        
        return success, error

if __name__ == "__main__":
    print("Testing databaseManager...")
    db = databaseManager("test")
    success, error = db.connect()
    print(f"db.connect() return: {success},{error}")
    succ, err, lastid = db.addUser("ben@delta", "bbben", "benben")
    db.addSong(lastid, "fire.mp3")
    succ, err, lastid = db.addUser("peyton@delta", "ppppn", "ppddee")
    db.addSong(lastid, "Utena <3 Himemiya")
    #db.commit()
    db.printAll()
