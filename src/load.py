 # src/load.py
from sqlalchemy import create_engine
import pandas as pd
from config import DB_URL

engine = create_engine(DB_URL)

def load_to_db(data: list, table_name: str):
    df = pd.DataFrame(data)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)