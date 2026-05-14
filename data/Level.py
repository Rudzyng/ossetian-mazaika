import sqlalchemy
from sqlalchemy import orm
from datetime import datetime

from .db_session import SqlAlchemyBase


class Level(SqlAlchemyBase):
    __tablename__ = 'levels'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Название на осетинском
    grid_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=2)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)

    parts = orm.relationship("PuzzlePart", back_populates="level",
                             cascade="all, delete-orphan",
                             order_by="PuzzlePart.id")
