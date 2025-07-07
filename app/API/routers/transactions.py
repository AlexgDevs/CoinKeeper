from typing import Literal
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select
from ..database import Session, Transaction, User

transaction_bp = Blueprint('trnsct', __name__)


@transaction_bp.get('/transactions')
@login_required
def get_transactions():

    user_id = current_user.id

    with Session() as session:
        transactions = session.scalars(select(Transaction).where(Transaction.user_id == user_id)).all()
        if transactions:
            return jsonify({'status': 'succses', 
                            'meta': 
                                {'count': len(transactions)},
                                'data': [{
                                    'id': transaction.id,
                                    'type': transaction.type,
                                    'amount': transaction.amount,
                                    'category_id': transaction.category_id,
                                    'user_id': transaction.user_id
                                } for transaction in transactions]
                                }), 200

        return jsonify({'status': 'error', 'error_type': 'transactions not found'}), 404


@transaction_bp.post('/transactions')
@login_required
def create_transaction():

    data = request.get_json()
    type = data.get('type')
    amount = data.get('amount')
    category_id = data.get('category_id') # будет через форму!
    user_id = current_user.id

    with Session.begin() as session:

        user = session.scalar(select(User).where(User.id == user_id))
        if type == 'Income':

            if user.balance - amount < 0:
                return jsonify({'status': 'error', 'error_type': 'insifision fance'}), 400

            user.balance -= amount

        if type == 'Expenditure':
            user.balance += amount

        new_transaction = Transaction(type=type, amount=amount, category_id=category_id, user_id=user_id)
        session.add(new_transaction)
        session.flush()

        return jsonify({'status': 'succsess', 'transaction': {
                                    'id': new_transaction.id,
                                    'type': new_transaction.type,
                                    'amount': new_transaction.amount,
                                    'category_id': new_transaction.category_id,
                                    'user_id': new_transaction.user_id}})


# keeper/api/v1/auth/[register, login, logout  [post]] succsess
# keeper/api/v1/transactions [post, get]
# keeper/api/v1/categories [post, get]
# keeper/api/v1/users [get]
# keeper/api/v1/users/me [get]