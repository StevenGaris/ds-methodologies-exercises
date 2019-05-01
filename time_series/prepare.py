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
    dt_format = '%a, %d %b %Y %H:%M:%S %Z'
    df['sale_date'] = pd.to_datetime(df.sale_date, format= dt_format, utc=True)
    return df
    

# Can just add utc=True in to_datetime
def to_UTC(df):
    df = df.tz_localize('utc')
    return df


def expand_dt(df):
    df['time'] = df.index
    df['year'] = df.time.dt.year
    df['quarter'] = df.time.dt.quarter
    df['month'] = df.time.dt.month
    df['day_of_month'] = df.time.dt.day
    df['day_of_week'] = df.time.dt.day_name().str[:3]
    df['is_weekend'] = ((pd.DatetimeIndex(df.index).dayofweek) > 4)
    df.drop(columns=['time'], inplace=True)
    return df


def set_dt_index(df):
    df.set_index('sale_date', inplace=True)
    return df


def prep_store():
    df = acquire.get_full_df_csv()
    df = chage_datetime(df)
    df = set_dt_index(df)
    df = expand_dt(df)
    return df
 