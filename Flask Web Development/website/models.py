from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Create a schema to store some Notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default=func.now())
    # set up the foreign key(To relate table - Notes with table - User)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# User info will be stored in a schema that looks like this
class User(db.Model, UserMixin): #Set up the user model
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    first_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    notes = db.relationship('Note') # Relate the notes a specific user created to his/her Info