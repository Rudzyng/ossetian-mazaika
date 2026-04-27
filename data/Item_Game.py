import sqlalchemy

from .db_session import SqlAlchemyBase


class Item_Game(SqlAlchemyBase):
    __tablename__ = 'item_game'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    level_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("levels.id"))
    word = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    word_index = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    image_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image_index = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)