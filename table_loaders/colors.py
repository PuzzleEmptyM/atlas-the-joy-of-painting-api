from extract import extract_youtube
from transform import transform_colors
from load import load_data

def load_colors():
    youtube_df = extract_youtube()
    colors_df = transform_colors(youtube_df)
    load_data(colors_df, 'Colors')
