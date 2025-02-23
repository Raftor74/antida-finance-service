from flask import Flask
from utils.database import db
from blueprints.auth import bp as auth_bp
from blueprints.category import bp as category_bp
from blueprints.users import bp as users_bp
from blueprints.transaction import bp as transaction_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    db.init_app(app)
    return app
