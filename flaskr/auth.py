from flask import Blueprint, g, jsonify, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import mysql_db
from credentials import secret

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post('/register')
def register() -> tuple:
    data = request.json
    if hasattr(data, 'username') and hasattr(data, 'password'):
        response = create_user(data)
    else:
        response = jsonify({"error": "Invalid request body!"}), 400
    return response

@bp.post('/login')
def login() -> tuple:
    data = request.json
    if hasattr(data, 'username') and hasattr(data, 'password'):
        response = get_user(data)
    else:
        response = jsonify({"error": "Invalid request body!"}), 400
    return response
    
@bp.before_app_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = mysql_db.get_user_by_id(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('/login'))




def get_user(data: dict) -> tuple:
    try:
        user = mysql_db.get_user_by_username(data['username'])  
        if user is None:
            response_status = jsonify({"error": "Not Found", "message": "No users found associated to the provided username."}), 406
        elif check_password_hash(user['password'], data['password']):
            response_status = ({"error": "Incorrect username or password", "message": "Incorrect Username or Password"}), 406
        else:
            session.clear()
            session['user_id'] = user['user_id']
            response_status = jsonify({
                'username': user['username'],
                'favoriteTeam': user['favorite_team'],
                'notificationPreference': user['notification_pref'],
                'emailAddress': user['email_address'],
                'phone': user['phone']
            }), 200
    except Exception as e:
        response_status = jsonify({"error": "Request Error", "message": f"{e}"}), 400
    return response_status


def create_user(data: dict) -> tuple:
    try:
        if mysql_db.get_user_by_id(data['username']) is None:
            response_status = jsonify(message = "User already exists!"), 200
        else:
            sql_statement = conncatenate_create_user_sql(data)
            procedure_status = mysql_db.execute_proc(sql_statement)

            if procedure_status != 'Success':
                response_status = jsonify({"error": "New user not created", "message": f"{procedure_status}"}), 400
            else:
                response_status = jsonify(message = "Success"), 200
    except Exception as e:
        response_status = jsonify({"error": "New user not created", "message": f"{e}"}), 400
    return response_status


def conncatenate_create_user_sql(data: dict) -> str:
    sql_statement = (f"""CALL PROC_CREATE_USER(
        '{data["username"]}',
        '{generate_password_hash(data["password"])}', 
        '{data["favoriteTeam"]}', 
        '{data["notificationPreference"]}', 
        '{data["emailAddress"]}', 
        '{data["phoneNumber"]}', 
        @status);
    """)
    return sql_statement