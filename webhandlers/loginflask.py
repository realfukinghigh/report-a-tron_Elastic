from flask import Flask, render_template, request, redirect, url_for
from elasticstuff import login
import flask_login

user_instance = login.User()
userConnection = login.Login()

def user_loader(username):
    user_check = userConnection.checkUserExists(username)
    if user_check == False:
        return

    else:
        user = user_instance
        user.id = username
        if user.is_authenticated:
            return user

def login():
	return render_template('login.html')

def loginapi():
    username = request.form['username']
    password = request.form['password']
    try:
        success_log_in = userConnection.comparePassword(username, password)
    except:
        success_log_in = False

    if success_log_in:
        user = user_instance
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('createasset'))

    return redirect(url_for('login'))
