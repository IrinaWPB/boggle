from itsdangerous import json
from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify


app = Flask(__name__)
app.config["SECRET_KEY"] = "gfhgf"

boggle_game = Boggle()

@app.route('/')
def show_board():
    """Homepage. Shows board"""
    
    board = boggle_game.make_board()
    session['board'] = board
    times_played = session.get("times_played", 0)
    return render_template('board.html', board = board, times_played = times_played)

@app.route('/check-word')
def check_word():
    """Checks if the word is valid"""

    word = request.args["word"]
    board = session['board']
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result' : result})

@app.route('/score', methods=["GET","POST"])
def score_count():
    """Checks if the score is higher than record and if so saves it. 
       Updates number of games played"""

    times_played = session.get("times_played", 0)
    session["times_played"] = times_played + 1

    score = request.json["score"]
    highest_score = session.get("highest_score", 0)
    if score > highest_score:
        session["highest_score"] = score 
    
    return jsonify(new_record = score > highest_score)
        
