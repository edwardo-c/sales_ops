import pandas as pd
import numpy as np

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
        'invoice_date': np.datetime64
    }
}