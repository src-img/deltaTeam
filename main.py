from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from database.DBHandler import databaseManager
from datetime import timedelta
from compositionVector import CompositionVector

app = Flask(__name__)
app.secret_key = "secretKeyTemp"
app.permanent_session_lifetime = timedelta(days=1)
db = databaseManager("testDB")
success, error = db.connect()
temp2 = CompositionVector()
temp2.newComposition()

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

@app.route("/compositionString")
def compositionString():
    return render_template('compositionString.html', current_composition = temp2.getCurrentComposition(), future_note = temp2.getCurrentCompositionFuture())

@app.route("/keyboard_event", methods=['POST'])
def handle_keyboard_event():
    data = request.get_json()
    temp2.modifyCurrentCompositionState(data.get("key"))
    print(f"keyboard just tapped! metronome counter: {temp2.metronomeCounter} sixteenth: {temp2.compositions[0].sixteenth} ")

    # Adding the new measures to the database
    if session.get("userID") != None and session.get("songID") != None:
        measuresList = temp.getCompMeasureList()
        result, error = db.fetchSong(session.get("songID")) 
        songMeasureLen = 0        

        if result != []:
            if result[4] != None:
                songMeasureLen = len(result[4])
        #print(songMeasureLen)
        
        print("measures list: ", measuresList)
        if measuresList != None:
            if len(measuresList) > songMeasureLen:
                print("measures list of songLen: ", measuresList[songMeasureLen])
                db.addMeasure(session["songID"], measuresList[songMeasureLen])


    return jsonify({"message": "Key received successfully"})

@app.route('/recording', methods=['POST'])
def toggle_record():
    data = request.get_json() 
    temp2.recording(0) # 0 temporary needs data.trackNumber
    if temp2.record == True:
        print("recording!") #temporary
    else:
        print("recording off!")
    return jsonify({'recording': ''})

@app.route('/deleteTrack', methods=['POST'])
def delete_Comp():
    data = request.get_json() 
    temp2.removeTrack(0) # 0 temporary needs data.trackNumber
    return jsonify({'deleteTrack': "track Deleted"}) 

@app.route('/clearTrack', methods=['POST']) 
def clear_track():
    data = request.get_json()
    temp2.clear_track(0) # 0 temporary needs data.trackNumber
    return jsonify({'clearTrack': "cleared track"})

@app.route("/modifyComp", methods=['GET'])
def modify_Comp():
    temp2.modifyCurrentComposition()
    temp2.printCurrentComposition()
    return jsonify({"data": "modified Comp"})

@app.route("/metronome", methods=['GET'])
def handle_metronome():
    temp2.incrementMetroCounter()
    return jsonify({"currentNote": temp2.metronomeCounter})

@app.route("/mute", methods=['GET'])
def toggle_mute():
    data.get_json()
    temp2.mute(0) # 0 temporary needs data.trackNumber
    return jsonify({"muteTrack": "mute"})

@app.route("/compositionGrab", methods=['POST'])
def compGrab():
    return jsonify({'composition': temp2.getUnmutedComposition()})

if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True, use_reloader=False)
