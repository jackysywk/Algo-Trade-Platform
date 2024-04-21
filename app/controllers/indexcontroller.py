from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User ## import kelas User dari model

@app.route('/', methods = ['GET'])
def index():
    if current_user.is_authenticated:

        user = current_user.username
    else:
        user = "anonymous"
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user(username)
        if user and user.verify_password(password):
            login_user(user)
            print("Successful Login")
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))