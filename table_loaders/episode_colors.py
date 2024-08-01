from extract import extract_youtube
from transform import transform_colors
from load import load_data

def load_episode_colors():
    youtube_df = extract_youtube()
    colors_df = transform_colors(youtube_df)
    episode_colors = youtube_df[['painting_title', 'season', 'episode']].merge(colors_df, left_on='colors', right_on='color_name')
    episode_colors.rename(columns={
        'painting_title': 'title',
        'episode': 'episode_number'
    }, inplace=True)
    load_data(episode_colors, 'EpisodeColors')
