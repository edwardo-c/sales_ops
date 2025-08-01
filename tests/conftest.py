import pytest
from pandas import DataFrame
import win32com.client as win32
import logging
from pathlib import Path
import tempfile
from random import randint
import pandas as pd
import shutil

logging.basicConfig(level=logging.INFO)

@pytest.fixture
def example_data():
    data = {
        'acct_num': [
            'abc',
            'abc',
            'def',
            'def',
            ],
        'part_number': [
            123,
            456,
            789,
            101
        ]
    }

    return DataFrame(data)


@pytest.fixture
def init_gen():
    with TestFileGenerator() as gen:
        yield gen

class TestFileGenerator():
    def __init__(self, excel: bool= True, temp_dir: bool= True):
        self.excel = win32.gencache.EnsureDispatch('Excel.Application') if excel else None
        self.temp_dir = Path(tempfile.mkdtemp()) if temp_dir else None

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.excel:
            self.excel.Quit()

        if self.temp_dir:
            shutil.rmtree(self.temp_dir)

    def _fill_temp_folder_with_csvs(self, csv_count: int):
        '''
        Creates and saves x amount of csvs
        csv_count: number of csvs to be saved in temp dir
        '''
        for i in range(csv_count):
            temp_path = self.temp_dir / f'temp_{i}.csv'
            df = self._generate_temp_df()
            df.to_csv(temp_path, index=False)

    @staticmethod
    def _generate_temp_df(col_count: int= 2, row_count: int= 3) -> pd.DataFrame:
        return pd.DataFrame(
            {
                f'col_ {c}': 
                [randint(0,9) for r in range(row_count)]
                for c in range(col_count)
            }
        )