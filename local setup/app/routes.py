from flask import Flask, render_template, url_for
from app import app 


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/play/find_game')
def find_game():
    return render_template('find_game.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/create')
def create():
    return render_template('create.html')
