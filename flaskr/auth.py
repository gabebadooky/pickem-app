from flask import Blueprint, g, jsonify, redirect, session, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from . import mysql_db

bp: Blueprint = Blueprint("auth", __name__, url_prefix="/auth")

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
    
#@bp.before_app_request
def load_user():
    user_id: int = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = mysql_db.authenticate_user_by_id(user_id)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("/login"))




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
                response_status: tuple = jsonify(access_token=access_token), 200
        else:
            print(f"User {data['username']} already exists!")
            response_status: tuple = jsonify(message = f"User already exists!"), 200
    except Exception as e:
        response_status: tuple = jsonify({"error": "New user not created!", "message": f"{e}"}), 400
    return response_status


def concatenate_create_user_sql(data: dict) -> str:
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
        '{generate_password_hash(data["password"], "pbkdf2:sha256", 16)}', 
        {favoriteTeam}, 
        {notificationPreference},
        {emailAddress},
        {phoneNumber}, 
        @status);
    """)
    return sql_statement