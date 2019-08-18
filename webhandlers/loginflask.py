from flask import Flask, render_template, request, redirect, url_for, flash
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
        return redirect(url_for('viewassets'))

    flash("login failed")
    return redirect(url_for('login'))

def changepassword():
    return render_template('changepassword.html')

def changepasswordapi():

    old_password = request.form['old_password']
    new_password = request.form['new_password']
    new_password_repeat = request.form['new_password_repeat']

    if new_password != new_password_repeat:
        flash("!passwords dont match!")
        return redirect(url_for('changepassword'))

    else:
        username = user_instance.get_id()
        correct_existing_password = userConnection.comparePassword(username, old_password)

        if not correct_existing_password:
            flash("!incorrect existing password!")
            return redirect(url_for('changepassword'))

        else:
            userConnection.updateUser(username, new_password)
            flash("success")
            return render_template('viewassets.html')
