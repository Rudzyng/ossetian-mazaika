import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class PuzzlePart(SqlAlchemyBase):
    """Часть пазла"""
    __tablename__ = 'puzzle_parts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    level_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("levels.id"), nullable=False)

    image_file = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    part_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)

    level = orm.relationship("Level", back_populates="parts")
