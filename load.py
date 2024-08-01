import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URI

def load_data(df, table_name):
    engine = create_engine(DATABASE_URI)
    with engine.connect() as connection:
        df.to_sql(table_name, con=connection, if_exists='append', index=False)
        connection.close()
