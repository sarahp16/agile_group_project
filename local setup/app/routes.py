from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from app.forms import RegistrationForm, LoginForm, UsersInfo, QuestForm, Quests, HintsSolutions, PlayerTracker, CompletedQuests
import sqlalchemy as sa
from app import app, db
from flask_login import current_user, login_user, logout_user

@app.route('/')
@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/user')
def user():
    # Getting player rank in city to return on dashboard
    user_city = current_user.city
    players_info = UsersInfo.query.filter_by(city=user_city).all()
    players_with_points = []
    for player_info in players_info:
        player = PlayerTracker.query.filter_by(user_id=player_info.id).first()
        if player:
            players_with_points.append({'name': player_info.name, 'points': player.points})
    # Sorting players by points in descending order to get the player's ranking
    sorted_players = sorted(players_with_points, key=lambda x: x['points'], reverse=True)
    for i, player in enumerate(sorted_players):
        if player['name'] == current_user.name:
            user_rank = i + 1
    # Querying respective databases for points, number of quests completed and number of quests created
    user_points = db.session.scalar(sa.select(PlayerTracker.points).where(PlayerTracker.user_id == current_user.id))
    completed = db.session.scalar(sa.select(PlayerTracker.quests_completed).where(PlayerTracker.user_id == current_user.id))
    created = db.session.query(sa.func.count(Quests.creator_id)).filter(Quests.creator_id == current_user.id).scalar()
    return render_template('user.html', name =current_user.name, points = user_points, quests_completed = completed, rank = user_rank, quests_created = created)

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/filter_users', methods=['GET'])
def filter_users():
    city = request.args.get('city')
    suburb = request.args.get('suburb')
    
    # Joining PlayerTracker and UsersInfo tables to retrieve user data
    query = db.session.query(PlayerTracker, UsersInfo).join(UsersInfo, PlayerTracker.user_id == UsersInfo.id)
    
    # Filtering by city and suburb if provided
    if city:
        query = query.filter(UsersInfo.city == city)
    if suburb:
        query = query.filter(UsersInfo.suburb == suburb)
    
    # Sorting users based on points in descending order to determine their rank
    query = query.order_by(PlayerTracker.points.desc())
    
    # Fetching all users with their corresponding points and additional information
    users_data = query.all()
    
    # Serializing user data including rank, name, and points
    serialized_users = [{'rank': idx + 1, 'name': user_info.name, 'points': player_tracker.points, 'user_id': player_tracker.user_id} for idx, (player_tracker, user_info) in enumerate(users_data)]
    
    return jsonify(serialized_users)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = QuestForm()
    if form.validate_on_submit():
        # Adding Quest information to Quest database table
        new_quest = Quests(title=form.q_title.data, duration=form.q_duration.data, difficulty=form.difficulty.data, suburb=form.quest_suburb.data, creator_id = current_user.id)
        db.session.add(new_quest)
        db.session.commit()
        new_quest_id = new_quest.id
        # Adding each individual Hint and Solution data to the HintsSolutions database table
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
        # Storing new user information in UsersInfo database table
        new_user = UsersInfo(name = form.name.data, surname = form.surname.data, email = form.email.data, password = form.password.data, city = form.city.data, suburb = form.suburb.data)
        db.session.add(new_user)
        db.session.commit()
        # Creating an instance of this user in PlayerTracker 
        new_player = PlayerTracker(user_id = new_user.id, points = form.points.data, quests_completed = form.quests_completed.data)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Checking Email submitted is the same as email in database
        user = db.session.scalar(sa.select(UsersInfo).where(UsersInfo.email == form.email.data))
        if user is None:
            flash('Invalid email or password!')
            return redirect(url_for('login'))
        # Checking password submitted is the same as the password in the database
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

@app.route('/filter', methods=['GET'])
def filter_quests():
    # Taking filtered column values
    duration = request.args.get('duration')
    difficulty = request.args.get('difficulty')
    suburb = request.args.get('suburb')
    # Querying for Completed Quests
    completed_quest_ids = [completed_quest.quest_id for completed_quest in CompletedQuests.query.filter_by(user_id=current_user.id).all()]
    # Querying for Created Quests
    created_quests_ids = [created_quest.id for created_quest in Quests.query.filter_by(creator_id=current_user.id).all()]
    #Creating a set of completed and created quests to exclude
    excluded_quest_ids = set(completed_quest_ids + created_quests_ids)
    # Excluding previous step from final filter 
    filtered_quests_query = Quests.query.filter(~Quests.id.in_(excluded_quest_ids))

    if duration:
        filtered_quests_query = filtered_quests_query.filter(Quests.duration == duration)
    if difficulty:
        filtered_quests_query = filtered_quests_query.filter(Quests.difficulty == difficulty)
    if suburb:
        filtered_quests_query = filtered_quests_query.filter(Quests.suburb == suburb)

    #Creating JSON response to AJAX request 
    filtered_quests = filtered_quests_query.all()
    serialized_quests = [{'id': quest.id, 'title': quest.title, 'difficulty': quest.difficulty, 'duration': quest.duration, 'suburb': quest.suburb} for quest in filtered_quests]

    return jsonify(serialized_quests)



@app.route('/play/<int:quest_id>/<int:hint_id>', methods=['GET', 'POST'])
def quest(quest_id, hint_id):
    # Getting all necessary Quest, Hint and Solution data based on selected quest
    quest_title = Quests.query.filter_by(id=quest_id).with_entities(Quests.title).scalar()
    all_hints = HintsSolutions.query.filter_by(quest_id=quest_id).all()
    quest_hints_solutions = []
    i = 0
    # Creating hint id and appending required information to quests_hints_solutions list
    for hint in all_hints:
        i += 1
        quest_hints_solutions.append({'hint_id': i, 'quest_hint': hint.hint_text, 'quest_solution': hint.solution_text.lower()})

    quest = next((h for h in quest_hints_solutions if h['hint_id'] == hint_id), None)
    
    # Creating heart counter, initially setting to 3 otherwise returning the current heart counters value
    if 'heart_count' not in session or request.method == 'GET':
        session['heart_count'] = 3

    heart_count = session['heart_count']

    # When user submits answer
    if request.method == 'POST':
        user_answer = request.form.get('answer', '').lower()
        quest_answer = quest['quest_solution']
        # Check if answers match 
        if user_answer == quest_answer:
            # If answers match, based on heart counter the number of points awarded to user, updates PlayerTracker table in database
            player = PlayerTracker.query.filter_by(user_id=current_user.id).first()
            if heart_count == 3:
                flash("Correct! +5 points!")
                player.points += 5
                db.session.commit()
            elif heart_count == 2:
                flash("Correct! +3 points!")
                player.points += 3
                db.session.commit()
            else:
                flash("Correct! +1 point!")
                player.points += 1
                db.session.commit()
            # Gets next hint id and redirects to next hint's html
            next_hint_id = hint_id + 1
            if next_hint_id <= len(quest_hints_solutions):
                return redirect(url_for('quest', quest_id=quest_id, hint_id=next_hint_id))
            else:
                # If the quest is completed, number of quests increases by 1 and redirects to Play route
                player = PlayerTracker.query.filter_by(user_id=current_user.id).first()
                if player:
                    player.quests_completed += 1
                    db.session.commit()
                new_completion = CompletedQuests(quest_id=quest_id, user_id=current_user.id)
                db.session.add(new_completion)
                db.session.commit()
                session.pop('selected_quest', None)
                return redirect(url_for('play'))
        else:
            # If user gets question wrong, heart counter decreases while greater than 0
            if session['heart_count'] > 0:
                session['heart_count'] -= 1
                heart_count = session['heart_count']
            # If user's heart are at 0, automatically sends user to next question
            if session['heart_count'] == 0:
                flash("No tries left! Onto the next hint.")
                next_hint_id = hint_id + 1
                if next_hint_id <= len(quest_hints_solutions):
                    return redirect(url_for('quest', quest_id=quest_id, hint_id=next_hint_id))
                else:
                    return redirect(url_for('play'))
            flash("Incorrect!")
                
    return render_template('quest.html', quest=quest, title=quest_title, hint_id=hint_id, quest_id=quest_id, heart_count=heart_count, hint_number = hint_id)
