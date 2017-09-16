from flask import Flask, url_for, request, redirect, json, jsonify


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def root():
    return "Hello World"

@app.route("/spending-today", methods=['GET'])
def spending_today():
    # TODO: Query CSV for total spending for today
    resp = {'text': '200'}
    return json.dumps(resp)

@app.route('/set-goal', methods=['POST'])
def set_goal():
    print(request.values.get("goal"))
    # TODO: Save goal value in storage (csv)

    return str(request.values.get("goal"))

if __name__ == "__main__":
    app.run(debug=True)
