import os
import psycopg2
import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from dotenv import load_dotenv
from flask import Flask, request, render_template, session, url_for, redirect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

#password = b"hellohihi"
#hashed = bcrypt.hashpw(password, bcrypt.gensalt())
#print(bcrypt.checkpw(password, hashed))

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    cur = connection.cursor()
    cur.execute("SELECT username FROM users WHERE id = %s", (int(user_id,)))
    user = cur.fetchone()
    cur.close()
    return user

create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(20) NOT NULL UNIQUE,
        password VARCHAR(60) NOT NULL
        );
    """

insert_query = """
    INSERT INTO users (username, password)
    VALUES (%s, %s)
    """

class RegisterForm(FlaskForm):
    username = StringField(validators=
                           [InputRequired(), Length(min=4, max=20)],
                            render_kw={"placeholder": "Username"})
    password = PasswordField(validators=
                           [InputRequired(), Length(min=8, max=20)],
                            render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        connection = psycopg2.connect(url)
        cur = connection.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s", (str(username,)))
        existing_user = cur.fetchone()
        if existing_user:
            raise ValidationError(
                "Username already exists. Please create a different one."
            )

class LoginForm(FlaskForm):
    username = StringField(validators=
                           [InputRequired(), Length(min=4, max=20)],
                            render_kw={"placeholder": "Username"})
    password = PasswordField(validators=
                           [InputRequired(), Length(min=8, max=20)],
                            render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.get("/")
def main():
    cur = connection.cursor()
    cur.execute(create_table_query)
    cur.close()
    return redirect(url_for("login"))
    
@app.route("/login", methods=["POST", "GET"])
def login():
    cur = connection.cursor()
    login = LoginForm()
    if login.validate_on_submit():
        cur.execute("SELECT username FROM users WHERE username = %s", (str(login.username),))
        cur_user = cur.fetchone()
        print(cur_user)
        if cur_user:
            cur.execute("SELECT password FROM users WHERE password = %s", (login.password,))
            if bcrypt.checkpw(login.password.encode("utf-8"), cur.fetchone()):
                login_user(cur_user)
                cur.close()
                return redirect(url_for("dashboard", data=login.username))
        else:
            print("username or password doesnt exist please register")
    return render_template("login.html", login=login)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    cur = connection.cursor()
    register = RegisterForm()
    if register.validate_on_submit():
        hashed_password = bcrypt.hashpw(register.password.encode("utf-8"), bcrypt.gensalt())
        # create new user with hashed password
        new_user = User(username=register.username, password=hashed_password) 
        # add user to database
        cur.execute(insert_query, new_user.username, new_user.password)
        connection.commit()
        cur.close()
        return redirect(url_for("login"))
    return render_template("register.html", register=register)

