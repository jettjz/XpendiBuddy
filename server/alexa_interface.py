import numpy as np
import datetime as dt
import transaction_process_functions

def get_daily_update(table_str, today):
    # will give weekly update on Sundays
    tab = pd.read_csv('transactions.csv')
    tab = process_raw(tab)
    if (today.weekday()==0):
        return get_weekly_update_helper(tab, today)
    else:
        return get_daily_update_helper(tab, today)


def get_daily_update_helper(tab, today):
    """return JSON of daily update"""
    today_expense = getTodayExpenditure(tab, today)
    full_freq = full_category_frequencies(tab, 'daily')
    week_freq = getFrequencies(tab, start_week, today)
    start_week, end_week = getFrequencyDate(today)
    week_expenses = getRangeExpenditure(tab, start_week, end_week)

    high_freq = set()
    for key in week_freq:
        # if you spend over 1.5 the normal amount
        if (week_freq[key] >= full_freq_daily[key]*1.5):
            high_freq.add(key)

    if (len(high_freq)==0):
        risk_category = "No major expenditures so far this week."
    else:
        for risk in high_freq:
            spent =


def get_weekly_update_helper(tab, today):
