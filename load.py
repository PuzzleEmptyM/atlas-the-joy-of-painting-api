from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
import logging
import config
import re

def extract_season_episode(episode_str):
    match = re.match(r'S(\d+)E(\d+)', episode_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def load_data(episodes_df, color_names, episode_colors, subject_names, episode_subjects):
    try:
        logging.info('Loading data into the database')
        engine = create_engine(config.DATABASE_CONNECTION_STRING)
        metadata = MetaData()
        metadata.reflect(engine)
        
        episodes_table = metadata.tables['Episodes']
        colors_table = metadata.tables['Colors']
        episode_colors_table = metadata.tables['Episodes_Colors']
        subjects_table = metadata.tables['Subjects']
        episode_subjects_table = metadata.tables['Episodes_Subjects']

        with engine.connect() as connection:
            for index, row in episodes_df.iterrows():
                try:
                    insert_statement = episodes_table.insert().values(
                        title=row['title'],
                        season=row['season'],
                        episode_number=row['episode'],
                        broadcast_date=row['date'],
                        img_src=row.get('img_src', None),
                        youtube_src=row.get('yt_link', None),
                        num_colors=row.get('num_colors', None)
                    )
                    logging.debug(f'Executing insert statement for Episodes row {index}: {row.to_dict()}')
                    connection.execute(insert_statement)
                except SQLAlchemyError as e:
                    logging.error(f'Error occurred while inserting Episodes row {index}: {row.to_dict()} - {e}')

            for index, row in color_names.iterrows():
                try:
                    insert_statement = colors_table.insert().values(
                        color_id=row['color_id'],
                        color_name=row['color_name'],
                        color_hex=row.get('color_hex', None)
                    )
                    logging.debug(f'Executing insert statement for Colors row {index}: {row.to_dict()}')
                    connection.execute(insert_statement)
                except SQLAlchemyError as e:
                    logging.error(f'Error occurred while inserting Colors row {index}: {row.to_dict()} - {e}')

            for index, row in episode_colors.iterrows():
                try:
                    insert_statement = episode_colors_table.insert().values(
                        episode_id=row['episode_id'],
                        color_id=row['color_id']
                    )
                    logging.debug(f'Executing insert statement for EpisodeColors row {index}: {row.to_dict()}')
                    connection.execute(insert_statement)
                except SQLAlchemyError as e:
                    logging.error(f'Error occurred while inserting EpisodeColors row {index}: {row.to_dict()} - {e}')

            for index, row in subject_names.iterrows():
                try:
                    insert_statement = subjects_table.insert().values(
                        subject_id=row['subject_id'],
                        subject_name=row['subject_name']
                    )
                    logging.debug(f'Executing insert statement for Subjects row {index}: {row.to_dict()}')
                    connection.execute(insert_statement)
                except SQLAlchemyError as e:
                    logging.error(f'Error occurred while inserting Subjects row {index}: {row.to_dict()} - {e}')

            for index, row in episode_subjects.iterrows():
                try:
                    season, episode = extract_season_episode(row['episode_id'])
                    if season is not None and episode is not None:
                        insert_statement = episode_subjects_table.insert().values(
                            episode_id=row['episode_id'],
                            subject_id=row['subject_id']
                        )
                        logging.debug(f'Executing insert statement for EpisodeSubjects row {index}: {row.to_dict()}')
                        connection.execute(insert_statement)
                    else:
                        logging.error(f'Error extracting season and episode from EpisodeSubjects row {index}: {row.to_dict()}')
                except SQLAlchemyError as e:
                    logging.error(f'Error occurred while inserting EpisodeSubjects row {index}: {row.to_dict()} - {e}')

        logging.info('Data loaded successfully')
    except SQLAlchemyError as e:
        logging.error(f'Error occurred while loading data: {e}')
        raise
