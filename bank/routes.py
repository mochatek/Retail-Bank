from flask import render_template, request, redirect, url_for, flash

@app.route('/')
def index():
    return "<h1>Home</h1>"