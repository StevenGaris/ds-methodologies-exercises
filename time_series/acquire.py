import pandas as pd
import numpy as np
from datetime import datetime
import itertools

# JSON API
import requests
import json

# data visualization
import matplotlib
import seaborn as sns
import statsmodels.api as sm

# ignore warnings
import warnings
warnings.filterwarnings("ignore")



def get_stores():
    base_url = 'https://python.zach.lol'
    
    response = requests.get('https://python.zach.lol/api/v1/stores')
    data = response.json()
    
    stores = pd.DataFrame(data['payload']['stores'])

#     response = requests.get(base_url + data['payload']['next_page'])
#     data = response.json()

#     while data['payload']['page'] <= data['payload']['max_page']:
        
#         stores = pd.concat([stores, pd.DataFrame(data['payload']['stores'])]).reset_index(drop=True)
 
#         if data['payload']['page'] == data['payload']['max_page']:
#             break  

#         response = requests.get(base_url + data['payload']['next_page'])
#         data = response.json()
        
    return stores

def get_items():
    base_url = 'https://python.zach.lol'
    
    response = requests.get('https://python.zach.lol/api/v1/items')
    data = response.json()
    
    items = pd.DataFrame(data['payload']['items'])

    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()

    while data['payload']['page'] <= data['payload']['max_page']:
        
        items = pd.concat([items, pd.DataFrame(data['payload']['items'])]).reset_index(drop=True)
 
        if data['payload']['page'] == data['payload']['max_page']:
            break  

        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        
    return items

def get_sales():
    base_url = 'https://python.zach.lol'
    
    response = requests.get('https://python.zach.lol/api/v1/sales')
    data = response.json()
    
    sales = pd.DataFrame(data['payload']['sales'])

    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()

    while data['payload']['page'] <= data['payload']['max_page']:
        
        sales = pd.concat([sales, pd.DataFrame(data['payload']['sales'])]).reset_index(drop=True)
 
        if data['payload']['page'] == data['payload']['max_page']:
            break  

        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()

    sales.rename(columns={'store': 'store_id'}, inplace=True)
    sales.rename(columns={'item': 'item_id'}, inplace=True)

    return sales


def get_full_df():
    stores = get_stores()
    items = get_items()
    sales = get_sales()
    df = sales.merge(stores)
    df = df.merge(items)
    return df


def get_full_df_csv():
    stores = pd.read_csv('stores.csv')
    items = pd.read_csv('items.csv')
    sales = pd.read_csv('sales.csv')

    sales.rename(columns={'store': 'store_id'}, inplace=True)
    sales.rename(columns={'item': 'item_id'}, inplace=True)

    df = sales.merge(stores)
    df = df.merge(items)
    return df