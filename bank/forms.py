from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError

def only_number(form, field):
        if not field.data.isnumeric():
            raise ValidationError('Only numbers are Allowed.')

class RegisterForm(FlaskForm):
    ssnid = StringField('SSN ID', validators=[DataRequired(message='Mandatory'), Length(min=9, max=9, message='Enter a valid 9-digit SSN ID'), only_number])
    uname = StringField('Username', validators=[DataRequired(message='Mandatory')])
    age = StringField('Age', validators=[DataRequired(message='Mandatory'), Length(min=2, max=3, message='Enter a valid age'), only_number])
    addr1 = TextAreaField('Address lane 1', validators=[DataRequired(message='Mandatory')])
    addr2 = TextAreaField('Address lane 2', validators=[DataRequired(message='Mandatory')])
    city = StringField('City', validators=[DataRequired(message='Mandatory')])
    state = StringField('State', validators=[DataRequired(message='Mandatory')])
    password = PasswordField('Password', validators=[DataRequired(message='Mandatory'), Length(min=6, message='Minimum 6 digits needed')])
    submit = SubmitField('Register')
