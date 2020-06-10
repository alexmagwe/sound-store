import os 
import json
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from app_store.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
admin = Admin(name = 'Dashboard')
login_manager = LoginManager()


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app_store.user.routes import user
    from app_store.admin.routes import admin
    from app_store.shop.routes import shop
    from app_store.errors.handlers import errors
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(shop)
    app.register_blueprint(errors)

    return app