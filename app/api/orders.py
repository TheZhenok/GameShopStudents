from flask import (
    Blueprint,
    jsonify,
    request
)
from app.models import Order
from app.extensions import db

orders = Blueprint('orders', __name__, template_folder='templates')


@orders.route("/", methods=['GET'])
def get_orders():
    result = db.session.execute(
        db.select(Order)
    ).scalars()
    orders: list = []
    for row in result:
        orders.append(row.as_dict())
    return jsonify(orders)


@orders.route("get/<int:id>", methods=['GET'])
def get_order(id: int):
    order = db.get_or_404(Order, id)
    return jsonify(order.as_dict())


@orders.route("/create", methods=['PUT'])
def create_order():
    order = Order(
        user_id=request.form["user_id"],
        gamecode_id=request.form["gamecode_id"],
        price=request.form["price"],
        date_order=request.form["date_order"],
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.as_dict())


@orders.route("/update/<int:id>", methods=['POST'])
def update_order(id: int):
    order = db.get_or_404(Order, id)
    order.user_id = request.form["user_id"],
    order.gamecode_id = request.form["gamecode_id"],
    order.price = request.form["price"],
    order.date_order = request.form["date_order"],
    db.session.commit()
    return jsonify(order.as_dict())


@orders.route("/delete/<int:id>", methods=['DELETE'])
def delete_order(id: int):
    order = db.get_or_404(Order, id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({
        "message": "success"
    })
