from enum import Enum
import random

class InputState(Enum):
    addNote = 1
    addRest = 2
    increaseDuration = 3

noteArray = ["s","e","i","q","qUs","j","jUs","h","hUs","hUe","hUi","d","dUs","dUe","dui","w"]
restArray = ["S","E","I","Q","QS","J","JS","H","HS","HE","HI","D","DS","DE","DI","W"]

class Composition:
    def __init__(self, composition = "g$|"):
        self.composition = composition
        self.userInput = InputState.addRest
        self.sixteenth = self.setSixteenth(composition)
        self.noteSizeLimit = self.setNoteSizeLimitInit(self.sixteenth)
        self.noteSize = 0
        self.arrayPtr = restArray.copy()

    def setSixteenth(self, composition):
        sixteenth = 1
        sixteenth += composition.count('s')
        sixteenth += composition.count('S')
        sixteenth += 2 * composition.count('e')
        sixteenth += 2 * composition.count('E')
        sixteenth += 3 * composition.count('i')
        sixteenth += 3 * composition.count('I')
        sixteenth += 4 * composition.count('q')
        sixteenth += 4 * composition.count('Q')
        sixteenth += 6 * composition.count('j')
        sixteenth += 6 * composition.count('J')
        sixteenth += 8 * composition.count('h')
        sixteenth += 8 * composition.count('H')
        sixteenth += 12 * composition.count('d')
        sixteenth += 12 * composition.count('D')
        sixteenth += 16 * composition.count('w')
        sixteenth += 16 * composition.count('W')
        sixteenth += 4 * composition.count('o')
        sixteenth += 4 * composition.count('O')
        sixteenth += 4 * composition.count('y')
        sixteenth += 4 * composition.count('n')
        sixteenth += 4 * composition.count('N')
        sixteenth += 4 * composition.count('m')
        sixteenth += 4 * composition.count('M')
        sixteenth = sixteenth % 16
        return sixteenth

    def setNoteSizeLimitInit(self, sixteenth):
        match ((sixteenth-1) % 4):
            case 0: 
                noteSizeLimit = 15 - ((sixteenth-1) % 16)
            case 1:
                noteSizeLimit = 1
            case 2:
                noteSizeLimit = 1
            case 3:
                noteSizeLimit = 0
        return noteSizeLimit

    def setNoteSizeLimit(self):
        match ((self.sixteenth) % 4):
            case 0: 
                self.noteSizeLimit = 15 - ((self.sixteenth) % 16)
            case 1:
                self.noteSizeLimit = 1
            case 2:
                self.noteSizeLimit = 1
            case 3:
                self.noteSizeLimit = 0

    def compose(self):
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
        if self.sixteenth == 16:
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

    def clearComposition(self):
        self.__init__()

    def parseComposition(self):
        self.composition = self.composition.replace("is", "o")
        self.composition = self.composition.replace("si", "O")
        self.composition = self.composition.replace("ssss", "y")
        self.composition = self.composition.replace("ee", "n")
        self.composition = self.composition.replace("ss", "N")
        self.composition = self.composition.replace("ess", "m")
        self.composition = self.composition.replace("sse", "M")
        self.composition = self.composition.replace(" ", "")

def modifyComposition(Composition):
    newComposition = Composition
    newComposition.compose()
    newComposition.printComposition()
    print(f"noteSize = {newComposition.noteSize}")
    print(f"noteSizeLimit = {newComposition.noteSizeLimit}")
    print(f"sixteenth = {newComposition.sixteenth}")

