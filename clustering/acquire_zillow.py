import pandas as pd
import env

def get_connection(db_name, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db_name}'


def get_properties_2016_data():
    return pd.read_sql('SELECT properties_2016.id, properties_2016.parcelid, logerror, transactiondate, \
                                basementsqft, bathroomcnt, bedroomcnt, buildingqualitytypeid, \
                                calculatedbathnbr, decktypeid, finishedfloor1squarefeet, calculatedfinishedsquarefeet, \
                                finishedsquarefeet12, finishedsquarefeet13, finishedsquarefeet15, finishedsquarefeet50, \
                                finishedsquarefeet6, fips, fireplacecnt, fullbathcnt, garagecarcnt, garagetotalsqft, \
                                hashottuborspa, latitude, longitude, lotsizesquarefeet, poolcnt, \
                                poolsizesum, pooltypeid10, pooltypeid2, pooltypeid7, propertycountylandusecode, \
                                propertyzoningdesc, rawcensustractandblock, regionidcity, \
                                regionidcounty, regionidneighborhood, regionidzip, roomcnt, threequarterbathnbr, \
                                unitcnt, yardbuildingsqft17, yardbuildingsqft26, yearbuilt, \
                                numberofstories, fireplaceflag, structuretaxvaluedollarcnt, taxvaluedollarcnt, assessmentyear, \
                                landtaxvaluedollarcnt, taxamount, taxdelinquencyflag, taxdelinquencyyear, censustractandblock,\
                                airconditioningdesc, architecturalstyledesc, buildingclassdesc, heatingorsystemdesc,\
                                propertylandusedesc, storydesc, typeconstructiondesc\
                        FROM properties_2016\
                                JOIN predictions_2016 ON properties_2016.parcelid = predictions_2016.parcelid\
                                LEFT JOIN airconditioningtype ON properties_2016.airconditioningtypeid = airconditioningtype.airconditioningtypeid\
                                LEFT JOIN architecturalstyletype ON properties_2016.architecturalstyletypeid = architecturalstyletype.architecturalstyletypeid\
                                LEFT JOIN buildingclasstype ON properties_2016.buildingclasstypeid = buildingclasstype.buildingclasstypeid\
                                LEFT JOIN heatingorsystemtype ON properties_2016.heatingorsystemtypeid = heatingorsystemtype.heatingorsystemtypeid\
                                LEFT JOIN propertylandusetype ON properties_2016.propertylandusetypeid = propertylandusetype.propertylandusetypeid\
                                LEFT JOIN storytype ON properties_2016.storytypeid = storytype.storytypeid\
                                LEFT JOIN typeconstructiontype ON properties_2016.typeconstructiontypeid = typeconstructiontype.typeconstructiontypeid;', get_connection('zillow'))

def get_properties_2017_data():
        return pd.read_sql('SELECT properties_2017.id, properties_2017.parcelid, logerror, transactiondate, \
                                    basementsqft, bathroomcnt, bedroomcnt, buildingqualitytypeid, \
                                    calculatedbathnbr, decktypeid, finishedfloor1squarefeet, calculatedfinishedsquarefeet, \
                                    finishedsquarefeet12, finishedsquarefeet13, finishedsquarefeet15, finishedsquarefeet50, \
                                    finishedsquarefeet6, fips, fireplacecnt, fullbathcnt, garagecarcnt, garagetotalsqft, \
                                    hashottuborspa, latitude, longitude, lotsizesquarefeet, poolcnt, \
                                    poolsizesum, pooltypeid10, pooltypeid2, pooltypeid7, propertycountylandusecode, \
                                    propertyzoningdesc, rawcensustractandblock, regionidcity, \
                                    regionidcounty, regionidneighborhood, regionidzip, roomcnt, threequarterbathnbr, \
                                    unitcnt, yardbuildingsqft17, yardbuildingsqft26, yearbuilt, \
                                    numberofstories, fireplaceflag, structuretaxvaluedollarcnt, taxvaluedollarcnt, assessmentyear, \
                                    landtaxvaluedollarcnt, taxamount, taxdelinquencyflag, taxdelinquencyyear, censustractandblock,\
                                    airconditioningdesc, architecturalstyledesc, buildingclassdesc, heatingorsystemdesc,\
                                    propertylandusedesc, storydesc, typeconstructiondesc\
                                FROM properties_2017\
                                    JOIN predictions_2017 ON properties_2017.parcelid = predictions_2017.parcelid\
                                    LEFT JOIN airconditioningtype ON properties_2017.airconditioningtypeid = airconditioningtype.airconditioningtypeid\
                                    LEFT JOIN architecturalstyletype ON properties_2017.architecturalstyletypeid = architecturalstyletype.architecturalstyletypeid\
                                    LEFT JOIN buildingclasstype ON properties_2017.buildingclasstypeid = buildingclasstype.buildingclasstypeid\
                                    LEFT JOIN heatingorsystemtype ON properties_2017.heatingorsystemtypeid = heatingorsystemtype.heatingorsystemtypeid\
                                    LEFT JOIN propertylandusetype ON properties_2017.propertylandusetypeid = propertylandusetype.propertylandusetypeid\
                                    LEFT JOIN storytype ON properties_2017.storytypeid = storytype.storytypeid\
                                    LEFT JOIN typeconstructiontype ON properties_2017.typeconstructiontypeid = typeconstructiontype.typeconstructiontypeid;', get_connection('zillow'))


def get_zillow_full():
    frames = [get_properties_2016_data(), get_properties_2017_data()]
    full = pd.concat(frames)
    full.dropna(subset=['latitude', 'longitude'], inplace=True)
    full.to_csv('zillow.csv')
    return full






