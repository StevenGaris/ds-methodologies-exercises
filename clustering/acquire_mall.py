import pandas as pd
import env

def get_connection(db_name, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db_name}'

def get_mall_customers_data():
    return pd.read_sql('SELECT * FROM customers;', get_connection('mall_customers'))