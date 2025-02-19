from flask import Flask, render_template, request, jsonify
from importFunction import Composition, modifyComposition

app = Flask(__name__)

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

@app.route("/features")
def features():
    return render_template('features.html')


temp = Composition()

@app.route("/metronome", methods=['POST'])
def handle_metronome():
    data = request.get_json()
    print("metronome received")
    modifyComposition(temp)
    return jsonify({'message': 'Data received', 'data': data})


if __name__ == "__main__":
    app.run(debug=True)
