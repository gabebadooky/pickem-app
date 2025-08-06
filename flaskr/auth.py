import os
from flask import current_app, Blueprint, g, jsonify, redirect, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
from . import mysql_db


bp: Blueprint = Blueprint("auth", __name__, url_prefix="/auth",)


oath: OAuth = OAuth(current_app)
google = oath.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    client_kwargs={"scope": "openid profile email"}
)


@bp.post("/register")
def register() -> tuple:
    """
    Body Example:
    [
        {
            "username": <str>, (REQUIRED)
            "password": <str>, (REQUIRED)
            "favoriteTeam": <str>, (optional)
            "notificationPreference": <str>, (optional)
            "emailAddress": <str>, (optional)
            "phone": <str> (optional)
        }
    ]
    """
    data = request.json
    if ("username" in data) and ("password" in data):
        response: tuple = create_user(data)
        print(f"response: {response[0].json}")
    else:
        response = jsonify({"error": "Invalid request body!"}), 400
    return response


@bp.post("/login")
def login() -> tuple:
    """
    Body Example:
    [
        {
            "username": <str>, (REQUIRED)
            "password": <str> (REQUIRED)
        }
    ]
    """
    data = request.json
    if ("username" in data) and ("password" in data):
        response: tuple = authenticate_user(data)
    else:
        response: tuple = jsonify({"error": "Invalid request body!"}), 400
    return response


### OAUTH ###
@bp.route("/google/login")
def login_google() -> tuple:
    try:
        redirect_uri = url_for("auth.authorize_google", _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        print(f"Error occurred during Google OAuth Login attempt: {e}")
        return jsonify({"error": "Google Login Error", "message": f"{e}"}), 400


@bp.route("/google/authorize")
def authorize_google():
    token = google.authorize_access_token()
    user_info_endpoint = google.server_metadata["userinfo_endpoint"]
    response = google.get(user_info_endpoint)
    user_info = response.json()
    email_address: str = user_info["email"]
    print(user_info)
    user: dict = mysql_db.get_user_by_username(email_address)
    if user is None:
        print(f"Creating new Google user {email_address}...")
        resp: tuple = create_user({ "username": email_address })
        #mysql_db.execute_proc(concatenate_create_user_sql(user_info))
        #response_status: tuple = jsonify(token), 200        
    else:
        print(f"Authenticating existing Google user {email_address}...")
        resp: tuple = authenticate_user({ "username": email_address, "password": "" })
        #response_status: tuple = jsonify(token), 200
    print(f"resp[0].json: {resp[0].json}")
    if ("access_token" in resp[0].json):
        access_token = resp[0].json["access_token"]
        return redirect(f"https://have-a-nice-pickem.onrender.com?access_token={access_token}")
    else:        
        return redirect(f"https://have-a-nice-pickem.onrender.com/")
### OAUTH ###


def authenticate_user(data: dict) -> tuple:
    try:
        user: dict = mysql_db.get_user_by_username(data["username"])
        if user is None:
            response_status: dict = jsonify({"error": "Not Found", "message": "No users found associated to the provided username."}), 406
        elif check_password_hash(user["PWDHASH"], data["password"]):
            access_token: str = create_access_token(identity=str(user["USER_ID"]), expires_delta=timedelta(hours=2))
            response_status: tuple = jsonify(access_token=access_token), 200
        else:
            response_status: tuple = ({"error": "Incorrect username or password", "message": "Incorrect Username or Password"}), 406
    except Exception as e:
        if e == "'NoneType' object is not subscriptable'":
            response_status: tuple = jsonify({"error": "Not Found!", "message": "No users found associated to the provided username."}), 406
        else:
            response_status: tuple = jsonify({"error": "Request Error", "message": f"{e}"}), 400
    return response_status


def create_user(data: dict) -> tuple:
    try:
        user: dict = mysql_db.get_user_by_username(data["username"])
        if user is None:
            sql_statement: str = concatenate_create_user_sql(data)
            procedure_status: str = mysql_db.execute_proc(sql_statement)
            print(f"procedure_status: {procedure_status}")
            if procedure_status != "Success":
                response_status: dict = jsonify({"error": "Error occurred calling PROC_CREATE_USER procedure!", "message": f"{procedure_status}"}), 400
            else:
                user_id: int = mysql_db.get_user_by_username(data["username"])["USER_ID"]
                access_token: str = create_access_token(identity=str(user_id), expires_delta=timedelta(hours=2))
                print(f"access_token: {access_token}")
                response_status: tuple = jsonify(access_token=access_token), 200
        else:
            print(f"User {data['username']} already exists!")
            response_status: tuple = jsonify(message = f"User already exists!"), 200
    except Exception as e:
        response_status: tuple = jsonify({"error": "New user not created!", "message": f"{e}"}), 400
    return response_status


def concatenate_create_user_sql(data: dict) -> str:    
    if ("password" not in data):
        password: str = "" # OAUTH
    else:
        password: str = data['password']

    if ("favoriteTeam" not in data):
        favoriteTeam: str = "NULL"
    else:
        favoriteTeam: str = f"'{data['favoriteTeam']}'"

    if ("notificationPreference" not in data):
        notificationPreference: str = "NULL"
    else:
        notificationPreference: str = f"'{data['notificationPreference']}'"

    if ("emailAddress" not in data):
        emailAddress: str = "NULL"
    else:
        emailAddress: str = f"'{data['emailAddress']}'"

    if ("phoneNumber" not in data):
        phoneNumber: str = "NULL"
    else:
        phoneNumber: str = f"'{data['phoneNumber']}'"

    sql_statement: str = (f"""CALL PROC_CREATE_USER(
        '{data["username"]}',
        '{generate_password_hash(password, "pbkdf2:sha256", 16)}', 
        {favoriteTeam}, 
        {notificationPreference},
        {emailAddress},
        {phoneNumber}, 
        @status);
    """)
    return sql_statement
