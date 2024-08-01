import pandas as pd

def transform_episodes(titles_df, youtube_df):
    # Merge DataFrames on the painting title
    episodes_df = youtube_df[['painting_title', 'season', 'episode', 'youtube_src', 'img_src']].merge(
        titles_df[['title', 'month', 'day', 'year']], 
        left_on='painting_title', 
        right_on='title', 
        how='left'
    )
    
    # Convert month to string and map to numerical values
    episodes_df['month'] = episodes_df['month'].str.strip().str.capitalize()
    month_map = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    episodes_df['month'] = episodes_df['month'].map(month_map)
    
    # Handle missing values
    episodes_df['day'] = episodes_df['day'].fillna(1).astype(int).astype(str).str.zfill(2)
    episodes_df['year'] = episodes_df['year'].fillna(1900).astype(int).astype(str)
    episodes_df['month'] = episodes_df['month'].fillna('01')
    
    # Combine year, month, and day into a single date column
    episodes_df['broadcast_date'] = pd.to_datetime(episodes_df[['year', 'month', 'day']].agg('-'.join, axis=1), format='%Y-%m-%d', errors='coerce')

    # Rename columns to match the database schema
    episodes_df.rename(columns={
        'painting_title': 'title',
        'episode': 'episode_number',
        'img_src': 'image_url',
        'youtube_src': 'youtube_src',
        'season': 'season'
    }, inplace=True)
    
    # Select the required columns
    episodes_df = episodes_df[['title', 'season', 'episode_number', 'broadcast_date', 'youtube_src', 'image_url']]
    
    print("Episodes DataFrame:")
    print(episodes_df.head())
    
    return episodes_df

def transform_colors(youtube_df):
    colors_df = youtube_df[['colors', 'color_hex']].drop_duplicates()
    colors_df = colors_df.set_index('color_hex')['colors'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).reset_index()
    colors_df.rename(columns={'colors': 'color_name'}, inplace=True)
    colors_df.reset_index(drop=True, inplace=True)
    colors_df.index += 1
    colors_df.reset_index(inplace=True)
    colors_df.rename(columns={'index': 'id'}, inplace=True)
    
    print("Colors DataFrame:")
    print(colors_df.head())
    
    return colors_df

def transform_subjects(colors_df):
    subjects_df = colors_df.melt(var_name='subject_name', value_name='exists').drop('exists', axis=1).drop_duplicates()
    subjects_df.reset_index(drop=True, inplace=True)
    subjects_df.index += 1
    subjects_df.reset_index(inplace=True)
    subjects_df.rename(columns={'index': 'id'}, inplace=True)
    
    print("Subjects DataFrame:")
    print(subjects_df.head())
    
    return subjects_df
