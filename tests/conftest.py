import pytest
from pandas import DataFrame
import win32com as win32
import logging
from pathlib import Path
import tempfile
from random import randint
import pandas as pd

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


class TestDataGenerator():
    def __init__(self, excel: bool= True, temp_dir: bool= True):
        self.excel = win32.gencache.EnsureDispatch('Excel.Application') if excel else None
        self.temp_dir = Path(tempfile.mkdtemp()) if temp_dir else None

    def __enter__(self):
        return self
    
    def __exit__(self):
        if self.excel:
            self.excel.Quit()

    def _fill_temp_folder_with_csvs(self, csv_count):
        for _ in range(csv_count):
            temp_path = self.temp_dir / Path(tempfile.mktemp())
            df = self._generate_temp_df()
            df.to_csv(temp_path)
                        
    @staticmethod
    def _generate_temp_df(col_count: int= 2, row_count: int= 3) -> pd.DataFrame:
        return pd.DataFrame(
            {
                f'col_ {c}': 
                [randint(0,9) for r in range(row_count)]
                for c in range(col_count)
            }
        )
        