import jwt, os, datetime
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)


# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


print(server.config["MYSQL_HOST"])


@server.route("/login", methods=["POST"])
def login():
    auth = request.authoriation
    if not auth:
        return jsonify({"message": "Missing Authorization header"}), 401
      
    # check for username nad passowrd
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )
    
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        
        if auth.password != password or auth.username != email:
            return jsonify({"message": "Invalid credentials"}), 401
        
            