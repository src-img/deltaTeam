
from enum import Enum
import random

class InputState(Enum):
    addNote = 1
    addRest = 2
    increaseDuration = 3


noteArray = ["S","E","E.","Q","Q+S","Q.","Q.+S","H","H+S","H+E","H+E.","H.","H.+S","H.+E","H.+E.","W"]
restArray = ["s","e","e.","q","q+s","q.","q.+s","h","h+s","h+e","h+e.","h.","h.+s","h.+e","h.+e.","w"]

class Composition:
    def __init__(self):
        self.composition = "|"
        self.userInput = InputState.addRest
        self.noteSizeLimit = 15
        self.sixteenth = 1
        self.quarter = 1
        self.noteSize = 0
        self.arrayPtr = restArray.copy()
        


    # def randomMeasureGenerator(self):
    #     randomState = random.randint(1,10)
    #     if randomState == 1:
    #         self.userInput = InputState.addNote
    #     elif randomState == 2:
    #         self.userInput = InputState.addRest
    #     else:
    #         self.userInput = InputState.increaseDuration

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
        #self.randomMeasureGenerator()
        if self.userInput == InputState.addNote or self.noteSize == self.noteSizeLimit or self.userInput == InputState.addRest and self.arrayPtr != restArray:
            self.composition += self.arrayPtr[self.noteSize]
            match self.userInput:
                case InputState.increaseDuration:
                    if self.arrayPtr == noteArray:
                        self.composition += "+"
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
            self.composition += "|"
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
    
def modifyComposition(Composition):
    newComposition = Composition
    
    newComposition.compose()

    newComposition.printComposition()

# if __name__ == "__main__":
#     modifyComposition()
