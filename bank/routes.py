from bank import app
from flask import render_template, request, redirect, url_for, flash
from bank.models import Customer, Login, Account, Transaction, db
from datetime import datetime
from bank.forms import RegisterForm, LoginForm, AccountForm
from sqlalchemy import or_
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
def index():
    return render_template('index.html', page='index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('customer_home'))
        else:
            return render_template('login.html', page='login')
    else:
        uname = request.form.get('uname')
        password = request.form.get('password')
        role = request.form.get('role')
        remember_me = bool(request.form.get('remember_me'))
        user = db.session.query(Login).filter(Login.uname==uname, Login.role==role).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            user.last_login = datetime.now()
            db.session.commit()
            flash('Successfully Logged in.', category='success')
            if user.role == 'customer':
                return redirect(url_for('customer_home'))
            else:
                return redirect(url_for('teller_home'))
        else:
            flash('Username-Password mismatch !!', category='danger')
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        uname = form.uname.data
        password = form.password.data
        role = request.form.get('role')
        last_login = datetime.now()
        user = Login(uname=uname, password=password, role=role, last_login=last_login)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successfull ! Login to continue.', category='success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', page='register', form=form)


@app.route('/customer')
@login_required
def customer_home():
    return render_template('customer_home.html', page='customer_home')

@app.route('/customer/create', methods=['GET', 'POST'])
@login_required
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
        cust_last_update = datetime.now()           #Timestamp of creation.
        cust_status = 'Active'
        cust_message = 'Profile Created'
        customer = Customer(cust_ssn=cust_ssn, cust_name=cust_name, cust_age=cust_age, cust_addr1=cust_addr1,
                    cust_addr2=cust_addr2, cust_city=cust_city, cust_state=cust_state, cust_last_update=cust_last_update, cust_status=cust_status, cust_message=cust_message)
        db.session.add(customer)
        db.session.commit()
        flash('Customer creation initiated successfull !.', category='info')
        return redirect(url_for('customer_home'))
    else:
        return render_template('create_customer.html', page='create_customer', form=form)


@app.route('/customer/update', methods=['GET', 'POST'])
@login_required
def update_customer():
    customer = None
    errors = None
    if request.method == 'POST':
        errors = {}
        cust_id = request.form.get('cust_id')
        cust_name = request.form.get('cust_name')
        cust_age = request.form.get('cust_age')
        cust_addr1 = request.form.get('cust_addr1')
        customer = db.session.query(Customer).filter(Customer.cust_id == cust_id).first()
        if cust_name.strip() == '':
            errors['cust_name'] = 'Invalid name'
        if cust_addr1.strip() == '':
            errors['cust_addr1'] = 'Invalid address'
        if cust_age.strip() == '' or not cust_age.isnumeric():
            errors['cust_age'] = 'Invalid age'
        if not errors:
            customer.cust_name = cust_name
            customer.cust_age = cust_age
            customer.cust_addr1 = cust_addr1
            customer.cust_message = 'Profile Updated'
            customer.cust_last_update = datetime.now()
            db.session.commit()
            flash('Customer update initiated successfully', category='info')
        else:
            flash('You need to fix the errors in order to update', category='danger')
    else:
        cust_id = request.args.get('cust_id', -1)
        if cust_id != -1:
            cust_ssn = request.args.get('cust_ssn')
            if cust_ssn.strip() == '' and cust_id.strip() == '':
                flash("Either one is mandatory and must be a 9-digit number", category='danger')
            else:
                customer = db.session.query(Customer).filter(or_(Customer.cust_ssn == cust_ssn, Customer.cust_id == cust_id)).first()
                if customer:
                    flash("Customer Found !", category='success')
                else:
                    flash("No customer found with the given ID", category='warning')
    return render_template('update_customer.html', page='update_customer', customer=customer, errors=errors)


@app.route('/customer/delete', methods=['GET', 'POST'])
@login_required
def delete_customer():
    customer = None
    if request.method == 'POST':
        cust_id = request.form.get('cust_id')
        customer = db.session.query(Customer).filter(Customer.cust_id == cust_id).first()
        if customer.cust_status == 'Deleted':
            customer.cust_status = 'Active'
            customer.cust_message = 'Profile Reactivated'
            flash('Customer reactivate initiated successfully', category='info')
        else:
            customer.cust_status = 'Deleted'
            customer.cust_message = 'Profile Deleted'
            flash('Customer delete initiated successfully', category='info')
        customer.cust_last_update = datetime.now()
        db.session.commit()
        return redirect(url_for('customer_home'))
    else:
        cust_id = request.args.get('cust_id', -1)
        if cust_id != -1:
            cust_ssn = request.args.get('cust_ssn')
            if cust_ssn.strip() == '' and cust_id.strip() == '':
                flash("Either one is mandatory and must be a 9-digit number", category='danger')
            else:
                customer = db.session.query(Customer).filter(or_(Customer.cust_ssn == cust_ssn, Customer.cust_id == cust_id)).first()
                if customer:
                    flash("Customer Found !", category='success')
                else:
                    flash("No customer found with the given ID", category='warning')

    return render_template('delete_customer.html', page='delete_customer', customer=customer)


@app.route('/customer/status')
@login_required
def customer_status():
    customers = db.session.query(Customer).all()
    return render_template('customer_status.html', page='customer_status', customers=customers)


@app.route('/account/create', methods=['GET', 'POST'])
@login_required
def create_account():
    form = AccountForm()
    cust_ids = db.session.query(Customer.cust_id).all()
    if form.validate_on_submit():
        cust_id = int(form.cust_id.data)
        acnt_type = form.acnt_type.data
        deposit_amnt = form.deposit_amnt.data
        acnt_last_tr_date = datetime.now()
        acnt_status = 'Active'
        acnt_message = 'Account Created'
        account = Account(cust_id=cust_id, acnt_type=acnt_type, acnt_balance=deposit_amnt,
                         acnt_last_tr_date=acnt_last_tr_date, acnt_status=acnt_status, acnt_message=acnt_message)
        db.session.add(account)
        db.session.commit()
        flash('Account creation initiated successfull !.', category='info')
        return redirect(url_for('customer_home'))
    else:
        return render_template('create_account.html', page='create_account', form=form, cust_ids=cust_ids)


@app.route('/account/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
    account = None
    if request.method == 'POST':
        acnt_id = int(request.form.get('acnt_id'))
        account = db.session.query(Account).filter(Account.acnt_id == acnt_id).first()
        print(account.acnt_status)
        if account.acnt_status == 'Deleted':
            account.acnt_status = 'Active'
            account.acnt_message = 'Account Reactivated'
            flash('Account reactivate initiated successfully', category='info')
        else:
            account.acnt_status = 'Deleted'
            account.acnt_message = 'Account Deleted'
            flash('Account delete initiated successfully', category='info')
        account.acnt_last_tr_date = datetime.now()
        db.session.commit()
        return redirect(url_for('customer_home'))
    else:
        all_acnt_ids = db.session.query(Account.acnt_id).all()
        acnt_id = request.args.get('acnt_id', '-1')
        if acnt_id != '-1':
            account = db.session.query(Account).filter(Account.acnt_id == acnt_id).first()
            if account:
                flash("Account Found !", category='success')
        else:
            flash("Select an account ID from dropdown to search", category='danger')

    return render_template('delete_account.html', page='delete_account', acnt_ids=all_acnt_ids, account=account)

@app.route('/account/status')
@login_required
def account_status():
    accounts = db.session.query(Account).all()
    return render_template('account_status.html', page='account_status', accounts=accounts)

@app.route('/teller')
@login_required
def teller_home():
    return render_template('teller_home.html', page='teller_home')


@app.route('/teller/account_details', methods=['GET', 'POST'])
@login_required
def account_details():
    key = None
    account = None
    if request.method == 'POST':
        cust_id = request.form.get('cust_id')
        acnt_id = request.form.get('acnt_id')
        if acnt_id.strip() == '' and cust_id.strip() == '':
                flash("Either one is mandatory", category='danger')
        else:
            account = db.session.query(Account).filter(Account.acnt_id == acnt_id).first()
            if account:
                key = 'acnt_id'
                flash("Account Found !", category='success')
            else:
                account = db.session.query(Account.acnt_id, Account.acnt_type).filter(Account.cust_id == cust_id).all()
                if account:
                    key = 'cust_id'
                    flash("Customer found. Choose Account to continue.", category='info')
                else:
                    flash("Sorry, No accounts matching your query", category='danger')
    return render_template('account_details.html', page='account_details', key=key, account=account)


@app.route('/teller/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    account = None
    prev_balance = None
    tr_amount = None
    if request.method == 'POST':
        acnt_id = request.form.get('acnt_id')
        tr_amount = request.form.get('tr_amount')
        if not tr_amount.isnumeric():
            flash("Not a valid amount", "danger")
        else:
            account = db.session.query(Account).filter(Account.acnt_id == int(acnt_id)).first()
            prev_balance = account.acnt_balance
            account.acnt_balance += int(tr_amount)
            account.acnt_last_tr_date = datetime.now()
            account.acnt_message = '₹. {} Deposited'.format(tr_amount)
            db.session.commit()
            flash("Amount deposited successfully", category="success")
    else:
        acnt_id = request.args.get('acnt_id')
    return render_template('deposit.html', page='account_details', tr_amount=tr_amount, acnt_id=acnt_id, prev_balance=prev_balance, account=account)


@app.route('/teller/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    account = None
    prev_balance = None
    tr_amount = None
    if request.method == 'POST':
        acnt_id = request.form.get('acnt_id')
        tr_amount = request.form.get('tr_amount')
        if not tr_amount.isnumeric():
            flash("Not a valid amount", "danger")
        else:
            account = db.session.query(Account).filter(Account.acnt_id == int(acnt_id)).first()
            prev_balance = account.acnt_balance
            if prev_balance < int(tr_amount) :
                flash("Insufficient balance ! Choose a smaller amount", category="warning")
            else:
                account.acnt_balance -= int(tr_amount)
                account.acnt_last_tr_date = datetime.now()
                account.acnt_message = '₹. {} Withdrawn'.format(tr_amount)
                db.session.commit()
                flash("Amount withdrawn successfully", category="success")
    else:
        acnt_id = request.args.get('acnt_id')
    return render_template('withdraw.html', page='account_details', tr_amount=tr_amount, acnt_id=acnt_id, prev_balance=prev_balance, account=account)



@app.route('/teller/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    tr_history = None
    if request.method == 'POST':
        cust_id = request.form.get('cust_id')
        src_acnt = request.form.get('src_acnt')
        trgt_acnt = request.form.get('trgt_acnt')
        tr_amount = request.form.get('tr_amount')
        if src_acnt == '-1':
            flash("Select source account to initiate transfer", category="danger")
        elif trgt_acnt == '-1':
            flash("Select target account to initiate transfer", category="danger")
        elif not tr_amount.isnumeric():
            flash("Not a valid amount", category="danger")
        else:
            tr_amount = int(tr_amount)
            account_src = db.session.query(Account).filter(Account.acnt_id == src_acnt).first()
            if tr_amount > account_src.acnt_balance:
                flash("Insufficient balance ! Choose a smaller amount", category="warning")
            else:
                account_src.acnt_balance -= tr_amount
                account_trgt = db.session.query(Account).filter(Account.acnt_id == trgt_acnt).first()
                account_trgt.acnt_balance += tr_amount
                account_src.acnt_message = '-₹. {} Transfered'.format(tr_amount)
                account_trgt.acnt_message = '+₹. {} Transfered'.format(tr_amount)
                account_src.acnt_last_tr_date = datetime.now()
                account_trgt.acnt_last_tr_date = datetime.now()
                db.session.commit()
                flash("Amount transfered successfully !", category="success")
                tr_history = {}
                tr_history['src'] = {'acnt_id':src_acnt, 'prev_bal':account_src.acnt_balance+tr_amount,
                                    'tr_amount':tr_amount, 'crnt_bal':account_src.acnt_balance}
                tr_history['trgt'] = {'acnt_id':trgt_acnt, 'prev_bal':account_trgt.acnt_balance-tr_amount,
                                    'tr_amount':tr_amount, 'crnt_bal':account_trgt.acnt_balance}

    cust_id = request.args.get('cust_id')
    src_account = db.session.query(Account.acnt_id, Account.acnt_type).filter(Account.cust_id == cust_id).all()
    src_acnt_ids = [acnt[0] for acnt in src_account]
    trgt_account = db.session.query(Account.acnt_id).filter(Account.acnt_id.notin_(src_acnt_ids)).all()
    return render_template('transfer.html', page='account_details', cust_id=cust_id, src_account=src_account, trgt_account=trgt_account, tr_history=tr_history)



@app.route('/teller/statement')
@login_required
def statement():
    return render_template('statement.html', page='statement')


@app.route('/api/acnt_api')
def acnt_api():
        acnt_id = int(request.args.get('acnt_id'))
        account = db.session.query(Account).filter(Account.acnt_id == acnt_id).first()
        return render_template('includes/acnt_api.html', account=account)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))