import os

from flask_bcrypt import Bcrypt
import pickle as pickle
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import pickle
import jwt
import re
from tensorflow.keras.models import load_model
from flask_cors import CORS

app = Flask(__name__, static_url_path="/static", static_folder="static/")
client = MongoClient("mongodb+srv://298a:admin298a@298a.kqrtzfx.mongodb.net/?retryWrites=true&w=majority")
db = client["298a"]
cors = CORS(app, origins="*")
bcrypt = Bcrypt(app)

corn_top_news_list = None
wheat_top_news_list = None
oats_top_news_list = None
sorghum_top_news_list = None
mode = None


def calculate_time_difference(input_datetime):
    # Current date and time
    current_datetime = datetime.now()

    # Convert input string to datetime object
    input_datetime = datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")

    # Calculate the time difference
    time_difference = current_datetime - input_datetime

    # Extract the number of days and hours from the time difference
    days_difference = time_difference.days
    hours_difference = time_difference.seconds // 3600

    # Generate the output based on the time difference
    if days_difference == 0 and hours_difference == 0:
        output = "Last updated just now"
    elif days_difference == 0:
        output = f"Last updated {hours_difference} hour{'s' if hours_difference > 1 else ''} ago"
    elif days_difference == 1:
        output = "Last updated 1 day ago"
    else:
        output = f"Last updated {days_difference} day{'s' if days_difference > 1 else ''} ago"

    return output


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def is_valid_input(**kwargs):
    email = kwargs.get("email")
    if email is not None and not is_valid_email(email):
        return False

    for arg_name, arg_value in kwargs.items():
        if arg_value is None:
            return False

    return True


def update_times():
    i = 0
    for i in range(len(corn_top_news_list)):
        published_date = corn_top_news_list[i]["published_date"]
        corn_top_news_list[i]["time"] = calculate_time_difference(published_date)
        pass

    i = 0
    for i in range(len(wheat_top_news_list)):
        published_date = wheat_top_news_list[i]["published_date"]
        wheat_top_news_list[i]["time"] = calculate_time_difference(published_date)
        pass

    i = 0
    for i in range(len(sorghum_top_news_list)):
        published_date = sorghum_top_news_list[i]["published_date"]
        sorghum_top_news_list[i]["time"] = calculate_time_difference(published_date)
        pass

    i = 0
    for i in range(len(oats_top_news_list)):
        published_date = oats_top_news_list[i]["published_date"]
        oats_top_news_list[i]["time"] = calculate_time_difference(published_date)
        pass


@app.route("/api/signup", methods=["POST"])
def signup():
    users = db["users"]
    name = request.json['name']
    email = request.json['email']
    password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')

    if not is_valid_input(name=name, email=email, password=password):
        return jsonify({"error": "Invalid input"}), 400

    user_id = users.insert_one({'name': name, 'email': email, 'password': password}).inserted_id
    token = jwt.encode({'user': email, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                       app.secret_key)
    return jsonify({'token': token})


@app.route("/api/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        email = request.json["email"]
        password = request.json["password"]

        if not is_valid_input(email=email, password=password):
            return jsonify({"error": "Invalid input"}), 400

        users = db["users"]

        response = users.find_one({'email': email})

        if response:
            if bcrypt.check_password_hash(response['password'], password):
                access_token = jwt.encode(
                    {'user': email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.secret_key)
                result = jsonify({"token": access_token})
            else:
                result = jsonify({"error": "Invalid username and password"})
        else:
            result = jsonify({"result": "No results found"})
        return result


@app.route('/api/validateToken', methods=['GET'])
def validate_token():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({'message': 'No authorization header provided'}), 401

    try:
        # remove 'Bearer ' from the token
        token = auth_header.split(' ')[1]

        # decode the token
        data = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        return jsonify({'status': 'valid'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 401


@app.route("/api/crops/", methods=["GET"])
def crop_select():
    crop_name = request.args.get("crop")
    response = {}
    response["market"] = mode

    if crop_name == "corn" or crop_name == "wheat":
        response["market"] = "down"
    else:
        response["market"] = "up"

    print("market = ", mode)
    print(type(response["market"]))
    if crop_name == "corn":
        response[
            "dashboardID"] = "https://public.tableau.com/views/Historicalanalysiscornprice/Sheet1?debug=false&:language=en-US&:display_count=y&:origin=viz_share_link"
        response["newsArticles"] = corn_top_news_list
        # response["market"] = 0
    elif crop_name == "wheat":
        response[
            "dashboardID"] = "https://public.tableau.com/views/HistoricAnalysisofWheat/Sheet1?:language=en-US&:display_count=n&:origin=viz_share_link"
        response["newsArticles"] = wheat_top_news_list
        # response["market"] = 0
    elif crop_name == "oats":
        response[
            "dashboardID"] = "https://public.tableau.com/views/OatHistoricalAnalysis/Sheet1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"
        response["newsArticles"] = oats_top_news_list
        # response["market"] = 1
    elif crop_name == "sorghum":
        response[
            "dashboardID"] = "https://public.tableau.com/views/HistoricalAnalysisofSoybeanprice/Sheet1?:language=en-US&:display_count=n&:origin=viz_share_link"
        response["newsArticles"] = sorghum_top_news_list
        # response["market"] = 1
    else:
        response[
            "dashboardID"] = "https://public.tableau.com/views/Historicalanalysiscornprice/Sheet1?:language=en-US&:display_count=y&:origin=viz_share_link"
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
    return mode


if __name__ == "__main__":
    mode = load_modell()

    corn_df = pd.read_pickle("models/corn.pickle")
    wheat_df = pd.read_pickle("models/wheat.pickle")
    sorghum_df = pd.read_pickle('models/sorghum.pickle')
    oat_df = pd.read_pickle('models/oat.pickle')

    corn_top_news_list = corn_df.to_dict("records")
    wheat_top_news_list = wheat_df.to_dict("records")
    sorghum_top_news_list = sorghum_df.to_dict("records")
    oats_top_news_list = oat_df.to_dict("records")

    update_times()

    app.secret_key = "ejk"
    app.run(host="0.0.0.0", port=8080, debug=True)
