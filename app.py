import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/choose_us")
def choose_us():
     return "It's working"

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)