import os
from . import auth, games, teams, picks, user
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth


def create_app(test_config=None):
    # create and configure the app
    app: Flask = Flask(__name__, instance_relative_config=True)
    CORS(app)

    load_dotenv()
    app.config.from_mapping(
        SECRET_KEY = os.getenv("SECRET_KEY")
    )

    oath: OAuth = OAuth(app)
    google_oath = oath.register(
        name="google",
        client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
        server_metadata_uri="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid profile email"}
    )
    app.config["GOOGLE_OAUTH"] = google_oath

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
    
    #app.run()

    return app