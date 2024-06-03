from flask import (
    Flask, request, Blueprint, redirect
)
from backend.blueprint import auth
from backend.extension import login_manager, mail
from backend.models import db, migrate

def createApp():
    app : Flask = Flask(__name__)
    app.config.from_pyfile('config.py')

    register_blueprint(app)
    register_database(app)
    register_extension(app) 

    return app;

def register_blueprint(app : Flask) ->None:
    """reload blueprint"""
    app.register_blueprint(auth.bp)


def register_database(app : Flask) -> None:
    """reload database"""
    db.init_app(app)
    migrate.init_app(app, db)


def register_extension(app : Flask) ->None:
    """reload extension"""
    login_manager.init_app(app)
    mail.init_app(app)
