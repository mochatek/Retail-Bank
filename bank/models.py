from bank import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssnid = db.Column(db.Integer, index=True, unique=True)
    uname = db.Column(db.String(50), index=False, unique=False)
    age = db.Column(db.Integer, index=False, unique=False)
    addr1 = db.Column(db.Text, index=False, unique=False)
    addr2 = db.Column(db.Text, index=False, unique=False)
    city = db.Column(db.String(50), index=False, unique=False)
    state = db.Column(db.String(50), index=False, unique=False)
    is_cust = db.Column(db.Integer, index=False, unique=False)
    created = db.Column(db.Date, index=False, unique=False)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'User : {}'.format(self.uname)