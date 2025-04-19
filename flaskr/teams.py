from flask import Blueprint, jsonify
from . import mysql_db

bp = Blueprint('teams', __name__, url_prefix='/teams')

@bp.get('/')
def get_teams() -> tuple:
    try:
        sql_statement = f"SELECT * FROM GET_TEAMS_VW;"
        teams = mysql_db.call_view(sql_statement)

        if len(teams) == 0:
            response_status = jsonify({"error": "Not Found", "message": f"No records retrieved from given query:\n{sql_statement}"}), 400
        else:
            camel_cased_list = []
            for x in range(len(teams)):
                camel_cased_pick = {
                    "teamID": teams[x]["TEAM_ID"],
                    "cbsCode": teams[x]["CBS_CODE"],
                    "espnCode": teams[x]["ESPN_CODE"],
                    "foxCode": teams[x]["FOX_CODE"],
                    "vegasCode": teams[x]["VEGAS_CODE"],
                    "conferenceCode": teams[x]["CONFERENCE_CODE"],
                    "conferenceName": teams[x]["CONFERENCE_NAME"],
                    "divisionName": teams[x]["DIVISION_NAME"],
                    "teamName": teams[x]["TEAM_NAME"],
                    "teamMascot": teams[x]["TEAM_MASCOT"],
                    "powerConference": teams[x]["POWER_CONFERENCE"],
                    "team_logo_url": teams[x]["TEAM_LOGO_URL"],
                    "primaryColor": teams[x]["PRIMARY_COLOR"],
                    "alternateColor": teams[x]["ALTERNATE_COLOR"],
                    "overallWins": teams[x]["OVERALL_WINS"],
                    "overallLosses": teams[x]["OVERALL_LOSSES"],
                    "overallTies": teams[x]["OVERALL_TIES"],
                    "conferenceWins": teams[x]["CONFERENCE_WINS"],
                    "conferenceLosses": teams[x]["CONFERENCE_LOSSES"],
                    "conferenceTies": teams[x]["CONFERENCE_TIES"],
                }
                camel_cased_list.append(camel_cased_pick)
            response_status = jsonify(camel_cased_list), 200
    except Exception as e:
        response = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status = response, 400
    
    return response_status