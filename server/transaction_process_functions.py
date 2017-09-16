import numpy as np
import pandas as pd
import datetime as dt

def getFrequencies(tab, start_day, end_day, freq='daily'):
    """returns dictionary of frequencies of price (eg $/time specified)"""
    date_range = [i for i in pd.date_range(start_day, end_day).values if i in tab.index.values]
    out = create_categories_map(tab)
    if (len(date_range)==0):
        return out
    transaction_range = tab.loc[date_range]
    out_val = transaction_range.groupby('Category')['Amount'].sum().to_dict()
    diff_days = (end_day - start_day).days
    if (diff_days==0):
        diff_days = 1

    if (freq == 'weekly'):
        r = diff_days/7
    elif (freq=='monthly'):
        r = diff_days/30
    elif (freq=='yearly'):
        r = diff_days/365
    else:
        r = diff_days
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
    transaction_range = tab.loc[date_range]
    out_val = transaction_range['Category'].value_counts().to_dict()
    diff_days = (end_day - start_day).days
    if (diff_days==0):
        diff_days = 1

    if (freq == 'weekly'):
        r = diff_days/7
    elif (freq=='monthly'):
        r = diff_days/30
    elif (freq=='yearly'):
        r = diff_days/365
    else:
        r = diff_days
    for k in out_val:
        out_val[k] = out_val[k]/r
        out[k] = out_val[k]
    return out

def full_category_frequencies(tab, freq='Daily'):
    """returns the frequency of entire table"""
    return getFrequencies(tab, min(tab.index), max(tab.index), freq)

def full_category_frequencies_counts(tab, freq='Daily'):
    """returns the frequency counts of entire table"""
    return getFrequenciesCounts(tab, min(tab.index), max(tab.index), freq)

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

def getFrequencyDate(time, freq='daily'):
    """returns the start and end dates based on the given frequency
    possible freq = 'daily', 'weekly', 'monthly', 'yearly' """
    if (freq=='weekly'):
        start = time - dt.timedelta(days=time.weekday())
        end = start + dt.timedelta(days=6)
    elif (freq=='monthly'):
        start = time.replace(day=1)
        start_day, end_day = calendar.monthrange(time.year,time.month)
        end = time.replace(day=end_day)
    elif (freq=='yearly'):
        start = time.replace(month=1).replace(day=1)
        end = time.replace(month=12).replace(day=31)
    else:
        start = time
        end = time
    return start, end

def savings_since(tab, start_day, end_day, freq='weekly'):
    past_freq = getFrequencies(tab, min(tab.index), start_day-dt.timedelta(days=1), 'weekly')
    current_freq = getFrequencies(tab, start_day, end_day, 'weekly')
    #interesting_categories = set(['Alcohol and Bars','Clothing','Coffee Shops','Fast Food','Food',''])
    diff = past_freq
    for cat in past_freq:
        diff[cat] = current_freq[cat]-past_freq[cat]
    return diff

def get_frequent_categories(tab, threshold=0.5):
    """returns a dict of categories and frequencies for categories that have a frequency over 0.5"""
    cats = full_category_frequencies_counts(tab, 'weekly')
    out = dict()
    for cat in cats:
        if (cats[cat] > threshold):
            out[cat] = cats[cat]
    return out

def sum_dict(d):
    '''returns the sum of a dictionary (key=anything, value=addable)'''
    s=0
    for c in d:
        s+=d[c]
    return s
