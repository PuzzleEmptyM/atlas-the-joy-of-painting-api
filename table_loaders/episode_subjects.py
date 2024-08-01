from extract import extract_colors
from transform import transform_subjects
from load import load_data

def load_episode_subjects():
    colors_df = extract_colors()
    subjects_df = transform_subjects(colors_df)
    episode_subjects = colors_df[['episode_id', 'subject_id']]
    load_data(episode_subjects, 'EpisodeSubjects')
