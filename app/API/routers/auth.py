from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import select

from ..database import User, Session
from .. import login_manager, LoginUser

auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/auth/register')
def process_register():

    if current_user.is_authenticated:
        return jsonify({'Статус': 'Зареган'})

    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    with Session.begin() as session:
        new_user = User(name=name, password=password)

        session.add(new_user)
        session.flush()

        return jsonify({'type': 'succses'})

@auth_bp.get('/auth/login')
def login():
    pass

@auth_bp.get('/auth/answer')
@login_required
def get_answer():
    return jsonify({'answer': f'youid - {current_user.id}'})

