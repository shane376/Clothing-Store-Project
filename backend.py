from flask import Flask, Jsonify
import mysql.connector

app = Flask(__name__)

#Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='store',
        user='user',
        password='password'
    )