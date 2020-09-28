import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
       import env

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = mongo.db.recipes.find()
    recipeList = list(recipes)
    print(mongo.db)
    print('This view works')
    for recipe in recipeList:

        print(recipe)
    return render_template("recipes.html", recipes=recipeList)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db['email-addresses'].find_one({"email": request.form.get("email").lower()})
    
        if existing_user:
            flash("email already registered")
            return redirect(url_for("register"))

        register = {
            "name": request.form.get("name").lower(),
            "email": request.form.get("email").lower()
        }
        print(register)
        mongo.db.users.insert_one(register)

        #put new user into 'session' cookie
        session["email"] = request.form.get("email").lower()
        flash("Registration successful")
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
