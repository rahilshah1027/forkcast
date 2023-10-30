import os
import psycopg2
import bcrypt
from dotenv import load_dotenv
from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


#password = b"hellohihi"
#hashed = bcrypt.hashpw(password, bcrypt.gensalt())
#print(bcrypt.checkpw(password, hashed))

load_dotenv()
app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(20) NOT NULL UNIQUE,
        password VARCHAR(60) NOT NULL
        );
    """

insert_query = """
    INSERT INTO users (username, email, password)
    VALUES (%s, %s, %s)
    RETURNING id;
    """

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def get_reports():
    return None

def create_status():
    return None

@app.get("/")
def main():
    # when u get to the first page check if the user is already logged in
    # if they are send them to hoem page
    # if not send them to the login page
    #if current_user.is_authenticated:
    #    return render_template("home.html", user=current_user)
    if connection:
        print("connected to db")
    return render_template("login.html")
    
@app.route("/login", methods=["POST", "GET"])
def login():
    name = request.form["username"]
    password = request.form["password"]
    return render_template("home.html", name=name)

@app.route("/register", methods=["POST", "GET"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    new_user = User(username, password)

    return "welcome to register page"

