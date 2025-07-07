from typing import Literal
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select
from ..database import Session, Transaction, User, Category

category_bp = Blueprint('category', __name__)

@category_bp.post('/categories')
@login_required
def create_category():

    name = request.get_json().get('name')
    user_id = current_user.id

    with Session.begin() as session:
        new_category = Category(name=name, user_id=user_id)
        session.add(new_category)
        session.flush()

        return jsonify({'status': 'succsess', 'category': {'id': new_category.id, 'name': new_category.name}}), 201


@category_bp.get('/categories')
@login_required
def get_categories():

    user_id = current_user.id
    with Session() as session:
        categories = session.scalars(select(Category).where(Category.user_id == user_id)).all()
        if categories:
            return jsonify({"data": [
            {
                "category_id": category.id,
                "category_name": category.name,
                "user_id": category.user_id
            } for category in categories
                ],
                "meta": {
                    "count": len(categories),
                    "status": "success"
                }
            }), 200
        
        return jsonify({'status': 'error', 'error_type': 'categories not found'}), 404

