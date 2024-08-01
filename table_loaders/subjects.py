from extract import extract_colors
from transform import transform_subjects
from load import load_data

def load_subjects():
    colors_df = extract_colors()
    subjects_df = transform_subjects(colors_df)
    load_data(subjects_df, 'Subjects')
