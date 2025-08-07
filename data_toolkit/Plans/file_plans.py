## --- plans specifically passed to pd.read_excel. sensative file paths exist in untracked config --- ##

STATUS_REPORT_SALES_2025 = {
    'alias': 'allsales_2025',
    'sheet_name': "2025",
    'row': 10,
    'usecols': [
        'Customer Account Number', 'Inventory CD', 'Classification(Sales Category)', 
        'Qty', 'Amount', 'Invoice Date'
        ],
    'dtype': {
        'Customer Account Number': 'string', 
        'Inventory CD': 'string',
        'Classification(Sales Category)': 'string', 
        'Qty': 'float64', 
        'Amount': 'float64',
        'Invoice Date': 'datetime[ns]'
    },
}

STATUS_REPORT_SALES_2024 = {
    'alias': 'allsales_2024',
    'sheet_name': "2024",
    'row': 1,
    'usecols': [
        'Account No.', 'Inventory CD', 'Category', 
        'Qty', 'Amount', 'Invoice Date'
        ],
    'dtype': {
        'Account No.':'string', 'Inventory CD': 'string', 'Category': 'string', 
        'Qty': 'float64', 'Amount': 'float64', 'Invoice Date': 'datetime[ns]',   
    },
}