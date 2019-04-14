import pandas as pd
from sklearn.preprocessing import LabelEncoder
import acquire_mall


def get_upper_outliers(s, k):
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    return s.apply(lambda x: max([x - upper_bound, 0]))

def add_upper_outlier_columns(df, k):
    for col in df.select_dtypes('number'):
        df[col + '_outliers'] = get_upper_outliers(df[col], k)
    return df


def encode_objects(df):
    le = LabelEncoder()
    le.fit(df.age)
    df['age_encoded'] = le.transform(df.age)
    return df


def mall_prepared(df):
    df = acquire_mall.get_mall_customers_data()
    df = add_upper_outlier_columns(df, 1.5)
    df = encode_objects(df)
    return df


def peekatdata(df):
    print('- Shape')
    print(df.shape)
    print('- Head and Tail')
    print(pd.concat([df.head(), df.tail()]))
    print('- Numeric Vars')
    print(df.describe())
    print('- String Columns')
    for col in df.select_dtypes('object'):
        print('--- {}'.format(col))
        print(df[col].value_counts().head())