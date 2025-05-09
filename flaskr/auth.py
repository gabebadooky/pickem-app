from flask import Blueprint, g, jsonify, redirect, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from . import mysql_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

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
    print("Beginning register request");
    data = request.json
    print(f"data: {data}")
    if ("username" in data) and ("password" in data):
        print("Username and Password passed through, creating user")
        response = create_user(data)
        print(f"response: {response}")
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
        response = get_user(data)
    else:
        response = jsonify({"error": "Invalid request body!"}), 400
    return response
    
@bp.before_app_request
def load_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = mysql_db.get_user_by_id(user_id)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("/login"))




def get_user(data: dict) -> tuple:
    try:
        user = mysql_db.get_user_by_username(data["username"])
        if user is None:
            response_status = jsonify({"error": "Not Found", "message": "No users found associated to the provided username."}), 406
        elif check_password_hash(user["PWDHASH"], data["password"]):
            access_token = create_access_token(identity=user["USER_ID"])
            response_status = jsonify(access_token=access_token)
        else:
            response_status = ({"error": "Incorrect username or password", "message": "Incorrect Username or Password"}), 406
    except Exception as e:
        if e == "'NoneType' object is not subscriptable'":
            response_status = jsonify({"error": "Not Found!", "message": "No users found associated to the provided username."}), 406
        else:
            response_status = jsonify({"error": "Request Error", "message": f"{e}"}), 400
    return response_status


def create_user(data: dict) -> tuple:
    try:
        user = mysql_db.get_user_by_username(data["username"])
        if user is None:
            sql_statement = conncatenate_create_user_sql(data)
            procedure_status = mysql_db.execute_proc(sql_statement)
            if procedure_status != "Success":
                response_status = jsonify({"error": "Error occurred calling PROC_CREATE_USER procedure!", "message": f"{procedure_status}"}), 400
            else:
                response_status = jsonify(message = "Success"), 200
        else:
            print(f"User {data["username"]} already exists!")
            response_status = jsonify(message = f"User already exists!"), 200
    except Exception as e:
        response_status = jsonify({"error": "New user not created !", "message": f"{e}"}), 400
    return response_status


def conncatenate_create_user_sql(data: dict) -> str:
    if ("favoriteTeam" not in data):
        favoriteTeam = "NULL"
    else:
        favoriteTeam = f"'{data["favoriteTeam"]}'"

    if ("notificationPreference" not in data):
        notificationPreference = "NULL"
    else:
        notificationPreference = f"'{data["notificationPreference"]}'"

    if ("emailAddress" not in data):
        emailAddress = "NULL"
    else:
        emailAddress = f"'{data["emailAddress"]}'"

    if ("phoneNumber" not in data):
        phoneNumber = "NULL"
    else:
        phoneNumber = f"'{data["phoneNumber"]}'"

    sql_statement = (f"""CALL PROC_CREATE_USER(
        '{data["username"]}',
        '{generate_password_hash(data["password"], "pbkdf2:sha256", 16)}', 
        {favoriteTeam}, 
        {notificationPreference},
        {emailAddress},
        {phoneNumber}, 
        @status);
    """)
    return sql_statement