from flask import Flask, render_template, request, redirect, url_for
from elasticstuff import login

loginConnection = login.Login()

def login():

    return render_template('login.html')

def loginapi():

    username = request.form['username']
    password = request.form['password']

    is_logged_in = loginConnection.loginCheck(username,password)

    password = ""
    return is_logged_in
