import pytest
import win32com.client as win32
import logging
from pathlib import Path
import tempfile
from random import randint
import shutil
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

    return pd.DataFrame(data)

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

    def _fill_temp_folder_with_xl_files(self, file_type: str, file_count: int, sheet_count: int = 2):
        '''
        Creates and saves x amount of {file_type} files.
        Currently accepts '.csv' and '.xlsx' file type
        
        args: 
            file_type: the type of file to be saved (accepts '.csv' or '.xlsx')
            file_count: number of files to be saved in temp dir
            sheet_count: if xlsx, the number of worksheets per workbook
        '''
        temp_paths = [self.temp_dir / f'temp_{i}{file_type}' for i in range(file_count)]
        assert len(temp_paths) == 3

        if file_type == '.xlsx':
            self._generate_xlsx_files(temp_paths, sheet_count)

        if file_type == '.csv':
            raise NotImplementedError("CSV generation not yet implemented.")

    def _generate_xlsx_files(self, temp_paths: list, sheet_count: int = 2, 
                             col_count: int= 2, row_count: int= 3):
        '''
        generates and saves data in provided [temp_paths].
        args:
            temp_paths: list of paths to save data to
            sheet_count: number of sheets each file should have
            col_count: number of columns sheet will have
            row_count: number of rows each column will have
        returns:
            None
        '''
        if sheet_count > 1:
            for path in temp_paths:
                with pd.ExcelWriter(path) as writer:
                    for j in range(sheet_count):
                        df = self._generate_temp_df(col_count, row_count)
                        df.to_excel(writer, sheet_name=f'sheet{j}', index=False)
        elif sheet_count == 1:    
            for path in temp_paths:
                df = self._generate_temp_df()
                df.to_excel(path, index=False)
        else:
            raise ValueError(f"invalid sheet count: {sheet_count}")

    @staticmethod
    def _generate_temp_df(col_count: int, row_count: int) -> pd.DataFrame:
        '''
        generate a dataframe with specified col and row count.
        Data filling rows are random integers only
        args: 
            col_count: number of columns to populate dataframe with
            row_count: number of rows to populate dataframe with
        return:
            pandas dataframe
        '''
        return pd.DataFrame(
            {
                f'col_ {c}': 
                [randint(0,9) for r in range(row_count)]
                for c in range(col_count)
            }
        )