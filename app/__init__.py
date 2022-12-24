from flask import Flask
from app.extensions import db, migrate
from app.api.users import users
from app.api.games import games
from app.api.gamecodes import gamecodes
from app.api.userfriends import userfriends
from app.api.orders import orders
from app.api.transactions import transactions


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app)
    app.register_blueprint(users, url_prefix='/api/users')
    app.register_blueprint(games, url_prefix='/api/games')
    app.register_blueprint(gamecodes, url_prefix='/api/gamecodes')
    app.register_blueprint(userfriends, url_prefix='/api/userfriends')
    app.register_blueprint(orders, url_prefix='/api/orders')
    app.register_blueprint(transactions, url_prefix='/api/transactions')

    with app.test_request_context():
        db.create_all()

    return app
