rom flask import Flask, render_template, redirect, url_for, request, session, flash
from app.forms import RegistrationForm, LoginForm, UsersInfo, QuestForm, Quests, Hints, Solutions
import sqlalchemy as sa
from app import app, db
from flask_login import login_required, current_user, login_user, logout_user

@app.route('/')
@app.route('/homepage')
@login_required
def homepage():
    if current_user.is_authenticated:
        return render_template('homepage.html')
    else:
        return redirect(url_for('login'))

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
    form = QuestForm()
    if form.validate_on_submit():
        new_quest = Quests(title=form.q_title.data, duration=form.q_duration.data, difficulty=form.difficulty.data, suburb=form.quest_suburb.data, completion=form.completed.data)
        db.session.add(new_quest)
        db.session.commit()
        for i in range(6):
            hint_text = form.hints[i].data
            solution_text = form.solutions[i].data
            if hint_text or solution_text:
                new_hint = Hints(hint_text=hint_text, quest=new_quest)
                db.session.add(new_hint)
                db.session.commit()
                new_solution = Solutions(solution_text=solution_text, quest=new_quest, hint=new_hint)
                db.session.add(new_solution)
                db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('create.html', form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = UsersInfo(name = form.name.data, surname = form.surname.data, email = form.email.data, password = form.password.data, city = form.city.data, suburb = form.suburb.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(UsersInfo).where(UsersInfo.email == form.email.data))
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('login'))
        if user.password == form.password.data:
            login_user(user)
            return redirect(url_for('homepage'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))
