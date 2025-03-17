from flask import Blueprint, g, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from . import mysql_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post('/register')
def register():
    data = request.json
    procedure_status = create_user(data)
    return jsonify({'status': procedure_status})

@bp.post('/login')
def login():
    data = request.json
    response = create_user(data)
    return jsonify(response)

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




def get_user(data) -> dict:
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
                'favoriteTeam': user['favoriteTeam'],
                'notificationPreference': user['notification_pref'],
                'emailAddress': user['email_address'],
                'phone': user['phone']
            }), 200

    except Exception as e:
        response_status = jsonify({"error": "Request Error", "message": f"{e}"}), 400
    return response_status


def create_user(data) -> str:
    try:
        sql_statement = (f"""CALL PROC_CREATE_USER(
                            '{data["username"]}',
                            '{generate_password_hash(data["password"])}', 
                            '{data["favorite_team"]}', 
                            '{data["notification_preference"]}', 
                            '{data["email_address"]}', 
                            '{data["phone_number"]}', 
                            @status);
                        """)
        procedure_status = mysql_db.execute_proc(sql_statement)

        if procedure_status != 'Success':
            response_status = jsonify(message = "Success"), 200
        else:
            response_status = jsonify({"error": "New user not created", "message": f"{procedure_status}"}), 400
    except Exception as e:
        response_status = jsonify({"error": "New user not created", "message": f"{e}"}), 400

    return procedure_status