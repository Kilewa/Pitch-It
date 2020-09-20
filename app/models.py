from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(240))
    email = db.Column(db.String(240), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(240))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship('Pitch', backref='user', lazy="dynamic")
    # comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    # post_likes = db.relationship('PostLikes', backref=db.backref('user', lazy='joined'),
    # lazy='dynamic', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'


class Pitch(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    pitch = db.Column(db.String(1000))
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # comments= db.relationship('Comment', backref='title', lazy='dynamic')
    # ser_likes = db.relationship('PostLikes', backref=db.backref('post', lazy='joined'),
    #                          lazy='dynamic', cascade='all, delete-orphan')
    # def __init__(self,id,title,pitch):
    #     self.id = id
    #     self.title = title
    #
    #     self.pitch = pitch

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls, id):
        pitches = Pitch.query.order_by(Pitch.posted.desc())
        return pitches


class Comment(db.Model):

    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(240))
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    # def __init__(self,id,title,comment):
    #     self.id = id
    #
    #     self.comment = comment

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments
