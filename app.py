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
            "email": request.form.get("email").lower(),

        }
        print(register)
        mongo.db.users.insert_one(register)

        #put new user into 'session' cookie
        session["email"] = request.form.get("email").lower()
        flash("Registration successful")
    return render_template("register.html")


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        task = {
            "photo": request.form.get("photo"),
            "title": request.form.get("title"),
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "meal_time": request.form.get("meal_time"),
            "diet_type": request.form.get("diet_type"),
            "ingredients": request.form.get("ingredients"),
            "preparation": request.form.get("preparation")

        }
        mongo.db.recipes.insert_one(task)
        flash("Recipe Successfully Added")
        return redirect(url_for("get_recipes"))
        return render_template("add_recipe.html")

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_recipe.html", recipe=recipe, categories=categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
