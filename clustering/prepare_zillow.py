import pandas as pd
import acquire_zillow
from sklearn.linear_model import LinearRegression


def find_single_unit_properties(df):
    # Only grabbing things that have a unit count of 1
    single_unit = df.loc[df['unitcnt'] == 1].dropna(subset=['calculatedfinishedsquarefeet'])
    # Only grabbing SFR and Condos. Others seem like multi-unit that were mislabeled.
    single_unit = single_unit.loc[(single_unit['propertylandusedesc'] == 'Single Family Residential') | (single_unit['propertylandusedesc'] == 'Condominium')]
    # Dropping those without a bedroom. Don't want studio appts.
    single_unit = single_unit.drop(single_unit[single_unit.bedroomcnt == 0].index)
    # Dropping those without a bathroom, need at least 1.
    single_unit = single_unit.drop(single_unit[single_unit.bathroomcnt == 0].index)
    # Dropping under 800 sqft. CA law min req. 
    single_unit = single_unit.loc[single_unit['calculatedfinishedsquarefeet'] >= 800]
    return single_unit


faux_num = ['bathroomcnt', 
            'bedroomcnt', 
            'latitude', 
            'longitude', 
            'regionidzip', 
            'yearbuilt']


def numeric_to_categorical(df: pd.DataFrame, cols: tuple) -> pd.DataFrame:
    to_coerce = {col: 'int' for col in cols}
    return df.astype(to_coerce)


# def prep_zill():
#     df = acquire_zillow.get_zillow_full()
#     df = find_single_unit_properties()
#     df = numeric_to_categorical(df, faux_num)
#     return df


def column_missing(df):
    missing_count = df.isnull().sum()
    missing_percent = df.isnull().sum()/df.shape[0]*100
    missing_count = pd.DataFrame(missing_count)
    missing_percent = pd.DataFrame(missing_percent)
    missing_count = missing_count.rename(columns={0: 'na_count'})
    missing_percent = missing_percent.rename(columns={0: 'na_percent'})
    column_na = missing_count.join(missing_percent)
    column_na['na_percent'] = column_na['na_percent'].round(2)
    return column_na


def row_missing(df):
    missing_count = df.isnull().sum(axis=1)
    missing_percent = df.isnull().sum(axis=1)/df.shape[1]*100
    missing_count = pd.DataFrame(missing_count)
    missing_percent = pd.DataFrame(missing_percent)
    missing_count = missing_count.rename(columns={0: 'na_count'})
    missing_percent = missing_percent.rename(columns={0: 'na_percent'})
    row_na = pd.concat([missing_count, missing_percent], axis=1)
    row_na['na_percent'] = row_na['na_percent'].round(2)
    return row_na


list_to_fill = ['poolcnt']

def fill_na_with_0(df, list_to_fill):
    for col in list_to_fill:
        df[col].fillna(0, inplace=True)
    return df

def impute_landsqft(df):
    good_land = df.loc[~df.lotsizesquarefeet.isna()]
    lm1 = LinearRegression()
    lm1.fit(good_land[['landtaxvaluedollarcnt']], good_land[['lotsizesquarefeet']])
    y_pred_lm1 = lm1.predict(df.loc[df.lotsizesquarefeet.isna(), ['landtaxvaluedollarcnt']])
    df.loc[df.lotsizesquarefeet.isna(), ['lotsizesquarefeet']] = y_pred_lm1
    return df


def drop_null_percent_column(df):
    pct_null = df.isnull().sum() / len(df)
    missing_features = pct_null[pct_null > 0.40].index
    df.drop(missing_features, axis=1, inplace=True)
    return df


def zillow_csv():
    df = pd.read_csv('zillow.csv')
    return df


def zillow_ready_to_explore(df):
    return df.pipe(find_single_unit_properties)\
             .pipe(impute_landsqft)\
             .pipe(drop_null_percent_column)