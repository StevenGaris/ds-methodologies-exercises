import pandas as pd
from datetime import timedelta, datetime
import numpy as np
from scipy import stats

import itertools

# data visualization 
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import statsmodels.api as sm

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

import acquire



def chage_datetime(df):
    df['sale_date'] = df.sale_date.str.replace(' 00:00:00 GMT', '')
    df['sale_date'] = df.sale_date.str[5:]
    df['sale_date'] = df.sale_date.str.replace(' ', '/')
    df['sale_date'] = pd.to_datetime(df['sale_date'], format='%d/%b/%Y')
    return df
    

def to_UTC(df):
    df = df.tz_localize('utc')
    return df


def expand_dt(df):
    df['time'] = df.index
    df['year'] = df.time.dt.year
    df['quarter'] = df.time.dt.quarter
    df['month'] = df.time.dt.month
    df['day_of_month'] = df.time.dt.day
    df['day_of_week'] = df.time.dt.dayofweek
    df['weekend'] = ((pd.DatetimeIndex(df.index).dayofweek) // 5 == 1).astype(float)
    df.drop(columns=['time'], inplace=True)
    return df


def set_dt_index(df):
    df.set_index('sale_date', inplace=True)
    return df


def prep_store():
    df = acquire.get_full_df_csv()
    df = chage_datetime(df)
    df = set_dt_index(df)
    df = to_UTC(df)
    df = expand_dt(df)
    return df
