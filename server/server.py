from flask import Flask, url_for, request, redirect, json, jsonify
import pandas as pd
import datetime as dt

from transaction_process_functions import *


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def root():
    return "Hello World"

@app.route("/spending-date", methods=['POST'])
def spending_today():
    date_string = request.values.get("ds")
    print(date_string)
    # TODO: Query CSV for total spending for today
    frame = pd.read_csv('transactions.csv')
    frame = process_raw(frame)
    spending = getTodayExpenditure(frame,today=pd.to_datetime(date_string))
    return json.dumps(spending)

@app.route('/set-goal', methods=['POST'])
def set_goal():
    print(request.values.get("goal"))
    # TODO: Save goal value in storage (csv)
    frame = pd.read_csv('goals.csv')
    frame['goal'][0] = request.values.get('goal')
    frame['progress'][0] = 0
    frame.to_csv('goals.csv', index=False)

    return str(request.values.get("goal"))

@app.route('/get-prog-goal', methods=['GET'])
def get_progress():
    frame = pd.read_csv('goals.csv')
    resp = {'goal': int(frame['goal'][0]), 'progress': int(frame['progress'][0])}
    return json.dumps(resp)

@app.route('/get-routines', methods=['GET'])
def get_routines():
    """Returns JSON list of routines. User will select these and modify."""
    frame = pd.read_csv('routines.csv')
    routine_list = []
    for index, row in frame.iterrows():
        routine_list.append((row['name'], float(row['freq']), int(row['value'])))

    return json.dumps(routine_list)



if __name__ == "__main__":
    app.run(debug=True)
