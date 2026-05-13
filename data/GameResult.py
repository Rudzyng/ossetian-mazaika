import sqlalchemy
from sqlalchemy import orm
from datetime import datetime

from .db_session import SqlAlchemyBase


class GameResult(SqlAlchemyBase):
    __tablename__ = 'game_results'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    level_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("levels.id"), nullable=False)
    time_seconds = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    level = orm.relationship("Level", backref="results")
    user = orm.relationship("User", backref="results")