from bank import app
from flask import render_template, request, redirect, url_for, flash
from bank.models import Customer, Login, Account, Transaction, db
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
        role = request.form.get('role')
        user = db.session.query(Login).filter(Login.uname==uname, Login.role==role).first()
        # if user and user.check_password(password):
        if user:
            flash('Successfully Logged in.')
            return redirect(url_for('customer_home'))
        else:
            flash('Username-Password mismatch !!')
        return redirect(url_for('login'))


@app.route('/customer')
def customer_home():
    return render_template('customer_home.html', page='customer_home')

@app.route('/customer/create', methods=['GET', 'POST'])
def create_customer():
    form = RegisterForm()
    if form.validate_on_submit():
        cust_ssn = form.cust_ssn.data
        cust_name = form.cust_name.data
        cust_age = form.cust_age.data
        cust_addr1 = form.cust_addr1.data
        cust_addr2 = form.cust_addr2.data
        cust_city = form.cust_city.data
        cust_state = form.cust_state.data
        # is_cust = 1                                  Used to distinguish between tellet & customer.
        cust_last_update = datetime.now()            #Timestamp of creation.
        # uname = form.uname.data
        # password = form.password.data
        customer = Customer(cust_ssn=cust_ssn, cust_name=cust_name, cust_age=cust_age, cust_addr1=cust_addr1,
                    cust_addr2=cust_addr2, cust_city=cust_city, cust_state=cust_state, cust_last_update=cust_last_update)

        # user = Login(cust_id=customer.cust_id, uname=uname, is_cust=is_cust)
        # user.set_password(password)

        db.session.add(customer)
        # db.session.add(user)
        db.session.commit()
        flash('Customer Registration successfull !.')
        return redirect(url_for('customer_home'))
    else:
        return render_template('create_customer.html', page='create_customer', form=form)

@app.route('/customer/update')
def update_customer():
    return render_template('update_customer.html', page='update_customer')

@app.route('/customer/delete')
def delete_customer():
    return render_template('delete_customer.html', page='delete_customer')

@app.route('/customer/status')
def customer_status():
    return render_template('customer_status.html', page='customer_status')

@app.route('/account/create')
def create_account():
    return render_template('create_account.html', page='create_account')

@app.route('/account/delete')
def delete_account():
    return render_template('delete_account.html', page='delete_account')

@app.route('/account/status')
def account_status():
    return render_template('account_status.html', page='account_status')

@app.route('/logout')
def logout():
    return 'logout'