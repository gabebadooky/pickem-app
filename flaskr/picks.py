from flask import Blueprint, g, jsonify, request, session

from . import mysql_db

bp = Blueprint('picks', __name__, url_prefix='/picks')

@bp.get('/<str:username>')
def get_user_picks(username):
    try:
        sql_statement = "SELECT * FROM GET_PICKS_VW WHERE USERNAME = '{username}';"
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