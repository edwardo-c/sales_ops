from pathlib import Path
import shutil
import tempfile
from sqlalchemy import create_engine
import pandas as pd

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
    
    @staticmethod
    def groups_to_csvs(data_group: dict, dst_dir: Path):
        '''
        output a data groupping dict(str, pd.dataframe) to csv
        naming each csv the name of the group
        args: 
            data group: the group that will be exported
            dst_dir = (Path) destination folder for exports
        returns:
            Path(temp_dir), directory filled with files
        '''
        temp_dir = Path(tempfile.mkdtemp())

        for acct_num, data in data_group.items():
            temp_export_path = temp_dir / f"{acct_num}.csv"
            data.to_csv(temp_export_path, index=False)

        return temp_dir
    
    @staticmethod
    def move_temp_dir_to_network(src_dir: str, dst_dir: str, final_name= None):
        '''
        moves an entire directory into a different parent directory
        args:
            src_dir: the directory to be moved
            dst_dir: the directory that will hold src_dir
            final_name (optional): used in case user wants to 
            rename the final directory's name
        return: 
            final path to foler containing all moved files
        '''
        if final_name:
            final_path = Path(dst_dir) / final_name
            shutil.move(src_dir, final_path)
            return final_path
        
        shutil.move(src_dir, dst_dir)
        return Path(dst_dir) / Path(src_dir).name
