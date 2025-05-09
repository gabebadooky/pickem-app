from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from . import mysql_db

bp = Blueprint("picks", __name__, url_prefix="/picks")


@bp.get("/<username>")
def get_user_picks(username) -> tuple:
    try:
        sql_statement = f"SELECT * FROM GET_PICKS_VW WHERE USERNAME = '{username}';"
        picks = mysql_db.call_view(sql_statement)

        if len(picks) == 0:
            response_status = jsonify({"error": "Not Found", "message": "No picks found associated to the provided username."}), 406
        else:
            camel_cased_list = []
            for x in range(len(picks)):
                camel_cased_pick = {
                    "gameID": picks[x]["GAME_ID"],
                    "teamPicked": picks[x]["TEAM_PICKED"],
                    "pickWeight": picks[x]["PICK_WEIGHT"],
                    "username": picks[x]["USERNAME"]
                }
                camel_cased_list.append(camel_cased_pick)
            
            response_status = jsonify(camel_cased_list), 200
    
    except Exception as e:
        response = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status = response, 400
        
    return response_status


@bp.post("/submit")
@jwt_required()
def submit_pick() -> tuple:
    """
    Body Example:
    [
        {
            "username": <int>, (REQUIRED)
            "gameID": <str>, (REQUIRED)
            "teamPicked": <str>, (REQUIRED)
            "pickWeight": <str> (REQUIRED)
        }
    ]
    """
    data = request.json
    print("Here :)")
    header, payload, signature = request.headers["Authorization"].split(".")
    print("Header: ", header)
    print("Payload: ", payload)
    print("Signature: ", signature)
    current_user = get_jwt_identity()
    print(current_user)
    try:
        if ("username" not in data) or ("gameID" not in data) or ("teamPicked" not in data) or ("pickWeight" not in data):
            response_status = jsonify({"error": "Required parameter missing from request", "message": "Required parameters: userID, gameID, teamPicked, pickWeight"})
        else:
            procedure_output = sql_update_pick(data)
            if procedure_output == "Success":
                response_status = jsonify(message = "Success"), 201
            else:
                response_status = jsonify({"error": f"Error occurred updating Pick database record!", "message": procedure_output}), 400
    except Exception as e:
        response_status = jsonify({"error": f"Error occurred calling submit endpoint!", "message": e}), 400
    return response_status



def sql_update_pick(data: dict) -> str:
    username = data["username"]
    game_id = data["gameID"]
    team_picked = data["teamPicked"]
    pick_weight = data["pickWeight"]
    sql_statement = f"CALL PROC_SUBMIT_PICK('{username}', '{game_id}', '{team_picked}', '{pick_weight}', @status);"
    procedure_output = mysql_db.execute_proc(sql_statement)
    return procedure_output