import numpy as np
from colorama import Fore, Style

def EDA(name_df):
    
    print(Fore.CYAN + 'Shape DataFrame:')
    print(Style.RESET_ALL)
    print(name_df.shape, '\n')

    print(Fore.CYAN + 'Basic information:')
    print(Style.RESET_ALL)
    name_df.info()
    print('\n')
    
    print(Fore.CYAN + 'Find the duplicates:')
    print(Style.RESET_ALL)
    print(name_df.duplicated().sum(), '\n')
    
    print(Fore.CYAN + 'Datatypes:')
    print(Style.RESET_ALL)
    print(name_df.dtypes, '\n')
    
    print(Fore.CYAN + 'Number of unique values in each column:')
    print(Style.RESET_ALL)
    for column in name_df.columns:
      print(column, name_df[column].nunique())
    print('\n')

    print(Fore.CYAN + 'Number of null values:')
    print(Style.RESET_ALL)
    print(name_df.isnull().sum(), '\n')

    print(Fore.CYAN + 'Сount, unique, top, freq:')
    print(Style.RESET_ALL)
    print(name_df.isnull().any().describe(), '\n')

    print(Fore.CYAN + 'Categorical data:')
    print(Style.RESET_ALL)
    cat = name_df.select_dtypes(include = object)
    cat_columns = cat.columns
    cat_features = list(cat_columns) 
    print(cat_features, '\n')
    
    print(Fore.CYAN + 'Numerical data:')
    print(Style.RESET_ALL)
    numeric = name_df.select_dtypes(include = np.number)
    numeric_columns= numeric.columns
    numeric_features = list(numeric_columns) 
    print(numeric_features, '\n')