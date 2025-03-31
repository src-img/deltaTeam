from recordUserInput import Composition, modifyComposition, InputState

class CompositionVector:
    def __init__(self):
        self.metronomeCounter = 2 # syncs with track that has recording on 
        self.compositions = []  #list of all compositions
        self.compositionPointer = 0 
        self.mutePointer = 0
        self.mute = False
        self.record = False

    def recording(self, trackNumber): # only 1 record button can be active 
        if self.record == False:
            self.metronomeCounter = self.compositions[trackNumber].sixteenth
            self.compositionPointer = trackNumber
            self.record = True
        elif self.record == True and self.compositionPointer != trackNumber:
            self.compositionPointer = trackNumber
        else:
            self.record = False

    def incrementMetroCounter(self):
        self.metronomeCounter += 1
        if self.metronomeCounter == 16:
            self.metronomeCounter = 0
    
    def modifyCurrentComposition(self):
        if self.record == True:
            self.compositions[self.compositionPointer].compose()

    def modifyCurrentCompositionState(self, keyPress):
        if keyPress == 'a':
            self.compositions[self.compositionPointer].userInput = InputState.addNote
        elif keyPress == 's':
            self.compositions[self.compositionPointer].userInput = InputState.addRest

    def newComposition(self, comp = "g$|"):
        self.compositions.append(Composition(comp)) 

    def printCurrentComposition(self):
        self.compositions[self.compositionPointer].printComposition()
    
    def getCurrentComposition(self):
        return self.compositions[self.compositionPointer].getComposition()

    def getCurrentCompositionFuture(self):
         return self.compositions[self.compositionPointer].getFutureNote()

    def clearTrack(self, trackNumber):
        self.compositions[trackNumber].deleteComposition()

    def removeTrack(self, trackNumber):
        self.compositions.pop(trackNumber)

    def getMeasureCurrentComposition(self):
        return self.compositions[self.compositionPointer].getCompMeasureList()

    def mute(self, trackNumber):
        if self.mute == False:
            self.mutePointer = trackNumber
            self.mute = True
        elif self.mute == True and self.mutePointer != trackNumber:
            self.mutePointer = trackNumber
        else:
            self.mute = False

    def getUnmutedComposition(self):
        return self.compositions[self.mutePointer].getComposition()
    
    # def loadCompositions() # will load comps from DB and create corresponding tracks on noteSkeleton
