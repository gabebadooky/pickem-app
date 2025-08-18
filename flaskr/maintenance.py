from flask import Blueprint, jsonify
from . import mysql_db

bp: Blueprint = Blueprint("maintenance", __name__, url_prefix="/maintenance")

@bp.get("/")
def call_is_system_under_maintenance_view() -> tuple:
    try:
        is_system_under_maintenance: int = mysql_db.call_view("SELECT * FROM IS_SYSTEM_UNDER_MAINTENANCE_VW;")
        response_status = jsonify({"isTrue": is_system_under_maintenance[0]["IS_TRUE"]}), 200
    except Exception as e:
        response: dict = jsonify({"error": "Request Error", "message": f"{e}"})
        response_status: tuple = response, 400
    return response_status
