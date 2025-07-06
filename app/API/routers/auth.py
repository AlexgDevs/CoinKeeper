from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from ..database import User, Session
from .. import login_manager, LoginUser

auth_bp = Blueprint('auth', __name__)

#register
@auth_bp.post('/auth/register')
def register():

    if current_user.is_authenticated:
        return jsonify({'status': 'is_authenticated'}), 200

    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    with Session.begin() as session:
        new_user = User(name=name, password=password)

        session.add(new_user)
        session.flush()

        login_user_obj = LoginUser(

                    id=new_user.id,
                    name=new_user.name,
                    password=new_user.password
                
                )

        login_user(login_user_obj)
        return jsonify({'statis': 'success'}), 201

#login
@auth_bp.post('/auth/login')
def login():
    
    if current_user.is_authenticated:
        return jsonify({'status': 'is_authenticated'})
    
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    with Session() as session:
        user = session.scalar(select(User).where(User.name == name))
        if user:
            if user.password == password:
                
                login_user_obj = LoginUser(

                    id=user.id,
                    name=user.name,
                    password=user.password
                
                )

                login_user(login_user_obj)
                return jsonify({'status': 'success', 'user': {'id': current_user.id, 'name': current_user.name}}), 201

            else:
                return jsonify({'status': 'error', 'error_type': 'uncorrected password'}), 400
        return jsonify({'status': 'error', 'error_type': 'user not found'}), 404

#logout
@auth_bp.get('/auth/logout')
def logout():
    logout_user()

    return jsonify({'status': 'succsess', 'message': 'logg out successfully'}), 200
