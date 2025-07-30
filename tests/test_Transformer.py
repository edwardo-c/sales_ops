from data_toolkit.transformer.transformer import Transformer
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

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

def test_Transformer_group_by():
    '''
    expected result
        group 1: 'abc': [123, 456]
        group 2: 'def: [789, 101]
    '''
    data = example_data()
    result = Transformer.split_by_groups(data, 'acct_num')
    assert len(result) == 2

    