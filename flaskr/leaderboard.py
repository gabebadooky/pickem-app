from flask import Blueprint, jsonify, request

from . import mysql_db

bp: Blueprint = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")


@bp.get("/")
def get_leaderboard() -> tuple:
    try:
        sql_statement: str = f"SELECT * FROM GET_LEADERBOAD_VW;"
        leaderboard: list = mysql_db.call_view(sql_statement)

        camel_cased_list: list = []
        for x in range(len(leaderboard)):
            camel_cased_row: dict = {
                "userID": leaderboard[x]["USER_ID"],
                "week": leaderboard[x]["WEEK"],
                "league": leaderboard[x]["LEAGUE"],
                "year": leaderboard[x]["YEAR"],
                "awayPowerConference": leaderboard[x]["AWAY_POWER_CONFERENCE"],
                "homePowerConference": leaderboard[x]["HOME_POWER_CONFERENCE"],
                "points": leaderboard[x]["POINTS"]
            }
            camel_cased_list.append(camel_cased_row)
        response_status: tuple = jsonify(camel_cased_list), 200
    except Exception as e:
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    
    return response_status