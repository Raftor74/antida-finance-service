from flask import Flask
from utils.database import db
from blueprints.auth import bp as auth_bp
from blueprints.users import bp as users_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    db.init_app(app)
    return app
