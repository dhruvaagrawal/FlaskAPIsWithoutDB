"""
Author: Dhruva Agrawal
Author E-mail: dhruva_agrawal@outlook.com
"""

from flask import Flask

from api import api
from api.teams import teams
from api.users import users
from config import FlaskConfig


def create_app(config_class=FlaskConfig, **kwargs):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Registering Blueprints
    api.register_blueprint(teams)
    api.register_blueprint(users)
    app.register_blueprint(api)

    return app

