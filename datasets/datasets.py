"""
These functions servs to load properly the datasets included in the project.
They return the loaded dataframe (with some basic preprocessing, if needed),
the name of the class column and the ideal number of bins for discretizating the
numerical attributes (if any, else None).
"""
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

DATA_FOLDER = 'datasets/real'
cat_types = ['object','str','category']

def preprocess(df, cl, min_bins=10):
    """
    Function that preprocess a pandas dataframe so that the resulting dataset 
    is made only by numerical data that correspond to discrete categories.
    Args:
        data: the data to preprocess
        cl: the column name of the class
    Returns:
        X: numpy preprocessed data
        y: numpy preprocessed target
        encoders: dicitonary with the label_encoders associated to the encoded attributes
    """ 
    columns = df.columns
    columns_no_class = np.delete(columns, np.where(columns==cl)) 
    encoders = {}
    for c in columns:     
        if df[c].dtype.name in cat_types: # Check if is not a numerical column
            le = LabelEncoder() # Encode the values
            df[c] = le.fit_transform(df[c])
            if c == cl:
                encoders['cl'] = le
            else:
                encoders[c] = le          
    X = df[columns_no_class].values
    y = df[cl].values
    return X, y, columns_no_class, encoders

def load_adult_stretch():
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'adult-stretch.csv'))
    return df, 'class', None

def load_crx():
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'crx.csv'), header=None)
    # Drop the rows that contain missing values
    df = df.replace('?',np.NaN)
    df = df.dropna(axis=0)
    # Convert object columns to float
    df[1] = df[1].astype(float)
    df[13] = df[13].astype(float)
    return df, 15, 6

def load_hillvalley():
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'hill_valley.csv'))
    return df, 'class', 6

def load_banknote():
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'banknote.csv'), header=None)
    return df, 4, 6

def load_pendigits():
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'pendigits.csv'))
    return df, 'class', 5

def load_nursery():
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'nursery.csv'))
    return df, 'class', None

def load_custom():
    """
    Function to load a custom dataset by the user. The attribute name
    of the class is asked. 
    """
    again =True
    while(again):
        path = input("Path to the csv file:\n")
        if os.path.isfile(path):
            try:
                df = pd.read_csv(path)
                again = False
            except:
                print("Impossible to read the file")
        else:
            print("File doesn't exist")

    again =True
    while(again):
        cl = input("Define the column name of the class (or the index):\n")
        if cl in df.columns:
            again = False
        elif cl.isdigit() and int(cl) >= 0 and int(cl) < df.columns.size:
            cl = df.columns[int(cl)]
            again = False
        else:
            print("Class not found")
    return df, cl, 10


def load(i):
    datasets = {1:load_crx,2:load_banknote,3:load_pendigits,4:load_nursery,5:load_custom}
    df, cl, bins = datasets[i]()
    X, y, columns_no_class, encoders = preprocess(df, cl, bins)
    return X, y
