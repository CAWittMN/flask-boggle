from boggle import Boggle
from flask import Flask, redirect, render_template, session, request, make_response
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "boopydoop"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def home_board():

    board = boggle_game.make_board()
    session['board'] = board

    return render_template('/index.html', board=board)

@app.route('/check-word')
def check_word():
