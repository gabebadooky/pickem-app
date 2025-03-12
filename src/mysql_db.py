import mysql.connector
from credentials import mysql_connection_string


def execute_proc(sql: str) -> str:
    conn = mysql.connector.connect(**mysql_connection_string.config)
    cursor = conn.cursor()
    cursor.execute(sql)
    status = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return status


def call_view(sql: str) -> list:
    conn = mysql.connector.connect(**mysql_connection_string.config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return results