## --- plans specifically passed to pd.read_excel. sensative file paths exist in untracked config --- ##
from config.paths import (
    CY_LY_ALL_SALES,
    STATUS_REPORT_DIMENSIONS
)

STATUS_REPORT_SALES_2025 = {
        'file': CY_LY_ALL_SALES,
        'file_meta': 
        {
            'alias': 'allsales_2025',
            'sheet_name': "2025",
            'row': 10,
            'usecols': [
                'Customer Account Number', 
                'Inventory CD', 
                'Classification(Sales Category)', 
                'Qty', 
                'Amount', 
                'Invoice Date'
            ],
            'dtype': {
                'Customer Account Number': 'string', 
                'Inventory CD': 'string',
                'Classification(Sales Category)': 'string', 
                'Qty': 'float64', 
                'Amount': 'float64',
            },
        }
    }

STATUS_REPORT_SALES_2024 = {
    'file': CY_LY_ALL_SALES,
    'file_meta': {
        'alias': 'allsales_2024',
        'sheet_name': "2024",
        'row': 1,
        'usecols': [
            'Account No.', 
            'Inventory CD', 
            'Category', 
            'Qty', 
            'Amount', 
            'Invoice Date',
        ], 
        'dtype': {
            'Account No.':'string', 
            'Inventory CD': 'string', 
            'Category': 'string', 
            'Qty': 'float64', 
            'Amount': 'float64',  
        },
    }
}

STATUS_REPORT_BENEFITS = {
    'file': STATUS_REPORT_DIMENSIONS,
    'file_meta': {
        'alias': 'benefits',
        'sheet_name': 'benefits',
        'dtype': {
            'acct_num': 'string',
        	'attribute': 'string',
            'value': 'float'
        }
    },
}

STATUS_REPORT_CUSTOMERS = {
    'file': STATUS_REPORT_DIMENSIONS,
    'file_meta': {
        'alias': 'customers',
        'sheet_name': 'customers',
        'dtype': {
            'acct_num': 'string',
        	'acct_group': 'string',
            'report_type': 'string'
        }
    },
}
