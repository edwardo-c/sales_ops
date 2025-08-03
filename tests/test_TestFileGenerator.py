import pytest
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def test_file_creation(init_gen):
    '''
    test and inspect csv creation and data
    #pytest --log-cli-level=INFO .\tests\test_TestFileGenerator.py
    '''
    assert init_gen.temp_dir is not None
    assert init_gen.temp_dir.exists()
    
    file_type = '.xlsx'
    file_count = 3

    init_gen._fill_temp_folder_with_xl_files(
        file_type, 
        file_count=file_count, 
        sheet_count=1
    )

    temp_files = list(init_gen.temp_dir.glob(f'*{file_type}'))
    assert len(temp_files) == file_count
   
    # file type switching needed
    if file_type == '.xlsx':
        df = pd.concat([pd.read_excel(file) for file in temp_files]) 
    elif file_type == '.csv':
        df = pd.concat([pd.read_csv(file) for file in temp_files])

    assert len(list(df.columns)) == 2
    assert len(df) == 9