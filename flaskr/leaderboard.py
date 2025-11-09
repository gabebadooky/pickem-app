from flask import Blueprint, jsonify, request

from . import mysql_db

bp: Blueprint = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")


@bp.get("/<week>")
def get_week_leaderboard(week) -> tuple:
    try:
        sql_statement: str = f"SELECT * FROM LEADERBOAD_VW WHERE WEEK = {week};"
        leaderboard: list = mysql_db.call_view(sql_statement)

        camel_cased_list: list = []
        for x in range(len(leaderboard)):
            camel_cased_row: dict = {
                "userID": leaderboard[x]["USER_ID"],
                "displayName": leaderboard[x]["DISPLAY_NAME"],
                "year": leaderboard[x]["YEAR"],
                "week": leaderboard[x]["WEEK"],
                "league": leaderboard[x]["LEAGUE"],
                "top25": leaderboard[x]["TOP_25_MATCHUP"],
                "powerConference": leaderboard[x]["P4_MATCHUP"],
                "nonPowerConference": leaderboard[x]["G6_MATCHUP"],
                "totalPoints": leaderboard[x]["TOTAL_POINTS"],
                "correctPicks": leaderboard[x]["CORRECT_PICKS"],
                "incorrectPicks": leaderboard[x]["INCORRECT_PICKS"],
                "picksSubmitted": leaderboard[x]["PICKS_SUBMITTED"]
            }
            camel_cased_list.append(camel_cased_row)
        response_status: tuple = jsonify(camel_cased_list), 200
    except Exception as e:
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    
    return response_status


@bp.get("/season")
def get_week_leaderboard(week) -> tuple:
    try:
        sql_statement: str = f"SELECT * FROM LEADERBOAD_VW;"
        leaderboard: list = mysql_db.call_view(sql_statement)

        camel_cased_list: list = []
        for x in range(len(leaderboard)):
            camel_cased_row: dict = {
                "userID": leaderboard[x]["USER_ID"],
                "displayName": leaderboard[x]["DISPLAY_NAME"],
                "year": leaderboard[x]["YEAR"],
                "week": leaderboard[x]["WEEK"],
                "league": leaderboard[x]["LEAGUE"],
                "top25": leaderboard[x]["TOP_25_MATCHUP"],
                "powerConference": leaderboard[x]["P4_MATCHUP"],
                "nonPowerConference": leaderboard[x]["G6_MATCHUP"],
                "totalPoints": leaderboard[x]["TOTAL_POINTS"],
                "correctPicks": leaderboard[x]["CORRECT_PICKS"],
                "incorrectPicks": leaderboard[x]["INCORRECT_PICKS"],
                "picksSubmitted": leaderboard[x]["PICKS_SUBMITTED"]
            }
            camel_cased_list.append(camel_cased_row)
        response_status: tuple = jsonify(camel_cased_list), 200
    except Exception as e:
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    
    return response_status



@bp.get("/")
def get_leaderboard() -> tuple:
    try:
        sql_statement: str = f"SELECT * FROM GET_LEADERBOAD_VW;"
        leaderboard: list = mysql_db.call_view(sql_statement)

        camel_cased_list: list = []
        for x in range(len(leaderboard)):
            camel_cased_row: dict = {
                "userID": leaderboard[x]["USER_ID"],
                "displayName": leaderboard[x]["DISPLAY_NAME"],
                "week": leaderboard[x]["WEEK"],
                "league": leaderboard[x]["LEAGUE"],
                "year": leaderboard[x]["YEAR"],
                "awayPowerConference": leaderboard[x]["AWAY_POWER_CONFERENCE"],
                "homePowerConference": leaderboard[x]["HOME_POWER_CONFERENCE"],
                "awayRanking": leaderboard[x]["AWAY_RANKING"],
                "homeRanking": leaderboard[x]["HOME_RANKING"],
                "points": leaderboard[x]["POINTS"],
                "correctPicks": leaderboard[x]["CORRECT_PICK"],
                "incorrectPicks": leaderboard[x]["INCORRECT_PICK"]
            }
            camel_cased_list.append(camel_cased_row)
        response_status: tuple = jsonify(camel_cased_list), 200
    except Exception as e:
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    
    return response_status