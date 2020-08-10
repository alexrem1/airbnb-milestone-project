import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import bcrypt
from functools import wraps

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "airbnb_revieww"
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET")

mongo = PyMongo(app)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        username = session["username"]
        if not username:
            return redirect(url_for("login"))

        user = mongo.db.user.find({"username": username})
        if not user:
            return redirect(url_for("login"))

        return fn(*args, **kwargs)

    return wrapper

@app.route("/")
@app.route("/choose_us")
def choose_us():
     return render_template("chooseus.html")

@app.route("/get_property")
def get_property():
    return render_template("properties.html", property=mongo.db.property.find())

@app.route("/index")
def index():
    if "username" in session:
        return redirect(url_for("get_property"))

    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    users = mongo.db.user
    login_user = users.find_one({"username": request.form["username"]})

    if login_user:
        if (
            bcrypt.hashpw(request.form["pass"].encode("utf-8"), login_user["password"])
            == login_user["password"]
        ):
            session["username"] = request.form["username"]
            return redirect(url_for("get_property"))
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        users = mongo.db.user
        existing_user = users.find_one({"username": request.form["username"]})
        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form["pass"].encode("utf-8"), bcrypt.gensalt()
            )
            users.insert({"username": request.form["username"], "password": hashpass})
            session["username"] = request.form["username"]
            return redirect(url_for("get_property"))
        return render_template("register.html")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("choose_us"))

@app.route("/add_listing")
@login_required
def add_listing():
    return render_template(
        "addlisting.html",
        amenities=mongo.db.amenities.find(),
        bedsize=mongo.db.bedsize.find(),
        property=mongo.db.property.find()
    )

@app.route("/insert_listing", methods=["POST", "GET"])
@login_required
def insert_listing():

    username = session["username"]
    user = mongo.db.user.find_one({"username": username})

    property = mongo.db.property
    property.insert_one(
        {
            "name": request.form.get("name"),
            "typeandhost": request.form.get("typeandhost"),
            "capacity": request.form.get("capacity"),
            "summary": request.form.get("summary"),
            "pricepernight": request.form.get("pricepernight"),
            "cleaningfee": request.form.get("cleaningfee"),
            "servicefee": request.form.get("servicefee"),
            "bedsize": request.form.getlist("bedsize"),
            "minnights": request.form.get("minnights"),
            "maxnights": request.form.get("maxnights"),
            "rules": request.form.get("rules"),
            "amenities": request.form.getlist("amenities"),
            "cancellation": request.form.get("cancellation"),
            "datevisited": request.form.get("datevisited"),
            "author": request.form.get("author"),
            "things": request.form.get("things"),             
            "user": user["_id"]
        }
    )
    return redirect(url_for("get_property"))


@app.route("/view_listing/<property_id>")
def view_listing(property_id):
    one_property = mongo.db.property.find({"_id": ObjectId(property_id)})
    reviews = mongo.db.reviews.find({"property": ObjectId(property_id)})
    one_user = mongo.db.reviews.find()
    return render_template(
        "viewlisting.html", property=one_property, reviews=reviews, user=one_user
    )

@app.route("/insert_review/<property_id>", methods=["POST"])
def insert_review(property_id):
    one_property = mongo.db.property.find({"_id": ObjectId(property_id)})
    reviews = mongo.db.reviews
    review = request.form.to_dict()
    review["property"] = ObjectId(property_id)
    reviews.insert_one(review)
    return redirect(url_for("view_listing", property_id=property_id))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)