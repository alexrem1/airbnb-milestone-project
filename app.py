import os
from flask import Flask, render_template, redirect, request, url_for, session

app = Flask(__name__)

@app.route("/")
@app.route("/choose_us")
def choose_us():
     return render_template("chooseus.html")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)