from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from miniproject import route

app = Flask(__name__)
app.config['SECRET_KEY'] = '4f2bfa6592418c6a7e50573998ce99db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uszpawccfbwmuc:91e25b7436cc84e899a928cab32b8563c439c89310b6a5af4d7ee5b1a1e64619@ec2-3-225-213-67.compute-1.amazonaws.com:5432/dacnk9n22snsps'
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

db = SQLAlchemy(app)
if __name__ == '__main__':
    app.run(debug=True)

