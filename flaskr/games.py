from flask import Blueprint, jsonify, request
from . import mysql_db

bp = Blueprint('games', __name__, url_prefix='/games')

@bp.get('/games')
def get_games(week) -> tuple:
    try:
        sql_statement = f"SELECT * FROM GET_GAMES_VW;"
        games = mysql_db.call_view(sql_statement)

        if len(games) == 0:
            response_status = jsonify({"error": "Not Found", "message": f"No records retrieved from given query:\n{sql_statement}"}), 400
        else:
            camel_cased_list = []
            for x in range(len(games)):
                camel_cased_pick = {
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""],
                    "": games[x][""]
                }
                camel_cased_list.append(camel_cased_pick)
            response_status = jsonify(camel_cased_list), 200
    except Exception as e:
        response = jsonify({"error": "Request Error", "message": e})
        response_status = response, 400
    
    return response_status