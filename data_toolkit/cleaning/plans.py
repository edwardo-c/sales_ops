MAP_VIOLATION_CLEAN = {
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
        'Account No.': 'AcctNum', 
        'Inventory CD': 'part_number',
        'Category': 'product_category',
        'Qty': 'qty',
        'Amount': 'amount',
        'Invoice Date': 'invoice_date'}
}