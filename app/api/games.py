import os
from flask import (
    Blueprint,
    jsonify,
    request
)
from werkzeug.utils import secure_filename
from app.models import Game, User, GameCode
from app.extensions import db
from config import Config

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/image/'

games = Blueprint('games', __name__, template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@games.route("/buy", methods=['POST'])
def buy_game():
    user = User.query.get(request.form["user_id"])
    if not user:
        return jsonify({
            "status": "error",
            "message": "Error! User not found"
        })

    game = Game.query.get(request.form["game_id"])
    if not game:
        return jsonify({
            "status": "error",
            "message": "Error! Game not found"
        })

    if game.count <= 0:
        return jsonify({
            "status": "error",
            "message": "Game count <= 0"
        })

    if user.wallet < game.price:
        return jsonify({
            "status": "error",
            "message": "Not enough money"
        })

    gamecode = GameCode.query.filter_by(
        game_id=game.id,
        is_active=True
    ).first()

    if not gamecode:
        return jsonify({
            "status": "error",
            "message": f"Error! Not code for game {game.title}"

        })

    user.wallet = user.wallet - game.price
    game.count -= 1
    gamecode.is_active = False
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": gamecode.code
    })


@games.route("/", methods=['GET'])
def get_games():
    result = db.session.execute(
        db.select(Game)
    ).scalars()
    games: list = []
    for game in result:
        games.append(game.as_dict())
    return jsonify(games)


@games.route("get/<int:id>", methods=['GET'])
def get_game(id: int):
    game = db.get_or_404(Game, id)
    return jsonify(game.as_dict())


@games.route("/create", methods=['PUT'])
def create_game():
    game = Game(
        title=request.form["title"],
        price=request.form["price"],
        count=request.form["count"],
        description=request.form["description"],
    )
    db.session.add(game)
    db.session.commit()
    return jsonify(game.as_dict())


@games.route("/update/<int:id>", methods=['POST'])
def update_game(id: int):
    game = db.get_or_404(Game, id)
    game.title = request.form["title"]
    game.price = request.form["price"]
    game.count = request.form["count"]
    game.description = request.form["description"]
    db.session.commit()
    return jsonify(game.as_dict())


@games.route("/delete/<int:id>", methods=['DELETE'])
def delete_game(id: int):
    game = db.get_or_404(Game, id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({
        "message": "success"
    })


@games.route("/upload/<int:id>", methods=['POST'])
def upload(id: int):
    game = db.get_or_404(Game, id)
    if 'file' not in request.files:
        return jsonify({
            "message": "No file part"
        })
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "message": "No selected file"
        })
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        game.image = filename
        db.session.commit()
        return jsonify({
            "message": "success"
        })
