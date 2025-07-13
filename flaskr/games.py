from flask import Blueprint, jsonify
from . import mysql_db

bp: Blueprint = Blueprint("games", __name__, url_prefix="/games")

@bp.get("/")
def get_games() -> tuple:
    try:
        sql_statement: str = f"SELECT * FROM GET_GAMES_VW ORDER BY DATE, TIME, LEAGUE;"
        games: list = mysql_db.call_view(sql_statement)

        if len(games) == 0:
            response_status: tuple = jsonify({"error": "Not Found", "message": f"No records retrieved from given query:\n{sql_statement}"}), 400
        else:
            camel_cased_list: list = []
            for x in range(len(games)):
                camel_cased_pick: dict = {
                    "gameID": games[x]["GAME_ID"],
                    "league": games[x]["LEAGUE"],
                    "week": games[x]["WEEK"],
                    "year": games[x]["YEAR"],
                    "awayTeamID": games[x]["AWAY_TEAM_ID"],
                    "homeTeamID": games[x]["HOME_TEAM_ID"],
                    "date": games[x]["DATE"],
                    "time": str(games[x]["TIME"]),
                    "tvCoverage": games[x]["TV_COVERAGE"],
                    "stadium": games[x]["STADIUM"],
                    "city": games[x]["CITY"],
                    "state": games[x]["STATE"],
                    "gameFinished": games[x]["GAME_FINISHED"],
                    "cbsCode": games[x]["CBS_CODE"],
                    "cbsAwayMoneyline": games[x]["CBS_AWAY_MONEYLINE"],
                    "cbsHomeMoneyline": games[x]["CBS_HOME_MONEYLINE"],
                    "cbsAwaySpread": games[x]["CBS_AWAY_SPREAD"],
                    "cbsHomeSpread": games[x]["CBS_HOME_SPREAD"],
                    "cbsOverUnder": games[x]["CBS_OVER_UNDER"],
                    "cbsAwayWinPercentage": games[x]["CBS_AWAY_WIN_PERCENTAGE"],
                    "cbsHomeWinPercentage": games[x]["CBS_HOME_WIN_PERCENTAGE"],
                    "espnCode": games[x]["ESPN_CODE"],
                    "espnAwayMoneyline": games[x]["ESPN_AWAY_MONEYLINE"],
                    "espnHomeMoneyline": games[x]["ESPN_HOME_MONEYLINE"],
                    "espnAwaySpread": games[x]["ESPN_AWAY_SPREAD"],
                    "espnHomeSpread": games[x]["ESPN_HOME_SPREAD"],
                    "espnOverUnder": games[x]["ESPN_OVER_UNDER"],
                    "espnAwayWinPercentage": games[x]["ESPN_AWAY_WIN_PERCENTAGE"],
                    "foxCode": games[x]["FOX_CODE"],
                    "foxAwayMoneyline": games[x]["FOX_AWAY_MONEYLINE"],
                    "foxHomeMoneyline": games[x]["FOX_HOME_MONEYLINE"],
                    "foxAwaySpread": games[x]["FOX_AWAY_SPREAD"],
                    "foxHomeSpread": games[x]["FOX_HOME_SPREAD"],
                    "foxOverUnder": games[x]["FOX_OVER_UNDER"],
                    "foxAwayWinPercentage": games[x]["FOX_AWAY_WIN_PERCENTAGE"],
                    "foxHomeWinPercentage": games[x]["FOX_HOME_WIN_PERCENTAGE"],
                    "vegasCode": games[x]["VEGAS_CODE"],
                    "vegasAwayMoneyline": games[x]["VEGAS_AWAY_MONEYLINE"],
                    "vegasHomeMoneyline": games[x]["VEGAS_HOME_MONEYLINE"],
                    "vegasAwaySpread": games[x]["VEGAS_AWAY_SPREAD"],
                    "vegasHomeSpread": games[x]["VEGAS_HOME_SPREAD"],
                    "vegasOverUnder": games[x]["VEGAS_OVER_UNDER"],
                    "vegasAwayWinPercentage": games[x]["VEGAS_AWAY_WIN_PERCENTAGE"],
                    "vegasHomeWinPercentage": games[x]["VEGAS_HOME_WIN_PERCENTAGE"],
                    
                    "awayQ1BoxScore": games[x]["AWAY_Q1_BOX_SCORE"],
                    "awayQ2BoxScore": games[x]["AWAY_Q2_BOX_SCORE"],
                    "awayQ3BoxScore": games[x]["AWAY_Q3_BOX_SCORE"],
                    "awayQ4BoxScore": games[x]["AWAY_Q4_BOX_SCORE"],
                    "awayOvertimeBoxScore": games[x]["AWAY_OVERTIME_BOX_SCORE"],
                    "awayTotalBoxScore": games[x]["AWAY_TOTAL_BOX_SCORE"],

                    "homeQ1BoxScore": games[x]["HOME_Q1_BOX_SCORE"],
                    "homeQ2BoxScore": games[x]["HOME_Q2_BOX_SCORE"],
                    "homeQ3BoxScore": games[x]["HOME_Q3_BOX_SCORE"],
                    "homeQ4BoxScore": games[x]["HOME_Q4_BOX_SCORE"],
                    "homeOvertimeBoxScore": games[x]["HOME_OVERTIME_BOX_SCORE"],
                    "homeTotalBoxScore": games[x]["HOME_TOTAL_BOX_SCORE"]
                }
                camel_cased_list.append(camel_cased_pick)
            response_status: tuple = jsonify(camel_cased_list), 200
    except Exception as e:
        print(f"Request Error: {e}")
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    
    return response_status