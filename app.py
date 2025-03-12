from flask import Flask
import mysql_db

app = Flask(__name__)

@app.route('/')
def hello_world():
    return {
        'hello': 'world'
    }