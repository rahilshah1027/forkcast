from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# visit the homepage and you have to sign in with bu.edu email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'