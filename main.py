from flask import Flask, session, render_template, request, jsonify, redirect, url_for, abort
from recordUserInput import Composition, InputState, emptyArray
from database.DBHandler import databaseManager
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secretKeyTemp"
app.permanent_session_lifetime = timedelta(days=1)
db = databaseManager("testDB")
success, error = db.connect()

temp = Composition()
lastInputState = InputState.addRest #this will allow the visual representation of what's being inputted work a little better

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
        
    return render_template('index.html')

@app.route("/userpage/<username>")
def profile(username):
    # Do database query shit here instead of this.
    userResult, error = db.fetchUserByUsername(username)
    
    if userResult == None or userResult == []:
        abort(404, description="User not found")
    
    songsResult = db.fetchUserSongsNames(userResult[0])
    print(songsResult)
    
    user_data = {
        "username": userResult[3],
        "songs": songsResult
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
    email = request.form['username']
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
        success, error, user_id = db.addUser(email, password, username)
        db.commit()
        return redirect(url_for('login'))
    else:
        print("Account with that email already exists")
        return redirect(url_for('signup'))
    print("girl")
    return redirect(url_for('login'))

@app.route("/compositionString")
def compositionString():
    return render_template('compositionString.html', current_composition = temp.getComposition(), future_note = temp.getFutureNote())

@app.route('/grabInputType')
def grabInputType():
    global lastInputState
    if(temp.userInput == lastInputState):
        if(temp.userInput == InputState.addNote):
            data = 1
        elif(temp.userInput == InputState.addRest):
            data = 2
    else:
        if(lastInputState == InputState.addNote):
            data = 1
        elif(lastInputState == InputState.addRest):
            data = 2
    
    return jsonify({'state': data})

@app.route('/deleteRecording', methods=['POST'])
def delete_Comp():
    data = request.get_json()
    temp.deleteComposition()
    return jsonify({'data': data}) 

@app.route("/metronome", methods=['POST'])
def handle_metronome():
    data = request.get_json()

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

    return jsonify({"data": data})

@app.route("/userPage")
def userPage():
    pfp = "../static/assets/img/drd.jpg"
    name = "Dr. D"
    username = "cortana268"
    bio = "Ask me about my projector-hating laptop. Former @progressive. All views are my own"
    compositions = [{"name": "axel f crazy frog epic remix"}, {"name": "the farmer in the dell epic remix"}, {"name": "Ballade in the Form of Variations on a Norwegian Folk Song in G minor, Op. 24, TRAP REMIX"}]
    return render_template('userPage.html', pfp = pfp, name = name, username = username, bio = bio, compositions = compositions)

if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True, use_reloader=False)
