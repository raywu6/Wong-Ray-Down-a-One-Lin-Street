import sqlite3 #stdlib
from os import urandom #stdlib

from flask import Flask, render_template, request, session, redirect, url_for, flash #pip install flask

from util import create_db


app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/register_auth', methods = ['POST'])
def register_auth():
    '''This function checks the form on the signup page and calls register() to register the user into the database.'''
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    confirmed_pass = request.form['confirmedPassword']
    if username == "":
        flash("Please make sure to enter a username!")
        return redirect(url_for('register'))
    elif password == "":
        flash("Please make sure to enter a password!")
        return redirect(url_for('register'))
    elif password != confirmed_pass: # checks to make sure two passwords entered are the same
        flash("Please make sure the passwords you enter are the same.")
        return redirect(url_for('register'))
    else:
        if create_db.register(username, password, name):
            flash("You have successfully registered.")
        else:
            flash("Please enter another username. The one you entered is already in the database.")
            return redirect(url_for('register'))
    return redirect('/login')

@app.route("/login")
def login():
    '''This function renders the HTML template for the login page.'''
    return render_template('login.html')

@app.route('/login_auth', methods = ['POST'])
def login_auth():
    '''This function calls authenticate() to check if the form's username and password match the database. If successful, this function redirects the user to the home page.'''
    username = request.form['username']
    password = request.form['password']

    if create_db.authenticate(username, password):
        session['username'] = username
        flash("You have successfully logged in.")
        return redirect('/')
    else:
        flash("Invalid username and password combination")
        return render_template('login.html')

@app.route('/logout')
def logout():
    '''This function removes the username from the session, logging the user out. Redirects user to home page.'''
    session.pop('username') # ends session
    flash("You have successfully logged out.")
    return redirect('/')

@app.route("/search")
def search():
    return "hi"

@app.route("/user")
def user():
    return "hi"

@app.route("/fin_aid")
def fin_aid():
    return "hi"

@app.route("/college")
def college():
    return "hi"

if __name__ == "__main__":
    app.debug = True
    create_db.setup() #setup database
    app.run()
