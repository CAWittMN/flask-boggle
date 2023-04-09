from boggle import Boggle
from flask import Flask, redirect, render_template, session, request, make_response, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "boopydoop"

#debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def home_page():
    return render_template('/base.html')

@app.route('/game')
def home_board():
    score = session["score"]
    words = session["used-words"]
    board = session['board']
    if board == None:
        return redirect('/')
    return render_template('/game.html', board=board, score=score, words=words)

@app.route('/initialize-game', methods=["POST"])
def initialize_game():
    board = boggle_game.make_board()
    session['board'] = board
    session['used-words'] = []
    session['score'] = 0
    return redirect('/game')

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

@app.route('/get-score')
def get_score():
    score = session["score"]
    return jsonify(score)

@app.route('/post-score', methods=["POST"])
def post_score():

    score = request.json["score"]
    session['score'] = score

    return jsonify(score)


@app.route('/end-game')
def end_game():
    endGame = request.args['endgame']
    if endGame == 'endgame':
        score = session['score']
        words = session["used-words"]
        return render_template('/end.html', score=score, words=words)
    return redirect('/')
