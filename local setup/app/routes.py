from flask import Flask, render_template, redirect, url_for, request, session, flash
from app.forms import RegistrationForm, LoginForm, UsersInfo, QuestForm, Quests, HintsSolutions, PlayerTracker
import sqlalchemy as sa
from app import app, db
from flask_login import current_user, login_user, logout_user

@app.route('/')
@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/user')
def user():
    return render_template('user.html', name =current_user.name)

#@app.route('/homepage')
#def homepage():
    #if current_user.is_authenticated:
        #return render_template('homepage.html')
    #else:
        #return redirect(url_for('login'))

@app.route('/play/find_game')
def find_game():
    return render_template('find_game.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = QuestForm()
    if form.validate_on_submit():
        new_quest = Quests(title=form.q_title.data, duration=form.q_duration.data, difficulty=form.difficulty.data, suburb=form.quest_suburb.data, completion=form.completed.data)
        db.session.add(new_quest)
        db.session.commit()
        new_quest_id = new_quest.id
        new_hintsolution = HintsSolutions(hint_text = form.hint_1.data, solution_text = form.solution_1.data, quest_id = new_quest_id)
        db.session.add(new_hintsolution)
        db.session.commit()
        new_hintsolution1 = HintsSolutions(hint_text = form.hint_2.data, solution_text = form.solution_2.data, quest_id = new_quest_id)
        db.session.add(new_hintsolution1)
        db.session.commit()
        new_hintsolution2 = HintsSolutions(hint_text = form.hint_3.data, solution_text = form.solution_3.data, quest_id = new_quest_id)
        db.session.add(new_hintsolution2)
        db.session.commit()
        new_hintsolution3 = HintsSolutions(hint_text = form.hint_4.data, solution_text = form.solution_4.data, quest_id = new_quest_id)
        db.session.add(new_hintsolution3)
        db.session.commit()
        new_hintsolution4 = HintsSolutions(hint_text = form.hint_5.data, solution_text = form.solution_5.data, quest_id = new_quest_id)
        db.session.add(new_hintsolution4)
        db.session.commit()
        return redirect(url_for('user'))
    return render_template('create2.html', form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = UsersInfo(name = form.name.data, surname = form.surname.data, email = form.email.data, password = form.password.data, city = form.city.data, suburb = form.suburb.data)
        db.session.add(new_user)
        db.session.commit()
        new_player = PlayerTracker(user_id = new_user.id, points = form.points.data, quests_completed = form.quests_completed.data)
        db.session.add(new_player)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(UsersInfo).where(UsersInfo.email == form.email.data))
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('login'))
        if user.password == form.password.data:
            login_user(user)
            return redirect(url_for('user'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base'))
