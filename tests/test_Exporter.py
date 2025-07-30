from config.paths import CSV_DST_DIR
from data_toolkit.exporter.exporter import Exporter
from data_toolkit.transformer.transformer import Transformer
import pytest
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def test_Exporter_groups(example_data):
    grouped = Transformer.split_by_groups(example_data, 'acct_num')
    
    # fill temp dir and return path to temp dir
    filled_temp_dir = Exporter.groups_to_csvs(grouped, CSV_DST_DIR)

    # test count of files in temp_dir
    assert len(list(filled_temp_dir.glob('**/*csv'))) == 2

    # move files to final folder
    final_name = 'final_name'
    dst_dir = Exporter.move_temp_dir_to_network(filled_temp_dir, CSV_DST_DIR, final_name=final_name)

    # test return folder was named properly
    expected_path = Path(CSV_DST_DIR) / final_name
    assert dst_dir == expected_path

    # test two files exist in temp folder
    assert len(list(dst_dir.glob('**/*csv'))) == 2