from flask import Flask, render_template, request, jsonify, redirect, url_for
from recordUserInput import Composition, modifyComposition, InputState
from database.DBHandler import databaseManager

app = Flask(__name__)
db = databaseManager("testDB")
success, error = db.connect()


@app.route("/")
def index():
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
    confirm_password = request.form['confirm_password']
    
    success, error, user_id = db.addUser(email, username, password)
    db.commit()
    print(error)
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
    return jsonify({"message": "Key received successfully"})


@app.route("/metronome", methods=['POST'])
def handle_metronome():
    data = request.get_json()
    print("metronome received")
    modifyComposition(temp)
    return jsonify({'message': 'Data received', 'data': data})


if __name__ == "__main__":
    app.run(debug=True)
