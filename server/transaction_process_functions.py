import numpy as np
import pandas as pd
import datetime as dt

def getFrequencies(tab, start_day, end_day, freq='daily'):
    """returns dictionary of frequencies of price (eg $/time specified)"""
    date_range = [i for i in pd.date_range(start_day, end_day).values if i in tab.index.values]
    out = create_categories_map(tab)
    if (len(date_range)==0):
        return out
    transaction_range = tab.loc[[i for i in pd.date_range(start_day, end_day).values if i in tab.index.values]]
    out_val = transaction_range.groupby('Category')['Amount'].sum().to_dict()
    if (freq == 'weekly'):
        r = (end_day - start_day).days/7
    elif (freq=='monthly'):
        r = (end_day - start_day).days/30
    elif (freq=='yearly'):
        r = (end_day - start_day).days/365
    else:
        r = (end_day - start_day).days
    for k in out_val:
        out_val[k] = out_val[k]/r
        out[k] = out_val[k]
    return out

def getFrequenciesCounts(tab, start_day, end_day, freq='daily'):
    """returns dictionary of frequencies of occurrences (eg num_purchases/time specified)"""
    date_range = [i for i in pd.date_range(start_day, end_day).values if i in tab.index.values]
    out = create_categories_map(tab)
    if (len(date_range)==0):
        return out
    transaction_range = tab.loc[[i for i in pd.date_range(start_day, end_day).values if i in tab.index.values]]
    out_val = transaction_range['Category'].value_counts().to_dict()
    if (freq == 'weekly'):
        r = (end_day - start_day).days/7
    elif (freq=='monthly'):
        r = (end_day - start_day).days/30
    elif (freq=='yearly'):
        r = (end_day - start_day).days/365
    else:
        r = (end_day - start_day).days
    for k in out_val:
        out_val[k] = out_val[k]/r
        out[k] = out_val[k]
    return out

def getRangeExpenditure(tab, date_start, date_end, category=None):
    '''returns the amount of money spent in date range'''
    date_range = [i for i in pd.date_range(date_start, date_end).values if i in tab.index.values]
    if (len(date_range)==0):
        return 0
    today_transactions = tab.loc[date_range]
    today_transactions.head()
    if (category==None):
        return sum(today_transactions['Amount'])
    else:
        return sum(today_transactions[today_transactions['Category']==category]['Amount'])

def getTodayExpenditure(tab, today=dt.datetime.today()):
    '''gets amount of money spent today or the specified date'''
    if (today not in tab.index):
        return 0
    today_transactions = tab.loc[today.date()]
    return sum(today_transactions['Amount'])

def process_raw(tab):
    if (type(tab)==str):
        df = pd.read_csv(str)
    else:
        df = tab
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index(df['Date']).drop('Date',axis=1)
    return df

def create_categories_map(tab, label='Category'):
    cat_set = set(tab[label])
    out = dict()
    for c in cat_set:
        out[c] = 0
    return out
