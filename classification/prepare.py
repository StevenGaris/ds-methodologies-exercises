from sklearn import preprocessing


def prep_iris(df_iris):
   df_iris.drop(['species_id', 'measurement_id'], axis=1, inplace=True)
   df_iris.rename(columns={'species_name': 'species'}, inplace=True)
   le = preprocessing.LabelEncoder()
   le.fit(df_iris['species'])
   df_iris['species_encoded'] = le.transform(df_iris['species'])
   return df_iris


def prep_titanic(df_titanic):
   df_titanic.embark_town.fillna('Other', inplace=True)
   df_titanic.embarked.fillna('O', inplace=True)
   df_titanic.drop(columns='deck', inplace=True)
   le_titanic = preprocessing.LabelEncoder()
   le_titanic.fit(df_titanic['embarked'])
   df_titanic['embarked'] = le_titanic.transform(df_titanic['embarked'])
   train, test = train_test_split(df_titanic, train_size=.7)
   mm_scaler = preprocessing.MinMaxScaler()
   mm_scaler.fit(train[['age', 'fare']])
   train[['age', 'fare']] = mm_scaler.transform(train[['age', 'fare']])
   test[['age', 'fare']] = mm_scaler.transform(test[['age', 'fare']])
   return df, train, test