import pandas as pd
import logging

def extract_data(titles_csv_path, colors_csv_path, youtube_csv_path):
    try:
        # Extract titles data
        logging.info(f'Reading titles data from {titles_csv_path}')
        titles_df = pd.read_csv(titles_csv_path)
        logging.debug(f'Titles DataFrame columns: {titles_df.columns.tolist()}')

        # Extract colors data
        logging.info(f'Reading colors data from {colors_csv_path}')
        colors_df = pd.read_csv(colors_csv_path)
        logging.debug(f'Colors DataFrame columns: {colors_df.columns.tolist()}')

        # Extract youtube data
        logging.info(f'Reading youtube data from {youtube_csv_path}')
        youtube_df = pd.read_csv(youtube_csv_path)
        logging.debug(f'YouTube DataFrame columns: {youtube_df.columns.tolist()}')

        return titles_df, colors_df, youtube_df
    except Exception as e:
        logging.error(f'Error occurred while extracting data: {e}')
        raise
