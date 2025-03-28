from flask import Blueprint, g, jsonify, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from . import mysql_db
from credentials import secret

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post('/register')
def register():
    data = request.json
    return create_user(data)

@bp.post('/login')
def login():
    data = request.json
    return get_user(data)
    
@bp.before_app_request
def load_user():
    user_id = session.get('userID')
    if user_id is None:
        g.user = None
    else:
        g.user = mysql_db.get_user_by_id(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('/login'))




def get_user(data) -> tuple:
    try:
        user = mysql_db.get_user_by_username(data['username'])  
        if user is None:
            response_status = jsonify({"error": "Not Found", "message": "No users found associated to the provided username."}), 406
        elif check_password_hash(user['password'], data['password']):
            response_status = ({"error": "Incorrect username or password", "message": "Incorrect Username or Password"}), 406
        else:
            session.clear()
            session['user_id'] = user['userID']
            response_status = jsonify({
                'username': user['username'],
                'favoriteTeam': user['favoriteTeam'],
                'notificationPreference': user['notification_pref'],
                'emailAddress': user['email_address'],
                'phone': user['phone']
            }), 200
    except Exception as e:
        response_status = jsonify({"error": "Request Error", "message": f"{e}"}), 400
    return response_status


def create_user(data) -> tuple:
    try:
        sql_statement = conncatenate_create_user_sql(data)
        procedure_status = mysql_db.execute_proc(sql_statement)
        if procedure_status == 'Success':
            response_status = jsonify(message = "Success"), 200
        else:
            response_status = jsonify({"error": "New user not created", "message": f"{procedure_status}"}), 400
    except Exception as e:
        response_status = jsonify({"error": "New user not created", "message": f"{e}"}), 400
    return procedure_status


def conncatenate_create_user_sql(data):
    sql_statement = (f"""CALL PROC_CREATE_USER(
        '{data["username"]}',
        '{generate_password_hash(data["password"])}', 
        '{data["favorite_team"]}', 
        '{data["notification_preference"]}', 
        '{data["email_address"]}', 
        '{data["phone_number"]}', 
        @status);
    """)
    return sql_statement