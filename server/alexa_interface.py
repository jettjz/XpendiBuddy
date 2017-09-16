import numpy as np
import pandas as pd
import datetime as dt
from transaction_process_functions import *

def get_daily_update(table_str, today=dt.datetime.today()):
    # will give weekly update on Sundays
    tab = pd.read_csv(table_str)
    today = pd.to_datetime("2017-9-16")
    tab = process_raw(tab)
    if (today.weekday()==5):
        return get_weekly_update_helper(tab, today)
    else:
        return get_daily_update_helper(tab, today)


def get_daily_update_helper(tab, today):
    """return JSON of daily update"""
    today_expense = getTodayExpenditure(tab, today)
    full_freq = full_category_frequencies(tab, 'daily')
    start_week, end_week = getFrequencyDate(today, 'weekly')
    week_freq = getFrequencies(tab, start_week, end_week)
    week_expenses = getRangeExpenditure(tab, start_week, end_week)

    so_far_str = "You spent " + str(round(today_expense,2)) + " dollars today and have spent " + str(round(week_expenses,2)) + " dollars so far this week. "

    #useless to calculate frequencies early in week
    if (today.weekday() < 3):
        return so_far_str

    differences = savings_since(tab, start_week, end_week)
    interesting_categories = get_frequent_categories(tab)
    good_saved = dict()
    good_saved_str = ""
    for cat in interesting_categories:
        if (differences[cat] <= -1):
            good_saved[cat] = -differences[cat]
            good_saved_str += "You are on track to save approximately " + str(round(good_saved[cat],2)) + " this week due to savings in " + cat + ". "
    if (len(good_saved)>1):
        good_saved_str += "Overall, we estimate you will save " + str(round(sum_dict(good_saved),2)) + " dollars by the end of the week compared to previous weeks. Great job! "


    high_freq = set()
    for key in week_freq:
        # if you spend over 1.5 the normal amount
        if (week_freq[key] >= full_freq[key]*1.5):
            high_freq.add(key)

    risk_category_str = ""
    if (len(high_freq)==0):
        risk_category_str = "No major expenditures so far this week."
    else:
        risk_category_str = ""
        for risk in high_freq:
            risk_category_str += "You spent significantly more on "+risk+" than previously before. "


    # similar = get_spending_similar(tab, today)
    # interesting_similar = max(similar.keys(), key=(lambda k: similar[k]))
    # # will add line abuot high spending comparing to others spendings
    # if (interesting_similar > 1 && interesting_similar in high_freq):
    #     horz_com = "You are spending " + similar[interesting_similar] + " the amount people normally your age spend on " +interesting_similar)
    # else:
    #     horz_com = ""

    #Goal track/savings


    return so_far_str+good_saved_str+risk_category_str




def get_weekly_update_helper(tab, today):
    pre_str = "It is Saturday! Here is how your week looked. "
    today_expense = getTodayExpenditure(tab, today)
    full_freq = full_category_frequencies(tab, 'daily')
    start_week, end_week = getFrequencyDate(today, 'weekly')
    week_freq = getFrequencies(tab, start_week, end_week)
    week_expenses = getRangeExpenditure(tab, start_week, end_week)

    so_far_str = "You spent " + str(round(today_expense,2)) + " dollars today and spent " + str(round(week_expenses,2)) + " dollars in total this past week. "

    differences = savings_since(tab, start_week, end_week)
    interesting_categories = get_frequent_categories(tab)
    good_saved = dict()
    good_saved_str = "You saved money this week in the following categories: "
    for cat in interesting_categories:
        if (differences[cat] <= -1):
            good_saved[cat] = -differences[cat]
            # good_saved_str += "You are on track to save approximately " + str(round(good_saved[cat],2)) + " this week due to savings in " + cat + ". "
            good_saved_str += cat + " "
    if (len(good_saved)>1):
        good_saved_str += ". You saved around " + str(round(sum_dict(good_saved),2)) + " dollars this week compared to previous weeks. Great job! "

    high_freq = set()
    for key in week_freq:
        # if you spend over 1.5 the normal amount
        if (week_freq[key] >= full_freq[key]*1.5):
            high_freq.add(key)

    risk_category_str = ""
    if (len(high_freq)==0):
        risk_category_str = "You had no extraordinary expenditure trends this week!"
    else:
        risk_category_str = "You spent significantly more on in the following categories: "
        for risk in high_freq:
            risk_category_str += risk + " "

    income = pd.read_csv("Data for Income.csv")
    income = income.set_index(income['Catergories']).drop('Catergories', axis = 1)
    age = pd.read_csv("Data for age under 25.csv")
    age = age.set_index(age['Categories']).drop('Categories', axis = 1)
    KeySets = ['less than 5000', '5000-9999', '10000-14999', '15000-19999', '20000-29999', '30000-39999', '40000-49999', '50000-69999']

    result0 = comparison(week_freq['Food'], income, 'Food', 'wk', KeySets)
    # result01 = comparison(week_freq['Transportation'], income, 'Transportation', 'wk', KeySets)
    result1 = comparison_age(week_freq['Food'], age, 'Food', '$/wk/person')
    # result11 = comparison_age(week_freqp['Transportation', age, 'Transportation', 'wk'])
    compare_line = ""
    if result1 < 0:
        compare_line = "You spent " + str(round(np.absolute(result1),2)) + " per week less than people of your similar age on food. And your spent on food is similar to people with income " + str(result0)
    else:
        compare_line = "You spent " + str(round(np.absolute(result1),2)) + " per week more than people of your similar age on food. And your spent on food is similar to people with income " + str(result0)
    return pre_str + so_far_str+good_saved_str+risk_category_str+compare_line
