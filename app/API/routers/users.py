from typing import Literal
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select
from ..database import Session, Transaction, User

users_bp = Blueprint('users', __name__)

@users_bp.get('/users')
def get_users():
    
    with Session() as session:
        users = session.scalars(select(User)).all()
        if users:
            return jsonify({'users': [{'user_id': user.id, 'user_name': user.name} for user in users], 'meta': {'count': len(users)}, 'status': 'success'}), 200
        return jsonify({'status': 'error', 'error_type': 'users not found'}), 404


@users_bp.get('/users/me')
@login_required
def get_user_me():

    with Session() as session:
        user = session.scalar(select(User).where(User.id == current_user.id))
        if user:
            return jsonify({'status': 'success', 'current_user': {'id': user.id, 'name': user.name, 'balance': user.balance}})