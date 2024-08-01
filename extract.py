import pandas as pd

def extract_titles(file_path='data/titles.csv'):
    return pd.read_csv(file_path)

def extract_colors(file_path='data/colors.csv'):
    return pd.read_csv(file_path)

def extract_youtube(file_path='data/youtube.csv'):
    return pd.read_csv(file_path)
