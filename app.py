from boggle import Boggle
import os
from flask import Flask, redirect, render_template, session, request, make_response, jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "boopydoop")

#debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def home_page():
    """Show home page"""

    return render_template('/base.html')

@app.route('/game')
def show_game():
    """Show game board and info"""

    score = session.get("score")
    words = session.get("used-words")
    board = session.get('board')

    if board == None:
        return redirect('/')
    
    return render_template('/game.html', board=board, score=score, words=words)

@app.route('/initialize-game', methods=["POST"])
def initialize_game():
    """Initialize session data on server"""

    board = boggle_game.make_board()

    session['board'] = board
    session['used-words'] = []
    session['score'] = 0

    return redirect('/game')

@app.route('/check-word')
def check_word():
    """Check submitted word and update used words"""

    board = session.get('board')
    word = request.args.get('word')
    used_words = session.get('used-words')

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
    """gets the used words from the server"""

    words = session['used-words']

    return jsonify(words)

@app.route('/get-score')
def get_score():
    """gets the score from the server"""

    score = session["score"]

    return jsonify(score)

@app.route('/post-score', methods=["POST"])
def post_score():
    """post score to server"""

    score = request.json["score"]
    session['score'] = score

    return jsonify(score)


@app.route('/end-game')
def end_game():
    """end game page"""

    endGame = request.args['endgame']

    if endGame == 'endgame':
        score = session['score']
        words = session["used-words"]

        return render_template('/end.html', score=score, words=words)
    
    return redirect('/')
