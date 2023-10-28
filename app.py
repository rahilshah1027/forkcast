import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import flask_login

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.get("/")
def home():
    return render_template("login.html")
    
def get_reports():
    return None

def create_status():
    return None