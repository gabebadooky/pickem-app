from flask import Blueprint, jsonify, request

from . import mysql_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.post('/update-email')
def update_user_email() -> dict:
    data = request.json
    try:
        procedure_output = sql_update_user_email(data)
        if procedure_output == 'Success':
            response_status = jsonify(message = "Success"), 201
        else:
            response_status = jsonify({"error": "Email Address not updated", "message": procedure_output})
    except Exception as e:
        response_status = jsonify({"error": "Email Address not updated", "message": e}), 400
    return response_status

@bp.post('/update-phone')
def update_user_phone() -> dict:
    data = request.json
    try:
        procedure_output = sql_update_user_phone(data)
        if procedure_output == 'Success':
            response_status = jsonify(message = "Success"), 201
        else:
            response_status = jsonify({"error": "Phone not updated", "message": procedure_output})
    except Exception as e:
        response_status = jsonify({"error": "Phone not updated", "message": e}), 400
    return response_status

@bp.post('/update-favorite-team')
def update_user_favorite_team() -> dict:
    data = request.json
    try:
        procedure_output = sql_update_user_favorite_team(data)
        if procedure_output == 'Success':
            response_status = jsonify(message = "Success"), 201
        else:
            response_status = jsonify({"error": "Favorite Team not updated", "message": procedure_output})
    except Exception as e:
        response_status = jsonify({"error": "Favorite Team not updated", "message": e}), 400
    return response_status

@bp.post('/update-notification-preference')
def update_user_notification_preference() -> dict:
    data = request.json
    try:
        procedure_output = sql_update_user_notification_preference(data)
        if procedure_output == 'Success':
            response_status = jsonify(message = "Success"), 201
        else:
            response_status = jsonify({"error": "Notification Preference not updated", "message": procedure_output})
    except Exception as e:
        response_status = jsonify({"error": "Notification Preference not updated", "message": e}), 400
    return response_status



def sql_update_user_email(data) -> str:
    user_id = data['userID']
    email_address = data['emailAddress']
    sql_statement = f"CALL PROC_UPDATE_USER_EMAIL('{user_id}', '{email_address}', @status);"
    procedure_output = mysql_db.execute_proc(sql_statement)
    return procedure_output

def sql_update_user_phone(data) -> str:
    user_id = data['userID']
    phone = data['phone']
    sql_statement = f"CALL PROC_UPDATE_USER_PHONE('{user_id}', '{phone}', @status);"
    procedure_output = mysql_db.execute_proc(sql_statement)
    return procedure_output

def sql_update_user_favorite_team(data) -> str:
    user_id = data['userID']
    favorite_team = data['favoriteTeam']
    sql_statement = f"CALL PROC_UPDATE_USER_FAVORITE_TEAM('{user_id}', '{favorite_team}', @status);"
    procedure_output = mysql_db.execute_proc(sql_statement)
    return procedure_output

def sql_update_user_notification_preference(data) -> str:
    user_id = data['userID']
    favorite_team = data['notificationPreference']
    sql_statement = f"CALL PROC_UPDATE_USER_NOTIFICATION_PREFERENCE('{user_id}', '{favorite_team}', @status);"
    procedure_output = mysql_db.execute_proc(sql_statement)
    return procedure_output