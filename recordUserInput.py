
from enum import Enum
import random

class InputState(Enum):
    addNote = 1
    addRest = 2
    increaseDuration = 3

noteArray = ["s","e","i","q","qUs","j","jUs","h","hUs","hUe","hUi","d","dUs","dUe","dui","w"]
restArray = ["S","E","I","Q","QS","J","JS","H","HS","HE","HI","D","DS","DE","DI","W"]
emptyArray = ["","","","","","","","","","","","","","","",""]

class Composition:
    def __init__(self):
        self.composition = "g$|"
        self.userInput = InputState.addRest
        self.noteSizeLimit = 15
        self.sixteenth = 1
        self.noteSize = 0
        self.arrayPtr = restArray.copy()
        self.record = False
        self.recordCountdown = 0
        self.noteSize = 0
        self.arrayPtr = emptyArray.copy()
        self.metronomeCounter = 0

    def setNoteSizeLimit(self):
            match (self.sixteenth % 4):
                case 0: 
                    self.noteSizeLimit = 15 - (self.sixteenth % 16)
                case 1:
                    self.noteSizeLimit = 1
                case 2:
                    self.noteSizeLimit = 1
                case 3:
                    self.noteSizeLimit = 0

    def compose(self):
        if self.arrayPtr != emptyArray:
            if self.userInput == InputState.addNote or self.noteSize == self.noteSizeLimit or (self.userInput == InputState.addRest and self.arrayPtr != restArray):
                self.composition += self.arrayPtr[self.noteSize]
                match self.userInput:
                    case InputState.increaseDuration:
                        if self.arrayPtr == noteArray:
                            self.composition += "U"
                    case InputState.addNote:
                        self.arrayPtr = noteArray.copy()
                    case InputState.addRest:
                        self.arrayPtr = restArray.copy()
                self.userInput = InputState.increaseDuration
                self.setNoteSizeLimit()
                self.noteSize = 0
            else:
                self.noteSize += 1
            if self.sixteenth % 16 == 0:
                if (self.composition[-1] == "U"):
                    self.composition = self.composition[:-1]
                    self.composition += "v"    
                else:
                    self.composition += "|"
                self.parseComposition()
                self.sixteenth = 0
            if self.sixteenth % 4 == 0:
                self.composition += " "
            self.sixteenth += 1
        else:
            if self.userInput == InputState.addNote:
                self.arrayPtr = noteArray.copy()
            else:
                self.arrayPtr = restArray.copy()
            self.userInput = InputState.increaseDuration
            self.noteSize += 1
            self.sixteenth += 1
        
    def printComposition(self):
        print(self.composition)
    
    def getCompMeasureList(self):
        result = []
        delimiter = '|'

        # This is to check if it is closed
        if self.composition.count(delimiter) == 1:
            return None

        parts = self.composition.split(delimiter)    
        substrings = [parts[i] for i in range(1, len(parts) - 1)]
    
        return substrings
        
    def getComposition(self):
            return self.composition
    
    def getFutureNote(self):
        return self.arrayPtr[self.noteSize]

    def deleteComposition(self):
        self.composition = "g$|"
        self.userInput = InputState.addRest
        self.noteSizeLimit = 15
        self.sixteenth = 1
        self.metronomeCounter = 0
        self.record = False
        self.recordCountdown = 0
        self.noteSize = 0
        self.arrayPtr = emptyArray.copy()

    def parseComposition(self):
        self.composition = self.composition.replace("ius", "o")
        self.composition = self.composition.replace("is", "o")
        self.composition = self.composition.replace("sui", "O")
        self.composition = self.composition.replace("si", "O")
        self.composition = self.composition.replace("ssss", "y")
        self.composition = self.composition.replace("ee", "n")
        self.composition = self.composition.replace("ess", "m")
        self.composition = self.composition.replace("sse", "M")
        self.composition = self.composition.replace("ss", "N")
        self.composition = self.composition.replace(" ", "")
   
    def recording(self):
        if self.record == False:
            self.recordCountdown = 20 + self.sixteenth
            self.metronomeCounter = self.sixteenth % 16
            self.record = True
            print("recording on")
        else:
            self.record = False
            if self.arrayPtr == noteArray:
                self.userInput = InputState.addNote
                self.compose()
                self.arrayPtr = restArray.copy()
            while self.sixteenth != 16:
                self.compose()
            self.compose()
            self.arrayPtr = emptyArray

            print("recording off")

    def incrementMetroCounter(self):
        self.metronomeCounter += 1
        print(f"metronomeCounter: {self.metronomeCounter}")
        if self.metronomeCounter == 16:
            self.metronomeCounter = 0
        
    def decrementCountdown(self):
        if self.recordCountdown > 0:
            self.recordCountdown -= 1



