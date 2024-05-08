from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class UsersInfo(UserMixin, db.Model):
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    surname: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True, primary_key = True)
    password: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    suburb: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    
    def get_password(email):
        user = UsersInfo.query.filter_by(email=email).first()
        if user:
            return user.password
        else:
            return None
