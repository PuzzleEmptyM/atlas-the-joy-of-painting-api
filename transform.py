import pandas as pd

def transform_data(titles_path, colors_path, youtube_path):
    # Read the data
    titles_df = pd.read_csv(titles_path)
    colors_df = pd.read_csv(colors_path)
    youtube_df = pd.read_csv(youtube_path)

    # Rename columns for consistency
    youtube_df = youtube_df.rename(columns={
        'season': 'season',
        'episode': 'episode_number'
    })

    # Merge the titles and youtube dataframes on title
    episodes_df = pd.merge(titles_df, youtube_df, left_on='title', right_on='painting_title')

    # Extract only the necessary columns
    episodes_df = episodes_df[[
        'title', 'month', 'day', 'year', 'img_src', 'youtube_src', 'season', 'episode_number', 'num_colors'
    ]]

    # Rename columns for consistency
    episodes_df = episodes_df.rename(columns={
        'title': 'episode_title',
        'month': 'broadcast_month',
        'day': 'broadcast_day',
        'year': 'broadcast_year'
    })

    # Convert broadcast date columns to a single broadcast_date column
    episodes_df['broadcast_date'] = pd.to_datetime(
        episodes_df[['broadcast_year', 'broadcast_month', 'broadcast_day']].astype(str).agg('-'.join, axis=1),
        errors='coerce'
    )

    # Drop the original broadcast date columns
    episodes_df = episodes_df.drop(columns=['broadcast_year', 'broadcast_month', 'broadcast_day'])

    # Transform the colors data
    unique_colors = pd.melt(colors_df, id_vars=['EPISODE', 'TITLE'], var_name='color_name', value_name='present')
    unique_colors = unique_colors[unique_colors['present'] == 1].drop(columns=['present'])

    # Merge with episodes_df to get episode_id
    unique_colors = pd.merge(unique_colors, youtube_df[['num', 'painting_title']], left_on='TITLE', right_on='painting_title')
    unique_colors = unique_colors.rename(columns={'num': 'episode_id'})

    # Map color names to IDs
    color_names = pd.DataFrame(unique_colors['color_name'].unique(), columns=['color_name'])
    color_names['color_id'] = color_names.index + 1

    mapped_unique_colors = pd.merge(unique_colors, color_names, on='color_name')

    # Create episode_colors DataFrame
    episode_colors = mapped_unique_colors[['episode_id', 'color_id']]

    # Transform the subjects data
    subjects = colors_df.columns[2:]
    unique_subjects = pd.melt(colors_df, id_vars=['EPISODE', 'TITLE'], var_name='subject_name', value_name='present')
    unique_subjects = unique_subjects[unique_subjects['present'] == 1].drop(columns=['present'])

    # Merge with episodes_df to get episode_id
    unique_subjects = pd.merge(unique_subjects, youtube_df[['num', 'painting_title']], left_on='TITLE', right_on='painting_title')
    unique_subjects = unique_subjects.rename(columns={'num': 'episode_id'})

    # Map subject names to IDs
    subject_names = pd.DataFrame(unique_subjects['subject_name'].unique(), columns=['subject_name'])
    subject_names['subject_id'] = subject_names.index + 1

    mapped_unique_subjects = pd.merge(unique_subjects, subject_names, on='subject_name')

    # Create episode_subjects DataFrame
    episode_subjects = mapped_unique_subjects[['episode_id', 'subject_id']]

    return episodes_df, color_names, episode_colors, subject_names, episode_subjects
