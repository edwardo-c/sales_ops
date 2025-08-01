from data_toolkit.loaders.base_loader import BaseLoader
from pathlib import Path
import shutil
import tempfile
from pandas import DataFrame
import logging
import random

logging.basicConfig(level=logging.INFO)

def _generate_test_csvs(col_count: int = 2, row_count: int = 3):
    return DataFrame(
        {
            f"col_{c}": 
            [random.randint(0,9) for _ in range(row_count)] 
            for c in range(col_count)
        }
    )

def test_folder_to_temp_files():
    for _ in range(2):
        ...

def test_single_dataframe_dir_reader():
    
    # create the temp dir to house files
    temp_dir = Path(tempfile.mkdtemp())
    
    # create temp files
    path_a = temp_dir / 'file_a.csv'
    DataFrame(
        {'col_a': [1,2,3],
         'col_b': [3,4,5]
        }
    ).to_csv(path_a, index=False)

    path_b = temp_dir / 'file_b.csv'
    DataFrame(
        {'col_a': [6,7,8],
         'col_b': [9,10,11]
        }
    ).to_csv(path_b, index=False)

    # convert to single data frame
    result = BaseLoader._single_dataframe_dir_reader('**/*.csv', temp_dir)

    # count rows of single df
    assert len(result) == 6

    # clean up
    shutil.rmtree(temp_dir)

