import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URI

def extract_titles(file_path='data/titles.csv'):
    return pd.read_csv(file_path)

def extract_colors(file_path='data/colors.csv'):
    return pd.read_csv(file_path)

def extract_youtube(file_path='data/youtube.csv'):
    return pd.read_csv(file_path)

def transform_episodes(titles_df, youtube_df):
    episodes_df = youtube_df[['painting_title', 'season', 'episode', 'youtube_src', 'img_src']].merge(
        titles_df[['title', 'month', 'day', 'year']], 
        left_on='painting_title', 
        right_on='title', 
        how='left'
    )
    episodes_df = episodes_df.dropna(subset=['year', 'month', 'day'])
    episodes_df['year'] = episodes_df['year'].astype(int).astype(str)
    episodes_df['day'] = episodes_df['day'].astype(int).astype(str).str.zfill(2)
    episodes_df['month'] = episodes_df['month'].astype(str)
    episodes_df['broadcast_date'] = pd.to_datetime(episodes_df[['year', 'month', 'day']].agg('-'.join, axis=1), format='%Y-%m-%d', errors='coerce')
    episodes_df.rename(columns={
        'painting_title': 'title',
        'episode': 'episode_number',
        'img_src': 'image_url',
        'youtube_src': 'youtube_src',
        'season': 'season'
    }, inplace=True)
    episodes_df = episodes_df[['title', 'season', 'episode_number', 'broadcast_date', 'youtube_src', 'image_url']]
    return episodes_df

def transform_colors(youtube_df):
    colors_df = youtube_df[['colors', 'color_hex']].drop_duplicates()
    colors_df = colors_df.set_index('color_hex')['colors'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).reset_index()
    colors_df.rename(columns={'colors': 'color_name'}, inplace=True)
    colors_df.reset_index(drop=True, inplace=True)
    colors_df.index += 1
    colors_df.reset_index(inplace=True)
    colors_df.rename(columns={'index': 'id'}, inplace=True)
    return colors_df

def transform_subjects(colors_df):
    subjects_df = colors_df.melt(var_name='subject_name', value_name='exists').drop('exists', axis=1).drop_duplicates()
    subjects_df.reset_index(drop=True, inplace=True)
    subjects_df.index += 1
    subjects_df.reset_index(inplace=True)
    subjects_df.rename(columns={'index': 'id'}, inplace=True)
    return subjects_df

def load_data(df, table_name):
    engine = create_engine(DATABASE_URI)
    print(f"Connecting to database using {DATABASE_URI}")
    with engine.connect() as connection:
        print(f"Connection established, loading data into {table_name} table")
        df.to_sql(table_name, con=connection, if_exists='append', index=False)
        print(f"Data loaded into {table_name} table")

def main():
    titles_df = extract_titles()
    youtube_df = extract_youtube()
    colors_df = extract_colors()

    episodes_df = transform_episodes(titles_df, youtube_df)
    print("Episodes DataFrame:")
    print(episodes_df.head())
    load_data(episodes_df, 'Episodes')

    colors_transformed_df = transform_colors(youtube_df)
    print("Colors DataFrame:")
    print(colors_transformed_df.head())
    load_data(colors_transformed_df, 'Colors')

    subjects_transformed_df = transform_subjects(colors_df)
    print("Subjects DataFrame:")
    print(subjects_transformed_df.head())
    load_data(subjects_transformed_df, 'Subjects')

if __name__ == "__main__":
    main()
