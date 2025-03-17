from flask import Blueprint, g, jsonify, request, session

from . import mysql_db

bp = Blueprint('picks', __name__, url_prefix='/picks')

@bp.get('/<str:username>')
def get_user_picks(username):
    try:
        sql_statement = "SELECT * FROM GET_PICKS_VW WHERE USERNAME = '{username}';"
        picks = mysql_db.call_view(sql_statement)
    except Exception as e:
        response = jsonify({"error": "Request Error", "message": f"{e}"})
        return response 400
    
    if len(picks) == 0:
        response = jsonify({"error": "Not Found", "message": "No picks found associated to the provided username."})
        return response, 406
    else:
        response = jsonify("picks": picks)
        return response, 200