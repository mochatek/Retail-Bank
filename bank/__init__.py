from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# CSRF Protection
csrf = CSRFProtect(app)

# DB Connection
db = SQLAlchemy(app)

# ORM Migartion
migrate = Migrate(app, db)

# Auth-Session middleware
login  = LoginManager(app)
login .login_view = 'login'

from bank import routes, models