from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from recordUserInput import Composition, modifyComposition, InputState
from database.DBHandler import databaseManager
from datetime import timedelta
import time

app = Flask(__name__)
app.secret_key = "secretKeyTemp"
app.permanent_session_lifetime = timedelta(days=1)
db = databaseManager("testDB")
success, error = db.connect()
global recording
recording = False
js_version = 1.0
global quarterNoteMs
global lastTap #relative to last tap <3
global startedTaps #bool so the first note isnt borked
startedTaps = False
global recordee
recordee = ""

@app.route("/")
def index():
    if session.get("userID") != None:
        if session.get("songID") == None:
            success, error, id = db.addSong(session["userID"], session["username"] + " song")
            session["songID"] = id
            db.commit()
        
     
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')
                        
@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    email = request.form['username']
    password = request.form['password']
    
    result, error = db.fetchUser(email)
    if result != None:
        if (result[1] == email) and (result[3] == password):
            session.permanent = True
            session["userID"] = result[0]
            session["username"] = result[2]
            session["songID"] = None
            print("logged in as " + result[2])
        else:
            return redirect(url_for('login'))
    else:
        print("user does not exist")
        return redirect(url_for('login'))
    
    return redirect(url_for('index'))

@app.route("/features")
def features():
    return render_template('features.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_submit():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']
    
    # checking for duplicate accounts
    result, error = db.fetchUser(email)
    if result == None:
        success, error, user_id = db.addUser(email, username, password)
        db.commit()
        return redirect(url_for('login'))
    else:
        print("Account with that email already exists")
        return redirect(url_for('signup'))
    
    return redirect(url_for('login'))


temp = Composition()

@app.route("/jinja")
def jinja():
    global js_version
    js_version += .1
    print(js_version)
    # inject_version()
    # data = {temp.getComposition()}
    return render_template('jinja.html', js_version=js_version)

@app.route("/keyboard_event", methods=['POST'])
def handle_keyboard_event():
    data = request.get_json()
    keyPressed = data.get("key")
    global startedTaps
    global lastTap
    global quarterNoteMs
    noteType = ""
    print(recording)
    print("help!")
    
    if recording == True:
        print("we made it here")
        if startedTaps == False:
            startedTaps = True
            #lastTap = time.time()
        
        print(lastTap)
        thisTap = time.time()
        
        if lastTap:
            elapsed_time = (thisTap - lastTap) * 1000
            print(f"Elapsed Time: {elapsed_time}")
            print(f"quarter note: {quarterNoteMs}")

            match (elapsed_time / quarterNoteMs):
                case num if 0 <= num < 0.375:
                    noteType = "S"
                case num if 0.375 <= num < 0.75:
                    noteType = "E"
                case num if 0.75 <= num < 1.5:
                    noteType = "Q"
                case num if 1.5 <= num < 3:
                    noteType = "H"
                case num if 3 <= num < 6:
                    noteType = "W"
                case _:
                    noteType = "W"
        else:
            print("girl help i have no frame of reference for time elapsed because you broke lastTap")

        lastTap = thisTap
        print(f"Current recordee value: {recordee}")
        return jsonify({"noteType": noteType, "recordee": recordee})

    
    # # Adding the new measures to the database
    # if session.get("userID") != None and session.get("songID") != None:
    #     measuresList = temp.getCompMeasureList()
    #     result, error = db.fetchSong(session.get("songID"))
    #     print(result, "result of song")
    #     songMeasureLen = 0

    #     if result[4] != None:
    #         songMeasureLen = len(result[4])
    #     #print(songMeasureLen)
        
    #     print("measures list: ", measuresList)
    #     if measuresList != None:
    #         if len(measuresList) > songMeasureLen:
    #             print("measures list of songLen: ", measuresList[songMeasureLen])
    #             db.addMeasure(session["songID"], measuresList[songMeasureLen])


@app.route('/recording', methods=['POST'])
def toggle_record():
    global startedTaps
    global recording
    global recordee
    data = request.get_json()
    #recording = request.get_json()
    if recording == True:
        recording = False
        print(f"recording off")
        startedTaps = False
        recordee = ""
    else:
        if (recordee == ""): recordee = data.get('recordee') #element that's recording
        recording = True
        print(f"recording on")
    
    return jsonify({'recording': recording})

@app.context_processor
def inject_composition():
    return dict(current_composition = temp.getComposition()) 

@app.route("/metronome", methods=['POST'])
def handle_metronome():
    data = request.get_json()
    #print(data)
    #print("metronome received")
    global quarterNoteMs
    global lastTap
    quarterNoteMs = data.get('quarterNoteMS')
    #print ("quarternotems " + str(data.get('quarterNoteMS')))
    if (startedTaps == False):
        lastTap = time.time()
    
    # if recording == True:
    modifyComposition(temp)
    inject_composition()
    return jsonify({'message': 'Data received', 'data': data})


if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True)
