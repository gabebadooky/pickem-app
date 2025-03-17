from flask import Blueprint, g, jsonify, request, session

from . import mysql_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.post('/update-email/<str:userID>')
def update_user_email(data):
    try:
        sql_statement = concatenate_update_user_email_sql(data)
        procedure_status = mysql_db.execute_proc(sql_statement)
        if procedure_status == 'Status':
            response_status = jsonify(message = "Success")
        else:
            response_status = jsonify({"error": "Email Address not updated", "message": procedure_status})
    except Exception as e:
        response_status = jsonify({"error": "Email Address not updated", "message": e}), 400

@bp.post('/update-phone/<str:userID>')
def update_user_phone(data):
    try:
        sql_statement = concatenate_update_user_phone_sql(data)
        procedure_status = mysql_db.execute_proc(sql_statement)
        if procedure_status == 'Status':
            response_status = jsonify(message = "Success")
        else:
            response_status = jsonify({"error": "Phone not updated", "message": procedure_status})
    except Exception as e:
        response_status = jsonify({"error": "Phone not updated", "message": e}), 400

@bp.post('/update-favorite-team/<str:userID>')
def update_user_favorite_team(data):
    try:
        sql_statement = (data)
        procedure_status = mysql_db.execute_proc(sql_statement)
        if procedure_status == 'Status':
            response_status = jsonify(message = "Success")
        else:
            response_status = jsonify({"error": "Favorite Team not updated", "message": procedure_status})
    except Exception as e:
        response_status = jsonify({"error": "Favorite Team not updated", "message": e}), 400


def concatenate_update_user_email_sql(data):
    user_id = data['userID']
    email_address = data['emailAddress']
    sql_statement = f"CALL PROC_UPDATE_USER_EMAIL('{user_id}', '{email_address}', @status);"
    return sql_statement

def concatenate_update_user_phone_sql(data):
    user_id = data['userID']
    phone = data['phone']
    sql_statement = f"CALL PROC_UPDATE_USER_PHONE('{user_id}', '{phone}', @status);"
    return sql_statement

def concatenate_update_user_favorite_team(data):
    user_id = data['userID']
    favorite_team = data['favoriteTeam']
    sql_statement = f"CALL PROC_UPDATE_USER_PHONE('{user_id}', '{favorite_team}', @status);"
    return sql_statement