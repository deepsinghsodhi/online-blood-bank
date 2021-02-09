from flask import  Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager,current_user


# Import the Permissions object
from flask_permissions.core import Permissions

app=Flask(__name__)

app.config['SECRET_KEY'] = 'secret_string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_new = 'login'
login_manager.login_message_category = 'info'

perms = Permissions(app, db, current_user)

from application import routes