import os

import bcrypt
import pickle as pickle
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
from keras.models import load_model
from flask_cors import CORS

app = Flask(__name__, static_url_path="/static", static_folder="static/")
client = MongoClient("mongodb+srv://298a:admin298a@298a.kqrtzfx.mongodb.net/?retryWrites=true&w=majority")
db = client["298a"]
cors = CORS(app, origins="*")

corn_top_news_list = None
wheat_top_news_list = None
oats_top_news_list = None
sorghum_top_news_list = None


@app.route("/", methods=["POST", "GET"])
def index():
    return redirect("/dashboard")


@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if "email" in session:
        data = dict()
        data["name"] = session["name"]
        print(data["name"])
        corn_df = pd.read_pickle("models/corn_news_rank.pkl")
        wheat_df = pd.read_pickle("models/wheat_news_rank.pkl")

        corn_top_news_list = corn_df.to_dict("records")
        wheat_top_news_list = wheat_df.to_dict("records")

        print(corn_top_news_list[0]["media"])

        return render_template("index.html", data=data, corn_top_news_list=corn_top_news_list,
                               wheat_top_news_list=wheat_top_news_list)
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


@app.route("/api/crops/", methods=["GET"])
def crop_select():
    crop_name = request.args.get("crop")
    response = {}
    response["market"] = "sup"
    if crop_name == "corn":
        response["dashboardID"] = "https://public.tableau.com/views/Historicalanalysiscornprice/Sheet1?debug=false&:language=en-US&:display_count=y&:origin=viz_share_link"
        response["newsArticles"] = corn_top_news_list
    elif crop_name == "wheat":
        response["dashboardID"] = "https://public.tableau.com/views/HistoricAnalysisofWheat/Sheet1?:language=en-US&:display_count=n&:origin=viz_share_link"
        response["newsArticles"] = wheat_top_news_list
    elif crop_name == "oats":
        response["dashboardID"] = "https://public.tableau.com/views/Historicalanalysiscornprice/Sheet1?:language=en-US&:display_count=y&:origin=viz_share_link"
        response["newsArticles"] = corn_top_news_list
    elif crop_name == "sorghum":
        response["dashboardID"] = "https://public.tableau.com/views/Historicalanalysiscornprice/Sheet1?:language=en-US&:display_count=y&:origin=viz_share_link"
        response["newsArticles"] = corn_top_news_list
    else:
        response["dashboardID"] = "https://public.tableau.com/views/Historicalanalysiscornprice/Sheet1?:language=en-US&:display_count=y&:origin=viz_share_link"
        response["newsArticles"] = corn_top_news_list

    return jsonify(response)


@app.route("/signout")
def signout():
    session.pop("email", None)
    flash("Successfully signed out", "signout")
    return redirect("/")


@app.route("/crops", methods=["GET", "POST"])
def crops():
    if request.method == "POST":
        print(request.form["crop-name"])
        crop = request.form["crop-name"]
    return render_template("index.html")


@app.route("/analysis", methods=["POST", "GET"])
def analysis():
    # if "email" in session:
    #     return render_template("index.html")
    # else:
    #     return redirect("/auth")
    return render_template("analysis.html")


def load_modell():
    model = load_model('models/model.h5', compile=False)
    model.compile()

    with open('models/seq.pkl', 'rb') as f:
        seq = pickle.load(f)

    realtime_pred = model.predict(seq)
    realtime_label_pred = np.where(realtime_pred > 0.5, 1, 0)
    df_f = pd.DataFrame(realtime_label_pred, columns=['label'])
    mode = int(df_f['label'].mode())

    print(f"mode = {mode}")

if __name__ == "__main__":
    load_modell()

    corn_df = pd.read_pickle("models/corn_news_rank.pkl")
    wheat_df = pd.read_pickle("models/wheat_news_rank.pkl")

    corn_top_news_list = corn_df.to_dict("records")
    wheat_top_news_list = wheat_df.to_dict("records")

    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=8080, debug=True)
