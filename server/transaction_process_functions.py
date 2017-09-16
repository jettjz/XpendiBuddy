import numpy as np
import pandas as pd
import datetime as dt

def getFrequencies(tab, start_day, end_day, freq='daily'):
    transaction_range = tab.loc[[i for i in pd.date_range(start_day, end_day).values if i in tab.index.values]]
    out = df.groupby('Category')['Amount'].sum().to_dict()
    if (freq == 'weekly'):
        r = (end_day - start_day).days/7
    elif (freq=='monthly'):
        r = (end_day - start_day).days/30
    elif (freq=='yearly'):
        r = (end_day - start_day).days/365
    else:
        r = (end_day - start_day).days
    for k in out:
        out[k] = out[k]/r
    return out

def getRangeExpenditure(tab, date_start, date_end, category=None):
    '''returns the amount of money spent in date range'''
    today_transactions = tab.loc[[i for i in pd.date_range(date_start, date_end).values if i in tab.index.values]]
    today_transactions.head()
    if (category==None):
        return sum(today_transactions['Amount'])
    else:
        return sum(today_transactions[today_transactions['Category']==category]['Amount'])

def getTodayExpenditure(tab, today=dt.datetime.today()):
    '''gets amount of money spent today'''
    today_transactions = tab.loc[today.date()]
    return sum(today_transactions['Amount'])
