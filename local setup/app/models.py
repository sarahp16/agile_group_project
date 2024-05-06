from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UsersInfo(db.Model):
    __tablename__ = 'UsersInfo'
    name = db.Column(db.String(100), nullable = False)
    surname = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(90), unique = True, primary_key = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    suburb = db.Column(db.String(50), nullable = False)
