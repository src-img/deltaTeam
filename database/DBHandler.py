import sqlite3
import re
import json
import threading

class databaseManager():
    def __init__(self, database):
        self.database = database
        self.cursor = None
        self.connection = None
        self.lock = threading.Lock()
        # Regex input validation
        #self.valid = re.compile(r'^[SEQHWseqhwSEIQQSJJSHSHEHIDDSDEDIWseiqqUsjjUshhUshUehvVUiddUsdUeduiwyY.+|()]*$')

    
    # Connecting to database
    def connect(self):
        success = True
        error = None

        try:
            self.connection = sqlite3.connect(self.database, check_same_thread=False)
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

    
    # Adding to database
    def addUser(self, email, password, username):
        success = True
        error = None

        self.lock.acquire(True)
        try:
            self.cursor.execute("INSERT INTO User(email, password, username) VALUES (?, ?, ?)", (email, password, username))
            print(f"Adding user with values, '{email}', '{password}', '{username}'")
        except sqlite3.Error as e:
            print("There was an error")
            success = False
            error = e
         
        id = self.cursor.lastrowid
        #print(id)
        self.lock.release()
        return success, error, id 

    def addSong(self, user_id, song_name):
        success = True
        error = None
        measuresJSON = '{ "measuresList":[] }'

        self.lock.acquire(True)
        try:
            self.cursor.execute("INSERT INTO Song(user_id, song_name, measures) VALUES (?, ?, ?)", (user_id, song_name, measuresJSON))
            print(f"Adding song with values, {user_id}, '{song_name}'")
        except sqlite3.Error as e:
            print("There was an error")
            success = False
            error = e
        self.lock.release()

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
        
        print("attempting to add measures")

        self.lock.acquire(True)
        try:
            res = self.cursor.execute(
                "SELECT measure_id FROM Measure WHERE notes = ?", 
                (notes,)
            ).fetchone()
            #print("printing res", res) 
            if res:  # Measure exists
                id = res[0]
            else:    # New measure
                self.cursor.execute(
                    "INSERT INTO Measure (notes) VALUES (?)", 
                    (notes,)
                )
                id = self.cursor.lastrowid


                print(res)
        except sqlite3.Error as e:
            print("Error inserting measure", e)
            error = e

        #print("measure ID: ", id)

        try:
            print("inserting ", notes, " into song ", song_id)
            #self.cursor.execute("UPDATE Song SET measures = json_insert(measures, '$.measuresList[#]', (?)) WHERE song_id=(?)", (id, song_id))
            #res = self.cursor.execute("SELECT * FROM Measure WHERE notes=(?)", [notes]).fetchone()
            #print(res)

            song_data = self.cursor.execute(
                "SELECT measures FROM Song WHERE song_id=?", 
                (song_id,)
            ).fetchone()
        
            if song_data and song_data[0]:
                # Parse existing JSON
                measures = json.loads(song_data[0])
                if 'measuresList' not in measures:
                    measures['measuresList'] = []
            else:
                # Initialize new JSON structure
                measures = {'measuresList': []}
            #print("here are the id's", id) 
            # Append the new measure ID
            measures['measuresList'].append(id)
        
            # Update the song with the modified measures
            self.cursor.execute(
                "UPDATE Song SET measures=? WHERE song_id=?",
                (json.dumps(measures), song_id)
            )
 


        except sqlite3.Error as e:
            print("Error inserting measure into song JSON")
            error = e
        

        self.lock.release()
        return success, error, id


    # Removing from database
    def removeUser(self, user_id):
        success = True
        error = None

        self.lock.acquire(True)

        try:
            self.cursor.execute("DELETE FROM User WHERE user_id=?", [user_id])
            self.cursor.execute("DELETE FROM Song WHERE user_id=?", [user_id])
            print("Removing user ", user_id, " from db...")
        except sqlite3.Error as e:
            print("There was an error removing user ", user_id)
            error = e

        self.lock.release()
        return success, error
        

    def removeSong(self, song_id):
        success = True
        error = None

        self.lock.acquire(True)
        try:
            self.cursor.execute("DELETE FROM Song WHERE song_id=?", [song_id])
            print("Removing song ", song_id, " from db...")
        except sqlite3.Error as e:
            print("There was an error removing song ", song_id)
            error = e
 
        self.lock.release()
         
        return success, error
    
    def clearSong(self, song_id):
        success = True
        error = None
        measuresJSON = '{ "measuresList":[] }'

        self.lock.acquire(True)
        try:
            self.cursor.execute("UPDATE Song SET measures = ? WHERE song_id=?", (measuresJSON, song_id))
            print("Clearing song ", song_id, " from db...")
        except sqlite3.Error as e:
            print("There was an error removing song ", song_id)
            error = e
 
        self.lock.release()
         
        return success, error


    def removeMeasure(self, song_id, position):
        success = True
        error = None

        self.lock.acquire(True)
        try:
            self.cursor.execute("UPDATE Song SET measures = json_remove(measures,'$.measuresList[" + str(position) + "]') WHERE song_id=(?)", [song_id])
        except sqlite3.Error as e:
            print("Error removing measure in song JSON")
            error = e
        
        self.lock.release()

        return success, error


    # Fetching from database
    def fetchUser(self, email):
        result = []
        error = None

        self.lock.acquire(True)
        try:
            result = self.cursor.execute("SELECT * FROM User WHERE email=?", [email]).fetchone()
            print("Result of user ", email," :", result)
        except sqlite3.Error as e:
            print("There was an error fetching for user")
            error = e

        self.lock.release() 
         
        if result != None:
            result = list(result)
        return result, error


    # Fetching from database
    def fetchUserByUsername(self, username):
        result = []
        error = None

        self.lock.acquire(True)
        try:
            result = self.cursor.execute("SELECT * FROM User WHERE username=?", [username]).fetchone()
            print("Result of user ", username," :", result)
        except sqlite3.Error as e:
            print("There was an error fetching for user")
            error = e

        self.lock.release() 
         
        if result != None:
            result = list(result)
        return result, error


    def fetchSong(self, song_id):
        
        result = []
        error = None

        self.lock.acquire(True)
        try:
            
            result = self.cursor.execute("SELECT * FROM Song WHERE song_id=?", [song_id]).fetchone()
        except sqlite3.Error as e:
            print("There was an error fetching for song")
            error = e
            return result, error
        
        self.lock.release()
        if result != None: 
            result = list(result)
            dictofjson = json.loads(result[4])
            arrayofjson = dictofjson['measuresList']
            result[4] = list(arrayofjson)
            print("Result of song ", song_id," :", result)
        # CHANGE THE JSON IN THE RESULT INTO AN ARRAY
        return result, error

    def fetchUserSongs(self, user_id):
        
        result = []
        error = None

        self.lock.acquire(True)
        try:
            
            result = self.cursor.execute("SELECT * FROM Song WHERE user_id=?", [user_id]).fetchall()
        except sqlite3.Error as e:
            print("There was an error fetching for song")
            error = e
            return result, error
        
        self.lock.release()
        #if result != None: 
        #    result = list(result)
        #    dictofjson = json.loads(result[4])
        #    arrayofjson = dictofjson['measuresList']
        #    result[4] = list(arrayofjson)
        #    print("Result of song ", user_id," :", result)
        # CHANGE THE JSON IN THE RESULT INTO AN ARRAY
        return result, error

    def fetchUserSongsNames(self, user_id):
        result, error = self.fetchUserSongs(user_id)
        names = []

        for song in result:
            names.append(song[2])

        return names

    def fetchUserSongsID(self, user_id):
        result, error = self.fetchUserSongs(user_id)
        ID = []

        for song in result:
            ID.append(song[0])

        return ID

    def fetchMeasure(self, measure_id):
        result = []
        error = None

        self.lock.acquire(True)
        try:
            result = self.cursor.execute("SELECT * FROM Measure WHERE measure_id=?", [measure_id]).fetchone()
            print("Result of fetch measure ", measure_id," :", result)
        except sqlite3.Error as e:
            print("There was an error fetching for measure")
            error = e
        
        self.lock.release()
        if result != None:
            result = list(result)
        return result, error

    def changeSongName(self, song_id, song_name):
        success = True
        error = None

        self.lock.acquire(True)
        try:
            self.cursor.execute("UPDATE Song SET song_name = '" + song_name + "' WHERE song_id=(?)", [song_id])
        except sqlite3.Error as e:
            print("There was an error changing song name")
            error = e
        self.lock.release()
        
        return success, error


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
    result, err = db.fetchUser("ben@delta")
    assert(result[0] == 1)
    assert(result[1] == 'ben@delta')
    assert(result[2] == 'bbben')
    assert(result[3] == 'benben')
    print(result)

    result, err = db.fetchUser("peyton@delta")
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
    db.printAll() 

    result, err = db.changeSongName(1, "changing name")
    print(err)
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
    #succ, err, id = db.addMeasure(4, "P")
    #assert(succ == False)
    #assert(err == "Invalid measure note string")
    db.printAll()
    
    #print("\nFetching measure test...")
    #result, err = db.fetchMeasure(1)
    #print("WTF", result)
    #assert(result[0] == 1)
    #assert(result[1] == None)
    #assert(result[2] == "W")

    #result, err = db.fetchMeasure(2)
    #assert(result[0] == 2)
    #assert(result[1] == None)
    #assert(result[2] == "Q")

    #result, err = db.fetchMeasure(3) 
    #assert(result == None)
    
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

    print("\nChanging song name test...")

    print("\nFetch by username test...")
    result, err = db.fetchUserByUsername("ppddee")

    print("\nRemoving Measure test...")
    succ, err = db.removeMeasure(4,1)
    assert(succ == True)
    assert(err == None)
    

    succ, err, id = db.addMeasure(4, "Q")
    succ, err, id = db.addMeasure(4, "V")
    succ, err, id = db.addMeasure(4, "v")
    db.printAll()

    succ, err = db.clearSong(4)
    db.printAll()
