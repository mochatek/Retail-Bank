from bank import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bank import login

@login.user_loader
def load_user(id):
    return db.session.query(Login).filter(Login.id==int(id)).first()

class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True)
    cust_ssn = db.Column(db.Integer, index=True, unique=True)
    cust_name = db.Column(db.String(20), index=False, unique=False)
    cust_age = db.Column(db.Integer, index=False, unique=False)
    cust_addr1 = db.Column(db.Text, index=False, unique=False)
    cust_addr2 = db.Column(db.Text, index=False, unique=False, nullable=True)
    cust_city = db.Column(db.String(20), index=False, unique=False)
    cust_state = db.Column(db.String(20), index=False, unique=False)
    cust_last_update = db.Column(db.Date, index=False, unique=False)
    cust_status = db.Column(db.String(20), index=False, unique=False)
    cust_message = db.Column(db.String(20), index=False, unique=False)
    account = db.relationship('Account', backref='customer')


class Login(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20), index=False, unique=True)
    password = db.Column(db.String(128), index=False, unique=False)
    role = db.Column(db.String(20), index=False, unique=False)
    last_login = db.Column(db.DateTime, index=False, unique=False)

    def set_password(self, password):
        self.password= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Account(db.Model):
    acnt_id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    acnt_type = db.Column(db.String(20), index=False, unique=False)
    acnt_balance = db.Column(db.Integer, index=False, unique=False)
    acnt_status = db.Column(db.String(20), index=False, unique=False)
    acnt_last_tr_date = db.Column(db.DateTime, index=False, unique=False)
    acnt_message = db.Column(db.String(20), index=False, unique=False)
    transaction = db.relationship('Transaction', backref='customer')


class Transaction(db.Model):
    tr_id = db.Column(db.Integer, primary_key=True)
    tr_amount = db.Column(db.Integer, index=False, unique=False)
    tr_type = db.Column(db.String(20), index=False, unique=False)
    tr_date = db.Column(db.DateTime, index=False, unique=False)
    tr_src= db.Column(db.Integer, db.ForeignKey('account.acnt_id'))
    tr_trgt= db.Column(db.Integer, index=False, unique=False)