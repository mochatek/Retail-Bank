from bank import app
from flask import render_template, request, redirect, url_for, flash

@app.route('/')
def index():
    return render_template('index.html', page='Index')

@app.route('/login')
def login():
    return render_template('login.html', page='Login')

@app.route('/register')
def register():
    return render_template('register.html', page='Register')