import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TCS_Case_Study_1'