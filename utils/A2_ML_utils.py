import pandas as pd
import joblib

# Function to determine if a column is categorical
def is_categorical(series, threshold=10):
    return series.dtype.name == 'category' or series.nunique() < threshold

def export_model(model, filename='model.pkl'):
    joblib.dump(model, filename)