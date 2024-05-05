from flask import Flask, render_template, url_for, request, redirect, session, flash
from app import app, db
from app.forms import RegistrationForm
from app.models import Users

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

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        city = form.city.data
        suburb = form.suburb.data

        new_user = Users(name = name, surname = surname, email = email, password = password, city = city, suburb = suburb)

        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('/login'))
    return render_template('registration.html', title = 'Register', form = form)
