from datetime import datetime
from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    password = db.Column(db.String(30))
    wallet = db.Column(db.Float, default=0)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserFriend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    price = db.Column(db.Float, default=0)
    count = db.Column(db.Integer, default=0)
    description = db.Column(db.String)
    rate = db.Column(db.Integer, default=0)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class GameCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id), nullable=False)
    code = db.Column(db.String, unique=True, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    gamecode_id = db.Column(
        db.Integer,
        db.ForeignKey(GameCode.id),
        nullable=False
    )
    price = db.Column(db.Float, nullable=False)
    date_order = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id))
    gamecode_id = db.Column(
        db.Integer,
        db.ForeignKey(GameCode.id),
    )
    description = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
