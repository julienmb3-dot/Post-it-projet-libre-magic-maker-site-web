from flask import Flask, render_template, request, session, redirect, url_for
import pymongo

import datetime


client = pymongo.MongoClient("mongodb+srv://b:7AoQ4qDkgmsywcBs@cluster0.0s76g90.mongodb.net/?appName=Cluster0")
db = client["SitePostIt"]

app = Flask(__name__)

app.secret_key = "akndjbwkdgaboqudbkoa"

@app.route("/")
def index():
    data = list(db["PostIt"].find())
    return render_template("index.html", annonces=data)

@app.route("/search", methods = ["GET"])
def search():
    query = request.args.get("q" , "").strip()

    if query == "":
        results = list(db["PostIt"].find({}))
        return render_template("search_result.html", annonces = results, query = query)
    else:
        results = list(db["PostIt"].find({
            "$or": [
                {"date": {"$regex" : query, "$options" : "i"}},
                {"content": {"$regex" : query, "$options" : "i"}},
                {"auteur": {"$regex" : query, "$options" : "i"}},
                {"color": {"$regex" : query, "$options" : "i"}}
            ]
        }))
        return render_template("search_result.html", annonces = results, query = query)
    
@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        db_users = db["Users"]
        user = db_users.find_one({"user_id" : request.form["user_id"]})
        if user:
            if request.form["password"] == user["password"]:
                session["user"] = request.form["user_id"]
                return redirect(url_for("index"))
            else:
                return render_template('login.html', erreur="mot de passe incorrect")
        else:
            return render_template('login.html', erreur="utilisateur incorrect")
    else:
        return render_template('login.html')

@app.route("/sigin", methods = ["POST", "GET"])
def sigin():
    if request.method == "POST":
        db_users = db["Users"]
        new_user = db_users.find_one({"user_id" : request.form["user_id"]})
        if new_user:
            return render_template('sigin.html', erreur="Ce nom d'utilisateur est déjà pris.")
        else:
            if request.form["password"] == request.form["password_validation"]:
                if not(request.form["password"] == "" or request.form["user_id"] == ""):
                    db_users.insert_one({
                        "user_id" : request.form["user_id"],
                        "password" : request.form["password"]
                    })
                    session["user"] = request.form["user_id"]
                    return redirect(url_for("index"))
                else:
                    return render_template('sigin.html', erreur="Le nom d'utilisateur ou le mot de passe est vide.")
            else:
                return render_template('sigin.html', erreur="Les deux mots de passe ne correspondent pas.")
    else:
        return render_template("sigin.html")
    
@app.route("/publish", methods = ["POST", "GET"])
def publish():
    if "user" not in session:
        return redirect(url_for("login.html"))

    if request.method == "POST":
        db_postIt = db["PostIt"]
        content = request.form["content"]
        auteur = session["user"]
        date = datetime.datetime.now()
        date = date.strftime("%x")
        
        if request.form["color"] == "yellow":
            color = "yellow"
        elif request.form["color"] == "red":
            color = "red"
        elif request.form["color"] == "blue":
            color = "blue"
        elif request.form["color"] == "green":
            color = "green"
        else:
            color = "yellow"
        
        if content:
            db_postIt.insert_one({
                "content" : content,
                "auteur" : auteur,
                "color" : color,
                "date" : date
            })
            return redirect(url_for("index"))
        else:
            return render_template('publish.html', erreur="Le titre ou le contenu est vide")
    else:
        return render_template("publish.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__  == "__main__":
    app.run(host="0.0.0.0", port=82)
