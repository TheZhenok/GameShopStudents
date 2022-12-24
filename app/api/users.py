from flask import (
    Blueprint,
    jsonify,
    request
)
from app.models import User
from app.extensions import db

users = Blueprint('users', __name__, template_folder='templates')


@users.route("/", methods=['GET'])
def get_users():
    result = db.session.execute(
        db.select(User)
    ).scalars()
    users: list = []
    for row in result:
        users.append(row.as_dict())
    return jsonify(users)


@users.route("get/<int:id>", methods=['GET'])
def get_user(id: int):
    user = db.get_or_404(User, id)
    return jsonify(user.as_dict())


@users.route("/create", methods=['PUT'])
def create_user():
    user = User(
        email=request.form["email"],
        password=request.form["password"],
        firstname=request.form["firstname"],
        lastname=request.form["lastname"],
        wallet=request.form["wallet"]
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.as_dict())


@users.route("/update/<int:id>", methods=['POST'])
def update_user(id: int):
    user = db.get_or_404(User, id)
    user.email = request.form["email"],
    user.password = request.form["password"],
    user.firstname = request.form["firstname"],
    user.lastname = request.form["lastname"],
    user.wallet = request.form["wallet"]
    db.session.commit()
    return jsonify(user.as_dict())


@users.route("/delete/<int:id>", methods=['DELETE'])
def delete_user(id: int):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        "message": "success"
    })
