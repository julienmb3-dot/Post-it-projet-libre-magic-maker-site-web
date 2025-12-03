from flask import Flask, render_template, request, session, redirect, url_for
import pymongo

from datetime import datetime


client = pymongo.MongoClient("mongodb+srv://b:7AoQ4qDkgmsywcBs@cluster0.0s76g90.mongodb.net/?appName=Cluster0")
db = client["SitePostIt"]

app = Flask(__name__)

app.secret_key = "akndjbwkdgaboqudbkoa"

@app.route("/")
def index():
    data = list(db["PostIt"].find())
    return render_template("index.html", annonces=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__  == "__main__":
    app.run(host="0.0.0.0", port=82)
