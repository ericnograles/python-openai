from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from .config import Config

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

# Import your models here
from . import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    return app
