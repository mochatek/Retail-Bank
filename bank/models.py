from bank import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    # login = db.relationship('Login', backref='customer')
    account = db.relationship('Account', backref='customer')


class Login(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    # cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    uname = db.Column(db.String(20), index=False, unique=True)
    password = db.Column(db.String(128), index=False, unique=False)
    role = db.Column(db.String(20), index=False, unique=False)
    last_login = db.Column(db.DateTime, index=False, unique=False)

    def set_password(self, password):
        self.password= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'User : {}'.format(self.uname)

class Account(db.Model):
    acnt_id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    acnt_type = db.Column(db.String(20), index=False, unique=False)
    acnt_balance = db.Column(db.Float, index=False, unique=False)
    acnt_last_tr_date = db.Column(db.Date, index=False, unique=False)
    acnt_status = db.Column(db.String(20), index=False, unique=False)


class Transaction(db.Model):
    tr_id = db.Column(db.Integer, primary_key=True)
    tr_amount = db.Column(db.Float, index=False, unique=False)
    tr_date = db.Column(db.Date, index=False, unique=False)
    tr_src= db.Column(db.Integer, index=False, unique=False)
    tr_trgt= db.Column(db.Integer, index=False, unique=False)