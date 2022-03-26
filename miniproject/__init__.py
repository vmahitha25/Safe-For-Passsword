from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '4f2bfa6592418c6a7e50573998ce99db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rskkyznpypxish:ed51c3a5aefab53431eff455ea03a032a07fd1dc021212400543a0048b167e81@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d30nj5bvs0a6j2'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from miniproject import route
