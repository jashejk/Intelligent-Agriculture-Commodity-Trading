import os

import bcrypt
from flask import Flask, render_template, request, redirect, session, flash, url_for
from pymongo import MongoClient

app = Flask(__name__, static_url_path="/static", static_folder="static/")
client = MongoClient("mongodb+srv://298a:admin298a@298a.kqrtzfx.mongodb.net/?retryWrites=true&w=majority")
db = client["298a"]


@app.route("/", methods=["POST", "GET"])
def index():
    if "email" in session:
        data = dict()
        data["name"] = session["name"]
        print(data["name"])
        return render_template("index.html", data=data)

    return redirect("/signin")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        users = db["users"]

        if users.find_one({"email": email}):
            print("Email already taken")
            flash("Email already taken", "signup")
            return render_template("auth.html")

        hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_id = users.insert_one({"email": email, "password": hashed_pwd, "name": name}).inserted_id
        print("used_id", user_id)
        return redirect("/signin")

    return render_template("auth.html")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        users = db["users"]
        user = users.find_one({"email": email})

        if not user:
            print("Email invalid")
            flash("Email invalid", "signin")
            return render_template("auth.html")

        if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            print("Password invalid")
            flash("Password invalid", "signin")
            return render_template("auth.html")

        print("Valid email and pwd")
        session["email"] = email
        session["name"] = user["name"]
        return redirect("/")

    return render_template("auth.html")


@app.route("/signout")
def signout():
    session.pop("email", None)
    flash("Successfully signed out", "signout")
    return redirect("/")


@app.route("/crops", methods=["GET", "POST"])
def crops():
    data = dict()
    if request.method == "POST":
        print(request.form["crop-name"])
        crop = request.form["crop-name"]
        if "email" in session:
            data = dict()
            data["name"] = session["name"]
            print(data["name"])
        else:
            data["name"] = "Profile"
    return render_template("index.html", data=data)


@app.route("/analysis", methods=["POST", "GET"])
def analysis():
    # if "email" in session:
    #     return render_template("index.html")
    # else:
    #     return redirect("/auth")
    return render_template("analysis.html")


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=80, debug=True)
