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

    word = request.args['word']
    board = session['board']

    used_words = session['used-words']
    used_words.append(word)
    session['used-words'] = used_words

    result = boggle_game.check_valid_word(board, word)

    return jsonify({'result': result})
