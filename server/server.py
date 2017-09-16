from flask import Flask, url_for, request, redirect, json, jsonify
import pandas as pd
import datetime as dt

from transaction_process_functions import *

from alexa_interface import get_daily_update

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

@app.route('/flash-breifing', methods=['GET'])
def get_flash_breifing():
    """ returns a JSON object that encodes the user's flash briefing """
    m = get_daily_update("transactions.csv")

    # TODO add non-hard coded date here
    d = '2017-09-16T00:00:00.00-000'
    t = 'Expendi Buddy Flash briefing'
    u = 'urn:uuid:testaroo'
    json_response =  jsonify(
        uid=u,
        updateDate=d,
        titleText=t,
        mainText=m
    )


    response = app.response_class(
        response=json_response,
        status=200,
        mimetype='application/json',
        headers = Headers({ Content-Type:'application/json'})
    )

    return response
    #print(response)
    #return response
    #response_w_header = Flask.Response(json_reponse)
    #response_w_header.headers['Content-Type'] = 'application/json'
    #return response_w_header

def populate_routines(date_start, date_end):
    """find routines, purge and rewrite the routines csv. only called on a new week. rolls on a thirty-day window."""
    ROUTINE_THRESH = 0.5

    frame = pd.read_csv('transactions.csv')
    frame = process_raw(frame)
    freqs = getFrequenciesCounts(frame, date_start, date_end,freq='weekly')
    values = getFrequencies(frame, date_start, date_end,freq='weekly')

    routines = []

    for k in freqs:
        if freqs[k] > ROUTINE_THRESH:
            routines.append((k, freqs[k], values[k]))

    routines.sort(key=lambda x: -x[1])

    routine_frames = pd.DataFrame(routines)
    routine_frames.columns = ['name', 'freq', 'value']

    routine_frames.to_csv('routines.csv', index=False)

@app.route('/activate-suggestions', methods=['POST'])
def activate_suggestions():
    """Activates suggestions by pushing them to the active suggestions csv.
    Expects JSON in following format:

    List of 3-tuples (name, freq, savings)

    Savings should be calculated on the Alexa side. If r = normal routine freq,
    and n = user-chosen reduced freq, savings = value * (1 - n/r)
    """
    suggestions = request.values.get('suggestions')
    print(suggestions)
    suggestions = eval(suggestions)
    print(suggestions)

    suggestion_frames = pd.DataFrame(suggestions)
    suggestion_frames.columns = ['name', 'freq', 'savings']

    suggestion_frames.to_csv('active_suggestions.csv', index=False)

    return "success"

@app.route('/weekly-update', methods=['POST'])
def weekly():
    date_string = request.values.get('ds')
    date_end = pd.to_datetime(date_string)
    date_start = date_end - pd.Timedelta(30, 'D') # 30 day window
    print(date_start, date_end)
    populate_routines(date_start, date_end)
    return 'WEEKLY'

@app.route('/daily-update', methods=['POST'])
def daily():
    """ makes a call to the daily update method from alexa_interface.py, but does
    not return a full flash briefing object -> only a string """
    # How much you spent yesterday
    # Progress on goal routines
    # How much you will save if you fulfill the active routine
    # does not specify any extra params to get daily updates
    m = get_daily_update("")

    return jsonify(message=m)



if __name__ == "__main__":
    app.run(debug=True)
