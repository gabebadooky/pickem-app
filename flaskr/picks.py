from flask import Blueprint, jsonify, request

from . import mysql_db

bp = Blueprint('picks', __name__, url_prefix='/picks')

@bp.get('/<str:username>')
def get_user_picks(username) -> tuple:
    try:
        sql_statement = f"SELECT * FROM GET_USER_PICKS_VW WHERE USERNAME = '{username}';"
        picks = mysql_db.call_view(sql_statement)

        if len(picks) == 0:
            response_status = jsonify({"error": "Not Found", "message": "No picks found associated to the provided username."}), 406
        else:
            response_status = jsonify({
                'username': picks['username'],
                'gameID': picks['game_id'],
                'teamPicked': picks['team_picked'],
                'pickWeight': picks['pick_weight']
            }), 200
    
    except Exception as e:
        response = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status = response, 400
        
    return response_status


@bp.post('/submit')
def submit_pick() -> tuple:
    data = request.json
    try:
        procedure_output = sql_update_pick(data)
        if procedure_output == 'Success':
            response_status = jsonify(message = "Success"), 201
        else:
            response_status = jsonify({"error": f"Pick {data['pick']} not updated", "message": procedure_output}), 400
    except Exception as e:
        response_status = jsonify({"error": f"Pick {data['pick']} not updated", "message": procedure_output}), 400
    return response_status



def sql_update_pick(data: dict) -> str:
    user_id = data['userID']
    game_id = data['gameID']
    team_picked = data['teamPicked']
    pick_weight = data['pickWeight']
    sql_statement = f"CALL PROC_SUBMIT_PICK('{user_id}', '{game_id}', '{team_picked}', '{pick_weight}', @status);"
    procedure_output = mysql_db.execute_proc(sql_statement)
    return procedure_output