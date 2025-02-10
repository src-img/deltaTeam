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
            print(f"Adding user with values, '{email}', '{password}', '{username}'")
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
        measuresJSON = '{ "measuresList":[] }'

        try:
            self.cursor.execute("INSERT INTO Song(user_id, song_name, measures) VALUES (?, ?, ?)", (user_id, song_name, measuresJSON))
            print(f"Adding song with values, {user_id}, '{song_name}'")
        except sqlite3.Error as e:
            print("There was an error")
            success = False
            error = e


        id = self.cursor.lastrowid
        return success, error, id

    """
    EXAMPLE OF EXTRACTING JSON, IMPORTANT! 
        try:
            row = self.cursor.execute("SELECT json_extract (measures, '$.measuresList[1]') AS measure FROM Song").fetchone()
            print("ROW:", row[0])
        except sqlite3.Error as e:
            print("There was an error")
            success = False
            error = e
    """


    def addMeasure(self, song_id, notes):
        # Check if notes is a valid notes string

        # Add measure to the database if it does not already exist
        # If it does exist then only get the ID and insert into song with songid

        # Kind of an expensive process, sorry :/
        pass

    # Removing from database
    def removeUser(self, user_id):
        success = True
        error = None

        try:
            self.cursor.execute("DELETE FROM User WHERE user_id=?", [user_id])
            self.cursor.execute("DELETE FROM Song WHERE user_id=?", [user_id])
            print("Removing user ", user_id, " from db...")
        except sqlite3.Error as e:
            print("There was an error removing user ", user_id)
            error = e

        return success, error
        

    def removeSong(self, song_id):
        success = True
        error = None

        try:
            self.cursor.execute("DELETE FROM Song WHERE song_id=?", [song_id])
            print("Removing song ", song_id, " from db...")
        except sqlite3.Error as e:
            print("There was an error removing song ", song_id)
            error = e

        return success, error

    def removeMeasure(self):
        pass

    # Fetching from database
    def fetchUser(self, user_id):
        result = []
        error = None

        try:
            result = self.cursor.execute("SELECT * FROM User WHERE user_id=?", [user_id]).fetchone()
            print("Result of user ", user_id," :", result)
        except sqlite3.Error as e:
            print("There was an error fetching for user")
            error = e

        return result, error

    def fetchSong(self, song_id):
        result = []
        error = None

        try:
            result = self.cursor.execute("SELECT * FROM Song WHERE song_id=?", [song_id]).fetchone()
            print("Result of song ", song_id," :", result)
        except sqlite3.Error as e:
            print("There was an error fetching for song")
            error = e

        # CHANGE THE JSON IN THE RESULT INTO AN ARRAY
        return result, error

    def fetchMeasure(self, measure_id):
        pass

    def printAll(self):
        fetch = self.cursor.execute(f"SELECT * FROM User")
        for item in fetch:
            print({item})
        
        fetch = self.cursor.execute(f"SELECT * FROM Song")
        for item in fetch:
            print({item})

        fetch = self.cursor.execute(f"SELECT * FROM Measure")
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
    print("Testing for connection...")
    print(f"db.connect() return: {success},{error}")
    
    print("\nAdding Users test...")
    succ, err, user1_id = db.addUser("ben@delta", "bbben", "benben")
    succ, err, user2_id = db.addUser("peyton@delta", "ppppn", "ppddee")

    print("\nAdding Songs test...")
    succ, err, song1_id = db.addSong(user1_id, "fire.mp3")
    succ, err, song2_id = db.addSong(user2_id, "Utena <3 Himemiya.wav")
    succ, err, song3_id = db.addSong(user1_id, "End Of The World")
    succ, err, song4_id = db.addSong(user2_id, "Prince Moment")


    print("\nFetching Users test...")
    #db.commit()
    result, err = db.fetchUser(user1_id)
    print(result)
    result, err = db.fetchUser(user2_id)
    print(result)

    print("\nFetching Songs test...")
    result, err = db.fetchSong(song1_id)
    print(result)
    result, err = db.fetchSong(song2_id)
    print(result)
   
    print("\nPrint all before removal test...")
    db.printAll()

    print("\nRemoving Users test...")
    succ, err = db.removeUser(user1_id)

    print("\nRemoving Songs test...")
    succ, err = db.removeSong(song2_id)

    print("\nPrint all test...")
    db.printAll()
