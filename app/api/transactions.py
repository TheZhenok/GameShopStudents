from flask import (
    Blueprint,
    jsonify
)
from app.models import Transaction
from app.extensions import db

transactions = Blueprint('transactions', __name__, template_folder='templates')


@transactions.route("/", methods=['GET'])
def get_transactions():
    result = db.session.execute(
        db.select(Transaction)
    ).scalars()
    transactions: list = []
    for row in result:
        transactions.append(row.as_dict())
    return jsonify(transactions)


@transactions.route("get/<int:id>", methods=['GET'])
def get_transaction(id: int):
    transaction = db.get_or_404(Transaction, id)
    return jsonify(transaction.as_dict())
