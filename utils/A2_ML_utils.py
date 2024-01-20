import pandas as pd


# Function to determine if a column is categorical
def is_categorical(series, threshold=10):
    return series.dtype.name == 'category' or series.nunique() < threshold
