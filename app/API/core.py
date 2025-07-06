from flask import Flask
from flask_login import LoginManager, UserMixin
from sqlalchemy import select

from .database import User, Session

app = Flask(__name__)
app.secret_key = '123_asd_123'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app=app)

class LoginUser(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    def check_password(self, password):
        return self.password == password

@login_manager.user_loader
def load_user(user_id):
    with Session() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            LoginUser(
                id = user.id,
                name = user.name,
                password = user.password
            )
    return None


