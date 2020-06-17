from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms import ValidationError
from bank.models import Login, db

def only_number(form, field):
        if not field.data.isnumeric():
            raise ValidationError('Only numbers are Allowed.')

def valid_amount(form, field):
        try:
            val = int(field.data)
        except:
            raise ValidationError('Not a valid amount')

def must_be_unique(form, field):
        user = db.session.query(Login).filter(Login.uname==field.data).first()
        if user:
            raise ValidationError('Sorry! This username is already taken.')

class RegisterForm(FlaskForm):
    cust_ssn = StringField('Customer SSN', validators=[DataRequired(message='Mandatory'), Length(min=9, max=9, message='Enter a valid 9-digit SSN ID'), only_number])
    cust_name = StringField('Name', validators=[DataRequired(message='Mandatory')])
    cust_age = StringField('Age', validators=[DataRequired(message='Mandatory'), Length(min=2, max=3, message='Enter a valid age'), only_number])
    cust_addr1 = TextAreaField('Address lane 1', validators=[DataRequired(message='Mandatory')])
    cust_addr2 = TextAreaField('Address lane 2',)
    cust_city = StringField('City', validators=[DataRequired(message='Mandatory')])
    cust_state = StringField('State', validators=[DataRequired(message='Mandatory')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired(message='Mandatory'), Length(min=8, message='Minimum 8 characters needed'), Regexp('^\w+$', message="Must be Alphanumeric"), must_be_unique])
    password = PasswordField('Password', validators=[DataRequired(message='Mandatory'), Length(min=10, message='Minimum 10 characters needed'), Regexp('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', message="Must contain atleast 1 number, uppercase letter and special character")])

class AccountForm(FlaskForm):
    acnt_type = SelectField('Account Type', choices=[('Current','current'), ('Savings', 'savings')])
    deposit_amnt = StringField('Deposit Amount', validators=[DataRequired(message='Mandatory'), valid_amount])
    submit = SubmitField('Submit')