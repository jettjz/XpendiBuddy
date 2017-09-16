import json

from flask import Flask, url_for, request, redirect


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def root():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)
