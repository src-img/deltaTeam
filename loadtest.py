from flask import Flask, session, render_template, request, jsonify, redirect, url_for, abort
from recordUserInput import Composition, InputState, emptyArray, empty_comp
from database.DBHandler import databaseManager
from datetime import timedelta



testString = "g$|nnsmeUs|jEnUovoUNEjevMnnn|nnyy|eEnUnmv"

testMeasureList = {0: "nnsmeUs", 1: "jEnUoU", 2: "oUNEjeU", 3: "Mnnn", 4: "nnyy", 5: "eEnUnmU"}

temp = Composition(empty_comp)
temp.composition = testString
temp.printComposition()


toDB = temp.getCompMeasureList()
print("measureList to DB: ", temp.getCompMeasureList())
temp.composition = ""
temp.loadComposition(testMeasureList)
temp.printComposition()
