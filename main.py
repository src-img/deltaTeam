from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from recordUserInput import Composition, modifyComposition, InputState
from database.DBHandler import databaseManager
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secretKeyTemp"
app.permanent_session_lifetime = timedelta(days=1)
db = databaseManager("testDB")
success, error = db.connect()


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


@app.route("/keyboard_event", methods=['POST'])
def handle_keyboard_event():
    data = request.get_json()
    keyPressed = data.get("key")
    if keyPressed == 'a':
        temp.userInput = InputState.addNote
    elif keyPressed == 's':
        temp.userInput = InputState.addRest
    print(f"Key pressed: {keyPressed}")

    # Adding the new measures to the database
    if session.get("userID") != None and session.get("songID") != None:
        measuresList = temp.getCompMeasureList()
        result, error = db.fetchSong(session.get("songID"))
        print(result, "result of song")
        songMeasureLen = 0

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
    record = request.get_json()
    global recording 
    if recording == True:
        recording = False
        print(f"recording off")
    else:
        recording= True
        print(f"recording on")
    
    data = recording
    return jsonify({'recording': data})

@app.context_processor
def inject_composition():
    return dict(current_composition = temp.getComposition()) 

@app.route("/metronome", methods=['POST'])
def handle_metronome():
    data = request.get_json()
    print("metronome received")
    if recording == True:
        modifyComposition(temp)
    inject_composition()
    return jsonify({'message': 'Data received', 'data': data})


if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True)
