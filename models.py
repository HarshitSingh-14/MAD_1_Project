from flask_login import UserMixin
from . import db
from tkinter import CASCADE


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    city = db.Column(db.String(150))
    course = db.relationship('Course')
    log = db.relationship('Log')


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    course_type = db.Column(db.String(150))
    settings = db.Column(db.String(150))
    log = db.relationship('Log')
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id" ,ondelete='CASCADE'))



class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(150))
    value = db.Column(db.Integer)
    notes = db.Column(db.String(150))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id',ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'))
    added_date_time = db.Column(db.String(150))
