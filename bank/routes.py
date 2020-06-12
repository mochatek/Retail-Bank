from bank import app
from flask import render_template, request, redirect, url_for, flash
from bank.models import User, db
from datetime import datetime
from sqlalchemy import and_

@app.route('/')
def index():
    return render_template('index.html', page='Index')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', page='Login')
    else:
        uname = request.form.get('uname')
        password = request.form.get('password')
        is_cust = int(request.form.get('is_cust'))
        user = db.session.query(User).filter(User.uname==uname, User.is_cust==is_cust).first()
        if user and user.check_password(password):
            flash('Successfully Logged in.')
            return redirect(url_for('index'))
        else:
            flash('Username-Password mismatch !!')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', page='Register')
    else:
        ssnid = request.form.get('ssnid')
        uname = request.form.get('uname')
        age = request.form.get('age')
        addr1 = request.form.get('addr1')
        addr2 = request.form.get('addr2')
        city = request.form.get('city')
        state = request.form.get('state')
        is_cust = 1                         #Used to distinguish between tellet & customer.
        created = datetime.now()            #Timestamp of creation.
        password = request.form.get('password')
        user = User(ssnid=ssnid, uname=uname, age=age, addr1=addr1,
                    addr2=addr2, city=city, state=state, is_cust=is_cust, created=created)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successfull ! Login to continue.')
        return redirect(url_for('login'))
