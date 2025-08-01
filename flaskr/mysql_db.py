import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()
config = {
    "user": "gbaduqui",
    "password": os.getenv("MYSQL_PASSWORD"),
    "host": "pickem-db-gb-pickem-db.i.aivencloud.com",
    "port": 26264,
    "database": "PICKEM_DB",
    "auth_plugin": "caching_sha2_password"
}

def execute_proc(sql: str) -> str:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print(sql)
    cursor.execute(sql)
    status = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return status


def call_view(sql: str) -> list:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_user_by_username(username: str) -> dict:
    sql: str = f"SELECT * FROM USERS WHERE USERNAME = '{username}';"
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_id(user_id: str) -> dict:
    sql: str = f"SELECT * FROM USERS WHERE USER_ID = {user_id};"
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return user