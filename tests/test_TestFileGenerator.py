import pytest
import pandas as pd

def test_csv_creation(init_gen):
    '''
    test and inspect csv creation and data
    '''
    init_gen._fill_temp_folder_with_csvs(3)
    
    temp_files = list(init_gen.temp_dir.glob('*csv'))

    df = pd.concat([pd.read_csv(csv) for csv in temp_files])

    assert len(temp_files) == 3
    assert len(list(df.columns)) == 2
    assert len(df) == 9

    # pytest .\tests\test_TestFileGenerator.py