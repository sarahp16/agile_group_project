from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import ForeignKey
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class UsersInfo(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    surname: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    suburb: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    
    def get_password(email):
        user = UsersInfo.query.filter_by(email=email).first()
        if user:
            return user.password
        else:
            return None

@login.user_loader
def load_user(id):
    return db.session.get(UsersInfo, id)



class Quests(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(200), index = True)
    duration: so.Mapped[str] = so.mapped_column(sa.String(100), index = True)
    difficulty: so.Mapped[str] = so.mapped_column(sa.String(100), index = True)
    suburb: so.Mapped[str] = so.mapped_column(sa.String(100), index = True)
    completion: so.Mapped[bool] = so.mapped_column(sa.Boolean, default = False)

    hints: so.WriteOnlyMapped['Hints'] = so.relationship(back_populates='quest')
    solutions: so.WriteOnlyMapped['Solutions'] = so.relationship(back_populates='quest')

class Hints(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    hint_text: so.Mapped[str] = so.mapped_column(sa.String(300), index = True)
    quest_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Quests.id), index = True)

    quest: so.Mapped[Quests] = so.relationship(back_populates="hints")

class Solutions(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    solution_text: so.Mapped[str] = so.mapped_column(sa.String(150), index = True)
    quest_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Quests.id), index = True)
    hint_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Hints.id), index = True)

    quest: so.Mapped[Quests] = so.relationship(back_populates="solutions")
