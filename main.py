import logging
from transform import transform_data
from load import load_data

def main():
    logging.basicConfig(level=logging.DEBUG)
    
    titles_path = '/home/puzzle/atlas-the-joy-of-painting-api/data/titles.csv'
    colors_path = '/home/puzzle/atlas-the-joy-of-painting-api/data/subjects.csv'
    youtube_path = '/home/puzzle/atlas-the-joy-of-painting-api/data/colors.csv'
    
    episodes_df, color_names, episode_colors, subject_names, episode_subjects = transform_data(
        titles_path, colors_path, youtube_path
    )
    
    load_data(episodes_df, color_names, episode_colors, subject_names, episode_subjects)

if __name__ == '__main__':
    main()
