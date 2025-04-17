from dbCode import *
from flask import Flask, render_template
import pymysql
import creds
from dbCode import *

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route("/")
def index():
    countries = get_list_of_dictionaries()
    return render_template("index.html", results=countries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


@app.route("/add-travel", methods=["POST"])
def add_travel():
    username = request.form["username"]
    destination = request.form["destination"]
    date_of_trip = request.form["date_of_trip"]
    add_travel_history(username, destination, date_of_trip)
    flash("Travel entry added successfully!", "success")
    return redirect(url_for("dashboard"))

@app.route("/get-travel-history/<username>")
def get_travel_history_route(username):
    travel_history = get_travel_history(username)
    return render_template("travel_history.html", travel_history=travel_history)