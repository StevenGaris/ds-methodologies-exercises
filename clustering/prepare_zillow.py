import pandas as pd
import acquire_zillow


def find_single_unit_properties():
    df = acquire_zillow.get_zillow_full()
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


faux_num = ['id', 'parcelid', 'transactiondate', 'bathroomcnt', 'bedroomcnt', 
            'buildingqualitytypeid', 'decktypeid', 'fips', 'fireplacecnt', 
            'fullbathcnt', 'garagecarcnt', 'hashottuborspa', 'latitude', 'longitude', 
            'poolcnt', 'poolsizesum', 'pooltypeid10', 'pooltypeid2', 'pooltypeid7', 
            'propertycountylandusecode', 'propertyzoningdesc', 'rawcensustractandblock', 'regionidcity', 
            'regionidcounty', 'regionidneighborhood', 'regionidzip', 'roomcnt', 'threequarterbathnbr', 
            'unitcnt', 'yardbuildingsqft17', 'yearbuilt', 'numberofstories', 
            'fireplaceflag', 'assessmentyear', 
            'taxdelinquencyflag', 'taxdelinquencyyear', 
            'censustractandblock', 'airconditioningdesc', 'architecturalstyledesc', 'buildingclassdesc', 
            'heatingorsystemdesc', 'propertylandusedesc', 'storydesc', 'typeconstructiondesc']


def numeric_to_categorical(df: pd.DataFrame, cols: tuple) -> pd.DataFrame:
    to_coerce = {col: "category" for col in cols}
    return df.astype(to_coerce)


def prep_zill():
    df = acquire_zillow.get_zillow_full()
    df = find_single_unit_properties()
    df = numeric_to_categorical(df, faux_num)
    return df


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
