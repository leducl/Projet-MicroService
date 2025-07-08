from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

# Initialisation de SQLAlchemy et d'Alembic
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    # Les tables sont gérées via migrations Alembic
    # Pour créer ou mettre à jour le schéma, utilisez:
    # flask db upgrade

    from app.routes import register_routes
    register_routes(app)
    return app
