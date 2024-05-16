from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import ForeignKey
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

class UsersInfo(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    surname: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    suburb: so.Mapped[str] = so.mapped_column(sa.String(64), index = True)
    
    writer: so.WriteOnlyMapped['Quests'] = so.relationship(back_populates='creator')
    player_tracker = so.relationship('PlayerTracker', back_populates='user')
    completeduser: so.Mapped['CompletedQuests'] = so.relationship(back_populates="questuser")

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
    creator_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(UsersInfo.id), index = True)

    creator: so.Mapped['UsersInfo'] = so.relationship('UsersInfo', back_populates='writer')
    hintsolution: so.WriteOnlyMapped['HintsSolutions'] = so.relationship(back_populates='quest')
    completedquests: so.Mapped['CompletedQuests'] = so.relationship(back_populates="completion")

class HintsSolutions(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    hint_text: so.Mapped[str] = so.mapped_column(sa.String(300), index = True)
    solution_text: so.Mapped[str] = so.mapped_column(sa.String(150), index = True)
    quest_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Quests.id), index = True)

    quest: so.Mapped[Quests] = so.relationship(back_populates="hintsolution")

class PlayerTracker(db.Model):
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(UsersInfo.id), primary_key = True, index = True)
    points: so.Mapped[int] = so.mapped_column(index = True, default = 0)
    quests_completed: so.Mapped[int] = so.mapped_column(index = True, default = 0)

    user = so.relationship('UsersInfo', back_populates='player_tracker')

class CompletedQuests(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    quest_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Quests.id), index = True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(UsersInfo.id), index = True)

    completion: so.Mapped[Quests] = so.relationship(back_populates="completedquests")
    questuser: so.Mapped[UsersInfo] = so.relationship(back_populates="completeduser")
