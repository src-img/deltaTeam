from flask import Flask, session, render_template, request, jsonify, redirect, url_for, abort
from recordUserInput import Composition, InputState, emptyArray, empty_comp
from database.DBHandler import databaseManager
from datetime import timedelta



testString = "g$|nnsmeUs|jEnUovoUNEjevMnnn|nnyy|eEnUnmv"


# measure list that should be stored in db after .getCompMeasureList() 
testMeasureList = ["nnsmeUs", "jEnUoU", "oUNEjeU", "Mnnn", "nnyy", "eEnUnmU"]

temp = Composition(empty_comp)
temp.composition = testString
temp.printComposition()

print("measureList to DB: ", temp.getCompMeasureList())
temp.composition = ""

# takes in list Measurelist and turns it back into original testString
temp.loadComposition(testMeasureList)
temp.printComposition()
