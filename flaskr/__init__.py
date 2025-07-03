import os
from . import auth, games, teams, picks, user
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import secret_key


def create_app(test_config=None):
    # create and configure the app
    app: Flask = Flask(__name__, instance_relative_config=True)
    CORS(app)
    """app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )"""
    app.config.from_mapping(
        SECRET_KEY = secret_key
    )

    jwt = JWTManager(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(games.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(picks.bp)
    app.register_blueprint(user.bp)

    @app.route('/')
    def hello():
        return {
            "gb": "pickem"
        }

    return app