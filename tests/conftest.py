import pytest
from pandas import DataFrame

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