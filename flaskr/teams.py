from flask import Blueprint, jsonify, request
from . import mysql_db

bp = Blueprint('teams', __name__, url_prefix='/games')

@bp.get('/teams')
def get_games(week) -> tuple:
    try:
        sql_statement = f"SELECT * FROM GET_TEAMS_VW;"
        games = mysql_db.call_view(sql_statement)

        if len(games) == 0:
            response_status = jsonify({"error": "Not Found", "message": f"No records retrieved from given query:\n{sql_statement}"}), 400
        else:
            camel_cased_list = []
            for x in range(len(games)):
                camel_cased_pick = {
                    "teamID": games[x]["TEAM_ID"],
                    "cbsCode": games[x]["CBS_CODE"],
                    "espnCode": games[x]["ESPN_CODE"],
                    "foxCode": games[x]["FOX_CODE"],
                    "vegasCode": games[x]["VEGAS_CODE"],
                    "conferenceCode": games[x]["CONFERENCE_CODE"],
                    "conferenceName": games[x]["CONFERENCE_NAME"],
                    "divisionName": games[x]["DIVISION_NAME"],
                    "teamName": games[x]["TEAM_NAME"],
                    "teamMascot": games[x]["TEAM_MASCOT"],
                    "powerConference": games[x]["POWER_CONFERENCE"],
                    "team_logo_url": games[x]["TEAM_LOGO_URL"],
                    "primaryColor": games[x]["PRIMARY_COLOR"],
                    "alternateColor": games[x]["ALTERNATE_COLOR"]
                }
                camel_cased_list.append(camel_cased_pick)
            response_status = jsonify(camel_cased_list), 200
    except Exception as e:
        response = jsonify({"error": "Request Error", "message": e})
        response_status = response, 400
    
    return response_status