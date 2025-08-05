import pandas as pd
import numpy as np
import datetime

MAP_VIOLATION = {
    "keep_columns": ['SKU', 'Product', 'URL', 'MAP', 'Price', 'Seller', 'PDF']
}

# ACU is short for acumatica
PLAN_DIRECT_SALES_ACU = {
    "keep_columns": [
        'Account No.', 
        'Inventory CD', 
        'Category', 
        'Qty', 
        'Amount', 
        'Invoice Date'],
    
    "rename_columns": {
        'Account No.': 'acct_num', 
        'Inventory CD': 'part_number',
        'Category': 'product_category',
        'Qty': 'qty',
        'Amount': 'amount',
        'Invoice Date': 'invoice_date'},
    
    "data_types" : {
        'acct_num': str,
        'part_number': str,
        'product_category': str,
        'qty': float,
        'amount': float,
        'invoice_date': 'datetime64[ns]'
    }
}


'''
order of plan execution:  
    rename columns of individual frames, 
    inner join to filter data (performance boost if done here),  
    concat if concat (truthy) else execult plan per frame, 
    effect entire data frame:
    fill empty: fill column (k) with value in (v)
    extract_month: extract the month number from column (v)
    extract_year: extract the month number from column (v)
'''
STATUS_REPORT_PLAN = {
    2025: {'rename_columns': '', 'join': 'inner'},
    2024: {'rename_columns': '', 'join': 'inner'},
    'concat':{
        'fill_empty': {'part_number': 'category'},
        'extract_month': 'invoice_date',
        'extract_year': 'invoice_date',
    }
}