from bank import app
from flask import render_template, request, redirect, url_for, flash
from bank.models import User, db
from datetime import datetime
from bank.forms import RegisterForm

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
    form = RegisterForm()
    if form.validate_on_submit():
        ssnid = form.ssnid.data
        uname = form.uname.data
        age = form.age.data
        addr1 = form.addr1.data
        addr2 = form.addr2.data
        city = form.city.data
        state = form.state.data
        is_cust = 1                         #Used to distinguish between tellet & customer.
        created = datetime.now()            #Timestamp of creation.
        password = form.password.data
        user = User(ssnid=ssnid, uname=uname, age=age, addr1=addr1,
                    addr2=addr2, city=city, state=state, is_cust=is_cust, created=created)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successfull ! Login to continue.')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', page='Register', form=form)
