from flask import Flask, session, render_template, request, jsonify, redirect, url_for, abort
from recordUserInput import Composition, InputState, emptyArray, empty_comp
from database.DBHandler import databaseManager
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secretKeyTemp"
app.permanent_session_lifetime = timedelta(days=1)
db = databaseManager("testDB")
success, error = db.connect()

# temp = Composition()
# lastInputState = InputState.addRest #this will allow the visual representation of what's being inputted work a little better

@app.context_processor
def injectNavBarDetails():
    userID = session.get("userID")
    uName = ""
    pfp = ""
    loggedIn = False
    if userID != None:
        uName = "Hello, " + session.get("username") + "!"
        # we need to make a real dynamic pfp but they're not in the db yet
        pfp = "./static/assets/img/drd.jpg"
        loggedIn = True
    else:
        uName = "Sign In"
        
        pfp = "./static/assets/img/defaultPFP.png"
    navbar_data = {
        "helloText": uName,
        "username": session.get("username"),
        "pfp": pfp,
        "loggedIn": loggedIn
    }
    return dict(navbar_data=navbar_data)  # Now `navbar_data` is available everywhere   return uName

@app.route("/")
def index():
    if session.get("userID") != None:
        if session.get("songID") == None:
            success, error, id = db.addSong(session["userID"], session["username"] + " song")
            session["songID"] = id

            db.commit()
    print("before", session.get("currentComposition"))
    if session.get("currentComposition") == None:
        session["currentComposition"] = empty_comp

    print(session.get("currentComposition"))
    print("working on song,",session.get("songID"))
    return render_template('index.html')

@app.route("/userpage/<username>")
def profile(username):
    # Do database query shit here instead of this.
    userResult, error = db.fetchUserByUsername(username)
    
    if userResult == None or userResult == []:
        abort(404, description="User not found")
    
    songsResult = db.fetchUserSongsNames(userResult[0])
    songsIDs = db.fetchUserSongsID(userResult[0])
    
    songsIDs = list(songsIDs)
    songsResult = list(songsResult)

    
    songAll = list(zip(songsIDs, songsResult))

    print(songAll)
    user_data = {
        "username": userResult[3],
        "songs": songAll
    }
    
    return render_template("userPage.html", user_data=user_data)

@app.route("/about")
def about():
    return render_template('about.html')
                        
@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/navbar")
def navbar():
    pass

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    email = request.form['email']
    password = request.form['password']
    
    result, error = db.fetchUser(email)
    if result != None:
        if (result[1] == email) and (result[2] == password):
            session.permanent = True
            session["email"] = result[1]
            session["userID"] = result[0]
            session["username"] = result[3]
            session["songID"] = None
            print("logged in as " + result[3])
        else:
            print("girl help")
            return redirect(url_for('login'))
    else:
        print("user does not exist")
        return redirect(url_for('login'))
    
    return redirect(url_for('index'))

# @app.route("/features")
# def features():
#     return render_template('features.html')

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
        success, error, user_id = db.addUser(email, password, username)
        db.commit()
        return redirect(url_for('login'))
    else:
        print("Account with that email already exists")
        return redirect(url_for('signup'))
    print("girl")
    return redirect(url_for('login'))

@app.route("/save", methods=["POST"])
def save():
    # Adding the new measures to the database
    if session.get("userID") != None and session.get("songID") != None:
        res, err = db.fetchSong(session.get("songID"))
        if res[1] != session.get("userID"):
            print("this isnt your song")
            return jsonify({"message": "This is not your song. Can't overrite it!"})

        temp = Composition(session["currentComposition"])
        measuresList = temp.getCompMeasureList()
        result, error = db.fetchSong(session.get("songID")) 
        db.clearSong(session["songID"])
        

        if measuresList != None:
            for measure in measuresList:
                db.addMeasure(session["songID"], measure)

    return jsonify({"message": "Successfully saved song! Yay!"})







@app.route("/new", methods=["POST"])
def new():
    if session.get("userID") != None:
        songName = "untitled"
        res, err, songID = db.addSong(session.get("userID"), songName)
    # return redirect(url_for('loadSong', songID = songID))
    song, err = db.fetchSong(songID)
    measureList = []
    if song[4] != None:
        for i in song[4]:
            measure, err = db.fetchMeasure(i)
            measureList.append(measure[1])
    temp = Composition(session["currentComposition"])
    temp.loadComposition(measureList)
    session["songID"] = songID
    session["currentComposition"] = temp.to_dict()
    print(session.get("currentComposition"))
    return jsonify({"message": "message"})


@app.route("/loadSong/<songID>")
def load(songID):
    song, err = db.fetchSong(songID)
    measureList = []
    if song[4] != None:
        for i in song[4]:
            measure, err = db.fetchMeasure(i)
            measureList.append(measure[1])
    temp = Composition(session["currentComposition"])
    temp.loadComposition(measureList)
    session["songID"] = songID
    session["currentComposition"] = temp.to_dict()
    print(session.get("currentComposition"))
    return redirect(url_for('index'))

@app.route("/compositionString")
def compositionString():
    temp = Composition(session['currentComposition']) # create temporary instance of class using session 
    return render_template('compositionString.html', current_composition = temp.getComposition(), future_note = temp.getFutureNote())

@app.route('/deleteRecording', methods=['POST'])
def delete_Comp():
    data = request.get_json()
    session["currentComposition"] = empty_comp
    return jsonify({'data': data}) 

@app.route("/metronome", methods=['POST'])
def handle_metronome():
    data = request.get_json()
    temp = Composition(session["currentComposition"])
    if data.get('record') == True:
        if data.get('userInput') == 1:
            temp.compose(InputState.addNote)
        elif data.get('userInput') == 2:
            temp.compose(InputState.addRest)
        else:
            temp.compose(InputState.noInput)
        temp.printComposition()
    elif data.get('record') == False: 
        while temp.sixteenth != 16:
            temp.compose(InputState.addRest)
        temp.compose(InputState.addRest)
        temp.arrayPtr = emptyArray
    else:
        print("METRONOME RECORD HANDLE ERROR")
    session["currentComposition"] = temp.to_dict() # convert temporary instance of class to dictionary and store it in session
    return jsonify({"data": data})

@app.route('/save_text', methods=['POST'])
def save_text():
    data = request.get_json()
    print(data)
    text_content = data['content']
    print(text_content)
    if session.get("userID") != None and session.get("songID") != None:
        db.changeSongName(session.get("songID"), str(text_content))

    return jsonify({"message": "Successfully saved song name! Yay!"})

@app.route("/userPage")
def userPage():
    pfp = "../static/assets/img/drd.jpg"
    name = "Dr. D"
    username = "cortana268"
    bio = "Ask me about my projector-hating laptop. Former @progressive. All views are my own"
    compositions = [{"name": "axel f crazy frog epic remix"}, {"name": "the farmer in the dell epic remix"}, {"name": "Ballade in the Form of Variations on a Norwegian Folk Song in G minor, Op. 24, TRAP REMIX"}]
    return render_template('userPage.html', pfp = pfp, name = name, username = username, bio = bio, compositions = compositions)

@app.route("/learn")
def docNotes():
    return render_template('dNotes.html')

@app.route("/learn/rests")
def docRests():
    return render_template('dRests.html')

@app.route("/learn/note_length")
def docNoteLength():
    return render_template('dNoteLength.html')

@app.route("/learn/notation")
def docNotation():
    return render_template('dNotation.html')

@app.route("/learn/time_signatures")
def docTimeSignatures():
    return render_template('dTimeSignatures.html')

if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True, use_reloader=False)
