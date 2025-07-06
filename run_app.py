from app import app, migrate, up, drop
from app.API.routers import auth_bp, transaction_bp

def reg_bp(app):
    bps = [
        auth_bp,
        transaction_bp
    ]

    for bp in bps:
        app.register_blueprint(bp, url_prefix='/api/v1')

if __name__ == '__main__':

    migrate()
    reg_bp(app=app)
    app.run(debug=True)