from boggle import Boggle
from flask import Flask, redirect, render_template, session, request, make_response, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "boopydoop"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def home_board():

    board = boggle_game.make_board()
    session['board'] = board
    session['used-words'] = []

    return render_template('/index.html', board=board)

@app.route('/check-word')
def check_word():
    board = session['board']
    word = request.args['word']
    used_words = session['used-words']
    result = boggle_game.check_valid_word(board, word)
    if result == 'ok':
        if word in used_words:
            result = "already-used"
        else:
            used_words.append(word)
            session['used-words'] = used_words
    return jsonify({'result': result})

@app.route('/get-words')
def get_words():
    words = session['used-words']
    return jsonify(words)

