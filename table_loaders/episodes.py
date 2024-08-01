import pandas as pd
from extract import extract_titles, extract_youtube
from transform import transform_episodes
from load import load_data

def load_episodes():
    titles_df = extract_titles()
    youtube_df = extract_youtube()
    episodes_df = transform_episodes(titles_df, youtube_df)
    load_data(episodes_df, 'Episodes')
