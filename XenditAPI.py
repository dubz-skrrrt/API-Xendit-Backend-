import os

from flask import Flask, request, render_template
from xendit import Xendit, XenditError

app = Flask(__name__)

@app.route("/")
def index():
    return{}
if __name__ == "__main__":
    app.run(debug=True)

xendit_instance = Xendit(api_key=os.getenv("xnd_development_P4qDfOss0OCpl8RtKrROHjaQYNCk9dN5lSfk+R1l9Wbe+rSiCwZ3jw=="))
