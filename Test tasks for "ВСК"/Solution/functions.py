import numpy as np

def EDA(name_df):
    
    print('Shape DataFrame:')
    print(name_df.shape,'\n')

    print('Basic information:')
    name_df.info()
    
    print('Find the duplicates:')
    print(name_df.duplicated().sum(),'\n')
    
    print('Datatypes:')
    print(name_df.dtypes,'\n')
    
    print('Number of unique values in each column:')
    for column in name_df.columns:
      print(column, name_df[column].nunique())
    
    print('Number of null values:')
    print(name_df.isnull().sum(),'\n')

    print('Сount, unique, top, freq:')
    print(name_df.isnull().any().describe(),'\n')

    print('Categorical data:')
    cat = name_df.select_dtypes(include = object)
    cat_columns = cat.columns
    cat_features = list(cat_columns) 
    print(cat_features,'\n')

    for feature in cat_features:
      print('The feature is {} and number of categories are {}'.format(feature,\
      len(name_df[feature].unique())))
    
    print('Numerical data:')
    numeric = name_df.select_dtypes(include = np.number)
    numeric_columns= numeric.columns
    numeric_features = list(numeric_columns) 
    print(numeric_features,'\n')

    for feature in numeric_features:
      print('The feature is {} and number of categories are {}'.format(feature,\
      len(name_df[feature].unique())))
    print()

    for feature in numeric_features: 
      print("The counts of the catagorical values in the '{}' feature:\n".format(feature.title()))
      print(name_df[feature].value_counts().sort_index(),'\n')