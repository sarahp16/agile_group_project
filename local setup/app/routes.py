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
    user_city = current_user.city
    players_info = UsersInfo.query.filter_by(city=user_city).all()
    players_with_points = []
    for player_info in players_info:
        player = PlayerTracker.query.filter_by(user_id=player_info.id).first()
        if player:
            players_with_points.append({'name': player_info.name, 'points': player.points})
    sorted_players = sorted(players_with_points, key=lambda x: x['points'], reverse=True)
    for i, player in enumerate(sorted_players):
        if player['name'] == current_user.name:
            user_rank = i + 1
    user_points = db.session.scalar(sa.select(PlayerTracker.points).where(PlayerTracker.user_id == current_user.id))
    completed = db.session.scalar(sa.select(PlayerTracker.quests_completed).where(PlayerTracker.user_id == current_user.id))
    return render_template('user.html', name =current_user.name, points = user_points, quests_completed = completed, rank = user_rank)

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/leaderboard')
def leaderboard():
    user_city = current_user.city
    players_info = UsersInfo.query.filter_by(city=user_city).all()
    players_with_points = []
    for player_info in players_info:
        player = PlayerTracker.query.filter_by(user_id=player_info.id).first()
        if player:
            players_with_points.append({'name': player_info.name, 'points': player.points})
    sorted_players = sorted(players_with_points, key=lambda x: x['points'], reverse=True)
    return render_template('leaderboard.html', city=user_city, players=sorted_players)

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
