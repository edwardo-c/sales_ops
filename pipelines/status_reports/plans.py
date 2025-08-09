
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
    'allsales_2024': {
        'rename_columns': '', 
        'join': 'inner'
        },
        
    'allsales_2025': {'rename_columns': '', 'join': 'inner'},
    'concat':{
        'fill_empty': {'part_number': 'category'},
        'extract_month': 'invoice_date',
        'extract_year': 'invoice_date',
    }
}