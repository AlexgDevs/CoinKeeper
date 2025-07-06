from typing import Literal
from flask import Blueprint, request, jsonify
from sqlalchemy import select
from ..database import Session, Transaction, User

transaction_bp = Blueprint('trnsct', __name__)