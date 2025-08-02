from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
import sqlite3
from datetime import datetime, timedelta, date
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/')
def index():
    is_login = False
    if 'username' in session:
        is_login = True
    return render_template('index.html', is_login=is_login)

@app.route('/tutor')
def tutor():
    return render_template('tutor.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

# @app.route('/signup')
# def signup():
#     return render_template('signup.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        graduation = request.form["graduation"]

        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()

        command = "SELECT * FROM Users WHERE username = ?;"
        cursor.execute(command, (username, ))
        result = cursor.fetchone() # (testest,123,adf@gmail.com.)
        if result is None:
            command = "INSERT INTO Users (username, password,graduation) VALUES (?,?,?)"
            cursor.execute(command, (username,password,graduation,))
            conn.commit()
            conn.close()
        else:
            flash('username already exists!')
            return render_template('signup.html')


        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()
        command = "SELECT password FROM Users WHERE username = ?;"
        cursor.execute(command, (username, ))
        result = cursor.fetchone() # (123, )
        if result is None:
            flash('Username or password is wrong')
            return render_template('login.html')
        else:
            password_db = result[0]
            if password == password_db:
                session["username"] = username
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                update_command = "UPDATE Users SET recent_login =? WHERE username =?;"
                cursor.execute(update_command, (current_time, username))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
            else:
                flash('username or password is wrong')
                return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/playground')
def debug():
    return render_template('index2.html')


if __name__ == "__main__":
    app.run(debug=True, port=1867)
