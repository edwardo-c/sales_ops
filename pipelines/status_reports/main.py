from data_toolkit.plans.file_reader_details import (
    STATUS_REPORT_SALES_2024, 
    STATUS_REPORT_SALES_2025,
    STATUS_REPORT_CUSTOMERS,
    STATUS_REPORT_BENEFITS
)
from data_toolkit.base_loader import BaseLoader
from data_toolkit.dataplan import transforms  # noqa: triggers auto-registration
from data_toolkit.dataplan.registry import GLOBAL_REGISTRY, build_registry
from data_toolkit.dataplan.executor import DataPlanExecutor
import logging

logging.basicConfig(level=logging.WARNING)
project_registry = build_registry(
    include=['rename_columns']
)

def main():
    base_loader = BaseLoader(
        STATUS_REPORT_SALES_2024, 
        STATUS_REPORT_SALES_2025, 
        STATUS_REPORT_CUSTOMERS, 
        STATUS_REPORT_BENEFITS
        )
    
    data = base_loader.data

    plans = {
        "allsales_2025": [
            {
                "op": "rename_columns", 
                "args": {
                    "Customer Account Number": "acct_num", 
                    "Inventory CD": "part_number",
                    "Qty": "qty",
                    "Amount": "amount",
                    "Invoice Date": "invoice_date",
                    "Classification(Sales Category)": "product_category",
                }
            },
        ],
        "allsales_2024": [
            {
                "op": "rename_columns", 
                "args": {
                    "Account No.": "acct_num",
                    "Inventory CD": "part_number",
                    "Qty": "qty",
                    "Amount": "amount",
                    "Invoice_Date": "invoice_date",
                    "Category": "product_category",
                }
            },
        ]
    }

    executor = DataPlanExecutor(data, plans, registry=project_registry, strict=False)
    processed = executor.processed_data

    # --- used only for inspection, workflow --- #
    for alias, df in processed.items():
        print(f"\nDataframe head for {alias}:")
        try:
            print(df.head())
        except Exception as e:
            raise ValueError(f"Expected a DataFrame for alias '{alias}', got {type(df)}") from e

if __name__ == '__main__':
    main()

# paste to run during temp: python -m pipelines.status_reports.main



'''
order of plan execution:  
    rename columns of individual frames, 
    inner join to filter data (performance boost if done here),  
    effect entire data frame:
    fill empty: fill column (k) with value in (v)
    extract_month: extract the month number from column (v)
    extract_year: extract the month number from column (v)
'''