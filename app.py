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
    """Decorator to force user authentication before view function is accessed.
    Args:
    fn: Decorated flask view function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        username = session.get("username", None)
        if not username:
            return redirect(url_for("aut"))

        user = mongo.db.user.find({"username": username})
        if not user:
            return redirect(url_for("aut"))

        return fn(*args, **kwargs)

    return wrapper


@app.route("/")
@app.route("/index")
def index():
    """
    landing page.
    """
    return render_template("index.html")


@app.route("/get_property")
def get_property():
    """
    reading property listings from database
    """
    return render_template("properties.html", property=mongo.db.property.find())


@app.route("/aut")
def aut():
    """
    If the user is in session redirect to get_property route
    """
    if "username" in session:
        return redirect(url_for("get_property"))

    return render_template("aut.html")


@app.route("/login", methods=["POST"])
def login():
    """
    I'm looking for a user (where the name = name submitted via registration) so I can compare passwords
    """
    users = mongo.db.user
    login_user = users.find_one({"username": request.form["username"]})

    if login_user:
        """
            I'm comparing the password the user entered and the existing password in the database
            """
        if (
            bcrypt.hashpw(request.form["pass"].encode("utf-8"), login_user["password"])
            == login_user["password"]
        ):
            """
                if it exists, I can add the user to the session
                """
        session["username"] = request.form["username"]
        return redirect(url_for("get_property"))
    return render_template("aut.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    """if it is a post, I want to determine if the username they're requesting already exists in the database
    """
    if request.method == "POST":
        users = mongo.db.user
        existing_user = users.find_one({"username": request.form["username"]})
        if existing_user is None:
            """and if it doesn't, they'll be allowed to register
            """
            hashpass = bcrypt.hashpw(
                request.form["pass"].encode("utf-8"), bcrypt.gensalt()
            )
            users.insert({"username": request.form["username"], "password": hashpass})
            session["username"] = request.form["username"]
            return redirect(url_for("aut"))
        return render_template("register.html")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("index"))


@app.route("/add_listing")
@login_required
def add_listing():
    """logic for users to add listing
    """
    return render_template(
        "addlisting.html",
        amenities=mongo.db.amenities.find(),
        bedsize=mongo.db.bedsize.find(),
        property=mongo.db.property.find(),
    )


@app.route("/insert_listing", methods=["POST", "GET"])
@login_required
def insert_listing():
    """logic for users, when inserting listing, to be associated with the listing
    """

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
            "user": user["_id"],
        }
    )
    return redirect(url_for("user_listing"))


@app.route("/view_listing/<property_id>")
def view_listing(property_id):
    """logic for viewing a property listing as well as reading reviews
"""
    one_property = mongo.db.property.find({"_id": ObjectId(property_id)})
    reviews = mongo.db.reviews.find({"property": ObjectId(property_id)})
    one_user = mongo.db.reviews.find()
    return render_template(
        "viewlisting.html", property=one_property, reviews=reviews, user=one_user
    )


@app.route("/insert_review/<property_id>", methods=["POST"])
def insert_review(property_id):
    """logic for inserted review to be associated with property
"""
    one_property = mongo.db.property.find({"_id": ObjectId(property_id)})
    reviews = mongo.db.reviews
    review = request.form.to_dict()
    review["property"] = ObjectId(property_id)
    reviews.insert_one(review)
    return redirect(url_for("view_listing", property_id=property_id))


@app.route("/edit_listing/<property_id>")
@login_required
def edit_listing(property_id):
    """functionality for editing property listings
"""
    the_property = mongo.db.property.find_one({"_id": ObjectId(property_id)})
    return render_template(
        "editlisting.html",
        property=the_property,
        amenities=mongo.db.amenities.find(),
        bedsize=mongo.db.bedsize.find(),
    )


@app.route("/update_listing/<property_id>", methods=["POST"])
@login_required
def update_listing(property_id):
    """logic for users, when updating listing, to still be associated with the listing
"""

    username = session["username"]
    user = mongo.db.user.find_one({"username": username})

    property = mongo.db.property
    property.update(
        {"_id": ObjectId(property_id)},
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
            "author": request.form.get("author"),
            "datevisited": request.form.get("datevisited"),
            "things": request.form.get("things"),
            "user": user["_id"],
        },
    )
    return redirect(url_for("user_listing"))


@app.route("/delete_listing/<property_id>")
@login_required
def delete_listing(property_id):
    """delete a listing functionality
"""
    mongo.db.property.remove({"_id": ObjectId(property_id)})
    return redirect(url_for("user_listing"))


@app.route("/user_listing/")
@login_required
def user_listing():
    """logic for user-specific property listings
"""
    username = session["username"]
    user = mongo.db.user.find_one({"username": username})
    return render_template(
        "userlisting.html", property=mongo.db.property.find({"user": user["_id"]})
    )


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=False)
