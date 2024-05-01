from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "TOP_SECRET"

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)  # Print out the HTTP method used
    if request.method == 'POST':
        try:
            user_details = request.form
            email = user_details['email']
            password = user_details['password']

            connection = pymysql.connect(**db_params)
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
                    user = cursor.fetchone()
            finally:
                connection.close()

            if user:
                session['user'] = {
                    'id': user[0],
                    'email': user[1],
                    'password': user[2]
                }
                print(session['user'])  # Add this line for debugging
                flash('Logged in successfully!', 'success')
                return redirect(url_for('main'))
            else:
                flash('Invalid email or password.', 'danger')
        except Exception as e:
            flash('An error occurred while logging in: {}'.format(str(e)), 'danger')

    return render_template('login.html')