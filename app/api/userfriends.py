from flask import (
    Blueprint,
    jsonify,
    request
)
from app.models import UserFriend
from app.extensions import db

userfriends = Blueprint('userfriends', __name__, template_folder='templates')


@userfriends.route("/", methods=['GET'])
def get_userfriends():
    result = db.session.execute(
        db.select(UserFriend)
    ).scalars()
    userfriends: list = []
    for row in result:
        userfriends.append(row.as_dict())
    return jsonify(userfriends)


@userfriends.route("get/<int:id>", methods=['GET'])
def get_userfriend(id: int):
    userfriend = db.get_or_404(UserFriend, id)
    return jsonify(userfriend.as_dict())


@userfriends.route("/create", methods=['PUT'])
def create_userfriend():
    userfriend = UserFriend(
        user_id=request.form["user_id"],
        friend_id=request.form["friend_id"]
    )
    db.session.add(userfriend)
    db.session.commit()
    return jsonify(userfriend.as_dict())


@userfriends.route("/update/<int:id>", methods=['POST'])
def update_userfriend(id: int):
    userfriend = db.get_or_404(UserFriend, id)
    userfriend.user_id = request.form["user_id"],
    userfriend.friend_id = request.form["friend_id"],
    db.session.commit()
    return jsonify(userfriend.as_dict())


@userfriends.route("/delete/<int:id>", methods=['DELETE'])
def delete_userfriend(id: int):
    userfriend = db.get_or_404(UserFriend, id)
    db.session.delete(userfriend)
    db.session.commit()
    return jsonify({
        "message": "success"
    })
