from flask import (
    Blueprint,
    jsonify,
    request
)
from app.models import GameCode
from app.extensions import db

gamecodes = Blueprint('gamecodes', __name__, template_folder='templates')


@gamecodes.route("/", methods=['GET'])
def get_gamecodes():
    result = db.session.execute(
        db.select(GameCode)
    ).scalars()
    gamecodes: list = []
    for row in result:
        gamecodes.append(row.as_dict())
    return jsonify(gamecodes)


@gamecodes.route("get/<int:id>", methods=['GET'])
def get_gamecode(id: int):
    gamecode = db.get_or_404(GameCode, id)
    return jsonify(gamecode.as_dict())


@gamecodes.route("/create", methods=['PUT'])
def create_gamecode():
    gamecode = GameCode(
        email=request.form["email"],
        password=request.form["password"],
        firstname=request.form["firstname"],
        lastname=request.form["lastname"],
        wallet=request.form["wallet"]
    )
    db.session.add(gamecode)
    db.session.commit()
    return jsonify(gamecode.as_dict())


@gamecodes.route("/update/<int:id>", methods=['POST'])
def update_gamecode(id: int):
    gamecode = db.get_or_404(GameCode, id)
    gamecode.email = request.form["email"],
    gamecode.password = request.form["password"],
    gamecode.firstname = request.form["firstname"],
    gamecode.lastname = request.form["lastname"],
    gamecode.wallet = request.form["wallet"]
    db.session.commit()
    return jsonify(gamecode.as_dict())


@gamecodes.route("/delete/<int:id>", methods=['DELETE'])
def delete_gamecode(id: int):
    gamecode = db.get_or_404(GameCode, id)
    db.session.delete(gamecode)
    db.session.commit()
    return jsonify({
        "message": "success"
    })
