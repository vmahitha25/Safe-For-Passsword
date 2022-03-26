from app import login_manager
from app import db
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='account_dp.png')
    password = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(4), nullable=False)
    posts = db.relationship('Data', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone}','{self.image_file}')"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segment_name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Data('{self.segment_name}', '{self.username}', '{self.password}')"



