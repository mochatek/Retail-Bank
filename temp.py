from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

print(generate_password_hash('mocha'))

print(datetime.now())