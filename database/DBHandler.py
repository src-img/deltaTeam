import sqlite3
import re
import json

class databaseManager():
    def __init__(self, database):
        self.database = database
        self.cursor = None
        self.connection = None

        # Regex input validation
        self.valid = re.compile(r'^[SEQHWseqhw.+|()]*$')

    
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
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Measure(measure_id INTEGER PRIMARY KEY AUTOINCREMENT, notes VARCHAR(50))")

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
        success = True
        error = None
        
        if self.valid.match(notes):
            print("valid string of notes")
        else:
            print("not valid string of notes. error. not adding measure")
            error = "Invalid measure note string"
            success = False
            return success, error, None

        try:
            res = self.cursor.execute("SELECT * FROM Measure WHERE notes=(?)", [notes]).fetchone()
            if res == None: 
                self.cursor.execute("INSERT INTO Measure(notes) VALUES(?)", (notes))
        except sqlite3.Error as e:
            print("Error inserting measure")
            error = e

        id = self.cursor.lastrowid
        #print("measure ID: ", id)

        try:
            self.cursor.execute("UPDATE Song SET measures = json_insert(measures, '$.measuresList[#]', (?)) WHERE song_id=(?)", (id, song_id))
        except sqlite3.Error as e:
            print("Error inserting measure into song JSON")
            error = e
       

        return success, error, id


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

    def removeMeasure(self, song_id, position):
        success = True
        error = None

        try:
            self.cursor.execute("UPDATE Song SET measures = json_remove(measures,'$.measuresList[" + str(position) + "]') WHERE song_id=(?)", [song_id])
        except sqlite3.Error as e:
            print("Error removing measure in song JSON")
            error = e
        
        return success, error


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


        if result != None:
            result = list(result)
        return result, error

    def fetchSong(self, song_id):
        result = []
        error = None

        try:
            result = self.cursor.execute("SELECT * FROM Song WHERE song_id=?", [song_id]).fetchone()
        except sqlite3.Error as e:
            print("There was an error fetching for song")
            error = e
            return result, error
        
        if result != None: 
            result = list(result)
            dictofjson = json.loads(result[4])
            arrayofjson = dictofjson['measuresList']
            result[4] = arrayofjson
            print("Result of song ", song_id," :", result)
        # CHANGE THE JSON IN THE RESULT INTO AN ARRAY
        return result, error

    def fetchMeasure(self, measure_id):
        result = []
        error = None

        try:
            result = self.cursor.execute("SELECT * FROM Measure WHERE measure_id=?", [measure_id]).fetchone()
            print("Result of fetch measure ", measure_id," :", result)
        except sqlite3.Error as e:
            print("There was an error fetching for measure")
            error = e
        
        if result != None:
            result = list(result)
        return result, error


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
    print("Starting tests\n")
    print("Testing databaseManager...")
    db = databaseManager("test")
    success, error = db.connect()
    print("Testing for connection...")
    print(f"db.connect() return: {success},{error}")
    assert(error == None)
    
    print("\nAdding Users test...")
    succ, err, user1_id = db.addUser("ben@delta", "bbben", "benben")
    assert(succ == True)
    assert(err == None)
    assert(user1_id == 1)

    succ, err, user2_id = db.addUser("peyton@delta", "ppppn", "ppddee")
    assert(succ == True)
    assert(err == None)
    assert(user2_id == 2)

    print("\nAdding Songs test...")
    succ, err, song1_id = db.addSong(user1_id, "fire.mp3")
    assert(succ == True)
    assert(err == None)
    assert(song1_id == 1)

    succ, err, song2_id = db.addSong(user2_id, "Utena <3 Himemiya.wav")
    assert(succ == True)
    assert(err == None)
    assert(song2_id == 2)

    succ, err, song3_id = db.addSong(user1_id, "End Of The World")
    assert(succ == True)
    assert(err == None)
    assert(song3_id == 3)

    succ, err, song4_id = db.addSong(user2_id, "Prince Moment")
    assert(succ == True)
    assert(err == None)
    assert(song4_id == 4)


    print("\nFetching Users test...")
    #db.commit()
    result, err = db.fetchUser(user1_id)
    assert(result[0] == 1)
    assert(result[1] == 'ben@delta')
    assert(result[2] == 'bbben')
    assert(result[3] == 'benben')
    print(result)

    result, err = db.fetchUser(user2_id)
    assert(result[0] == 2)
    assert(result[1] == 'peyton@delta')
    assert(result[2] == 'ppppn')
    assert(result[3] == 'ppddee')
    print(result)

    print("\nFetching Songs test...")
    result, err = db.fetchSong(song1_id)
    assert(result[0] == 1)
    assert(result[1] == 1)
    assert(result[2] == 'fire.mp3')
    assert(result[3] == None)
    assert(result[4] == [])
    print(result)

    result, err = db.fetchSong(song2_id)
    assert(result[0] == 2)
    assert(result[1] == 2)
    assert(result[2] == 'Utena <3 Himemiya.wav')
    assert(result[3] == None)
    assert(result[4] == [])
    print(result)
   
    print("\nPrint all before removal test...")
    db.printAll()

    print("\nRemoving Users test...")
    succ, err = db.removeUser(user1_id)
    assert(succ == True)
    assert(err == None)

    print("\nRemoving Songs test...")
    succ, err = db.removeSong(song2_id)
    assert(succ == True)
    assert(err == None)

    print("\nPrint all test...")
    db.printAll()

    print("\nInsert Measure Test...")
    succ, err, id = db.addMeasure(4, "W")
    assert(succ == True)
    assert(err == None)
    succ, err, id = db.addMeasure(4, "Q")
    assert(succ == True)
    assert(err == None)
    succ, err, id = db.addMeasure(4, "P")
    assert(succ == False)
    assert(err == "Invalid measure note string")
    db.printAll()
    
    print("\nFetching measure test...")
    result, err = db.fetchMeasure(1)
    print("WTF", result)
    assert(result[0] == 1)
    assert(result[1] == None)
    assert(result[2] == "W")

    result, err = db.fetchMeasure(2)
    assert(result[0] == 2)
    assert(result[1] == None)
    assert(result[2] == "Q")

    result, err = db.fetchMeasure(3) 
    assert(result == None)
    
    print("\nFetching Songs with measures test...")
    result, err = db.fetchSong(song3_id)
    assert(result == None) 
    print(result)
    result, err = db.fetchSong(song4_id)
    assert(result[0] == 4)
    assert(result[1] == 2)
    assert(result[2] == 'Prince Moment')
    assert(result[3] == None)
    assert(result[4] == [1, 2])
    print(result)

    print("\nRemoving Measure test...")
    succ, err = db.removeMeasure(4,1)
    assert(succ == True)
    assert(err == None)

    db.printAll()
