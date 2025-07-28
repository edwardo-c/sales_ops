import pandas as pd
from sqlalchemy import create_engine

class Exporter():
    def __init__(self, df):
        self.df = df

    def export_csv(self, df: pd.DataFrame, export_path):
        df.to_csv(export_path, index=False)

    def to_sql(self, engine_url: str, table_name: str, if_exists: str = "replace"):
        engine = create_engine(engine_url)
        self.df.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,
            index=False
        )
    

