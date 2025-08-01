from flask import Blueprint, jsonify, request

from . import mysql_db

bp: Blueprint = Blueprint("user", __name__, url_prefix="/user")


@bp.get("/<user_id>")
def get_user_properties(user_id) -> tuple:
    try:
        user: dict = mysql_db.get_user_by_id(user_id)
        if len(user) == 0:
            response_status: tuple = jsonify({"error": "Not Found", "message": "No Users found associated to the provided User ID."}), 406
        else:
            camel_cased_user: dict = {
                "userID": user["USER_ID"],
                "username": user["USERNAME"],
                "favoriteTeam": user["FAVORITE_TEAM"],
                "notificationPreference": user["NOTIFICATION_PREF"],
                "emailAddress": user["EMAIL_ADDRESS"],
                "phone": user["PHONE"]
            }
            response_status: tuple = jsonify(camel_cased_user), 200
    except Exception as e:
        print(e)
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    return response_status


@bp.get("/ids")
def get_all_users() -> tuple:
    try:
        users: list = mysql_db.call_view("SELECT * FROM GET_USER_IDS_VW;")
        camel_cased_list: list = []
        for user in users:
            camel_cased_user: dict = {
                "userID": user["USER_ID"],
                "username": user["USERNAME"]
            }
            camel_cased_list.append(camel_cased_user)
        response_status = jsonify(camel_cased_list), 200
    except Exception as e:
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    return response_status
            

@bp.post("/update-email")
def update_user_email() -> tuple:
    """
    Body Example:
    [
        {
            "userID": <int>, (REQUIRED)
            "emailAddress": <str> (REQUIRED)
        }
    ]
    """
    data = request.json
    try:
        procedure_output: str = sql_update_user_email(data)
        if procedure_output == "Success":
            response_status: tuple = jsonify(message = "Success"), 201
        else:
            response_status: tuple = jsonify({"error": "Email Address not updated", "message": procedure_output})
    except Exception as e:
        response_status: tuple = jsonify({"error": "Email Address not updated", "message": e}), 400
    return response_status


@bp.post("/update-phone")
def update_user_phone() -> tuple:
    """
    Body Example:
    [
        {
            "userID": <int>, (REQUIRED)
            "phone": <str> (REQUIRED)
        }
    ]
    """
    data = request.json
    try:
        procedure_output: str = sql_update_user_phone(data)
        if procedure_output == "Success":
            response_status: tuple = jsonify(message = "Success"), 201
        else:
            response_status: tuple = jsonify({"error": "Phone not updated", "message": procedure_output})
    except Exception as e:
        response_status: tuple = jsonify({"error": "Phone not updated", "message": e}), 400
    return response_status


@bp.post("/update-favorite-team")
def update_user_favorite_team() -> tuple:
    """
    Body Example:
    [
        {
            "userID": <int>, (REQUIRED)
            "favoriteTeam": <str> (REQUIRED)
        }
    ]
    """
    data = request.json
    try:
        procedure_output: str = sql_update_user_favorite_team(data)
        if procedure_output == "Success":
            response_status: tuple = jsonify(message = "Success"), 201
        else:
            response_status: tuple = jsonify({"error": "Favorite Team not updated", "message": procedure_output})
    except Exception as e:
        response_status: tuple = jsonify({"error": "Favorite Team not updated", "message": e}), 400
    return response_status


@bp.post("/update-notification-preference")
def update_user_notification_preference() -> tuple:
    """
    Body Example:
    [
        {
            "userID": <int>, (REQUIRED)
            "notificationPreference": <str> (REQUIRED)
        }
    ]
    """
    data = request.json
    try:
        procedure_output: str = sql_update_user_notification_preference(data)
        if procedure_output == "Success":
            response_status: tuple = jsonify(message = "Success"), 201
        else:
            response_status: tuple = jsonify({"error": "Notification Preference not updated", "message": procedure_output})
    except Exception as e:
        response_status: tuple = jsonify({"error": "Notification Preference not updated", "message": e}), 400
    return response_status



def sql_update_user_email(data: dict) -> str:
    user_id: int = data["userID"]
    email_address: str = data["emailAddress"]
    sql_statement: str = f"CALL PROC_UPDATE_USER_EMAIL('{user_id}', '{email_address}', @status);"
    procedure_output: str = mysql_db.execute_proc(sql_statement)
    return procedure_output

def sql_update_user_phone(data: dict) -> str:
    user_id: int = data["userID"]
    phone: str = data["phone"]
    sql_statement: str = f"CALL PROC_UPDATE_USER_PHONE('{user_id}', '{phone}', @status);"
    procedure_output: str = mysql_db.execute_proc(sql_statement)
    return procedure_output

def sql_update_user_favorite_team(data: dict) -> str:
    user_id: int = data["userID"]
    favorite_team: str = data["favoriteTeam"]
    sql_statement: str = f"CALL PROC_UPDATE_USER_FAVORITE_TEAM('{user_id}', '{favorite_team}', @status);"
    procedure_output: str = mysql_db.execute_proc(sql_statement)
    return procedure_output

def sql_update_user_notification_preference(data: dict) -> str:
    user_id: int = data["userID"]
    favorite_team: str = data["notificationPreference"]
    sql_statement: str = f"CALL PROC_UPDATE_USER_NOTIFICATION_PREFERENCE('{user_id}', '{favorite_team}', @status);"
    procedure_output: str = mysql_db.execute_proc(sql_statement)
    return procedure_output