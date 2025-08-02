from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from . import mysql_db

bp: Blueprint = Blueprint("teams", __name__, url_prefix="/teams")

@bp.get("/")
def get_teams() -> tuple:
    try:
        sql_statement: str = f"SELECT * FROM GET_TEAMS_VW WHERE TEAM_ID IS NOT NULL;"
        teams: list = mysql_db.call_view(sql_statement)

        if len(teams) == 0:
            response_status: tuple = jsonify({"error": "Not Found", "message": f"No records retrieved from given query:\n{sql_statement}"}), 400
        else:
            camel_cased_list: list = []
            for x in range(len(teams)):
                camel_cased_pick: dict = {
                    "teamID": teams[x]["TEAM_ID"],
                    "league": teams[x]["LEAGUE"],
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
                    "teamLogoUrl": teams[x]["TEAM_LOGO_URL"],
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
            response_status: tuple = jsonify(camel_cased_list), 200
    except Exception as e:
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    
    return response_status


@bp.get("/notes/<user_id>")
def get_team_notes(user_id) -> tuple:
    try:
        sql_statement: str = f"SELECT USER_ID, TEAM_ID, NOTES FROM USER_TEAM_NOTES WHERE USER_ID = {user_id};"
        notes: list = mysql_db.call_view(sql_statement)

        if len(notes) == 0:
            response_status: tuple = jsonify({"error": "Request Error", "message": f"No records retrieved from given query: {sql_statement}"}), 400
        else:
            camel_cased_list: list = []
            for x in range(len(notes)):
                notes_bytes = notes[x]["NOTES"]
                if notes_bytes is None: 
                    notes_property = ""
                else:
                    notes_property = notes[x]["NOTES"].decode("utf-8") # base64.b64decode(notes[x]["NOTES"]).decode("utf-8")
                camel_cased_note: dict = {
                    "userID": notes[x]["USER_ID"],
                    "teamID": notes[x]["TEAM_ID"],
                    "notes": notes_property
                }
                camel_cased_list.append(camel_cased_note)
            response_status: tuple = jsonify(camel_cased_list), 200

    except Exception as e:
        response_status: tuple = jsonify({"error": "Request Error", "message": f"{e}"})
    return response_status


@bp.post("/update-notes")
@jwt_required()
def update_team_notes() -> tuple:
    """
    Body Example:
    [
        {
            "userID": <int>, (REQUIRED)
            "teamID": <str>, (REQUIRED)
            "notes": <str>
        }
    ]
    """
    data = request.json
    current_user = int(get_jwt_identity())
    if current_user != data["userID"]:
        response_status = jsonify({"error": "Cannot update another user's picks!"})
    else:
        try:
            procedure_output: str = sql_update_team_notes(data)
            if procedure_output == "Success":
                response_status: tuple = jsonify(message = "Success"), 201
            else:
                response_status: tuple = jsonify({"error": "Team Notes not updated", "message": f"{procedure_output}"})
        except Exception as e:
            response_status: tuple = jsonify({"error": "Team Notes not updated", "message": f"{e}"}), 400
    return response_status
    


def sql_update_team_notes(data: dict) -> str:
    user_id: int = data["userID"]
    team_id: str = data["teamID"]
    notes: bytes = data["notes"]
    sql_statement: str = f"CALL PROC_UPDATE_TEAM_NOTES({user_id}, '{team_id}', '{notes}', @status);"
    procedure_output: str = mysql_db.execute_proc(sql_statement)
    return procedure_output