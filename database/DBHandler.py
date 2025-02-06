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
            # Add cursor.execute here after DB is designed

        return success, error

    # Functions needed to be implemented as well as parameters after DB is figured out
    # Functions are subject to change
    
    # Adding to database
    def addUser(self):
        pass

    def addSong(self):
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


    # Commiting changes to database 

    def commit(self):
        pass
