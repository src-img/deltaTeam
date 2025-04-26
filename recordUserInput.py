
from enum import Enum
import random

class InputState(Enum):
    addNote = 1
    addRest = 2
    noInput = 3

noteArray = ["s","e","i","q","qUs","j","jUs","h","hUs","hUe","hUi","d","dUs","dUe","dui","w"]
restArray = ["S","E","I","Q","QS","J","JS","H","HS","HE","HI","D","DS","DE","DI","W"]
emptyArray = ["",""]
empty_comp = {'composition': 'g$|', 'sixteenth': 0, 'noteSizeLimit': 15, 'noteSize': 0, 'arrayPtr': emptyArray}

class Composition:
    def __init__(self, empty_comp):
        for key, value in empty_comp.items():
            setattr(self, key, value)

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

    def compose(self, state):
        if self.arrayPtr == emptyArray:
            if state == InputState.addNote:
                self.arrayPtr = noteArray.copy()
            else:
                self.arrayPtr = restArray.copy()
            self.setNoteSizeLimit()
            self.noteSize = 0
            self.sixteenth = 1
        else:
            if state == InputState.addNote or self.noteSize == self.noteSizeLimit or (state == InputState.addRest and self.arrayPtr != restArray):
                self.composition += self.arrayPtr[self.noteSize]
                match state:
                    case InputState.noInput:
                        if self.arrayPtr == noteArray:
                            self.composition += "U"
                    case InputState.addNote:
                        self.arrayPtr = noteArray.copy()
                    case InputState.addRest:
                        self.arrayPtr = restArray.copy()
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

    def printComposition(self):
        print(self.composition)
    
    def getCompMeasureList(self):
        result = []
        comp = self.composition.replace("v", "U|" ) # handles "v" case
        delimiter = '|'

        # This is to check if it is closed
        if comp.count(delimiter) == 1:
            return None

        parts = comp.split(delimiter)
        substrings = [parts[i] for i in range(1, len(parts) - 1)]
    
        return substrings

    def loadComposition(self, measureList):
        result = "g$|"
        for measure in measureList.values():
            if measure[-1] == "U": # if end of measure is 'U' then it deletes'U' and adds 'v'
                measure = measure[:-1]
                result += measure
                result += 'v'
            else:   
                result += measure
                result += '|'
        self.composition = result
        
    def getComposition(self):
            return self.composition
    
    def getFutureNote(self):
        return self.arrayPtr[self.noteSize]

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

    def to_dict(self):
        return self.__dict__.copy()

