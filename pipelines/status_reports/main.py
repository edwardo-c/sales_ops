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
import pandas as pd

logging.basicConfig(level=logging.WARNING)

project_registry = build_registry(
    include=[
        "rename_columns", "filter_in", 
        "static_value", "drop"
        ]
)

def main():
    print("loading...")
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
                    "Amount": "amount",
                    "Classification(Sales Category)": "product_category",
                },
            },
            {
                "op": "static_value",
                "args": {"value": 2025, "col_name": "invoice_year"},
            },
        ],
        "allsales_2024": [
            {
                "op": "rename_columns",
                "args": {
                    "Account No.": "acct_num",
                    "Amount": "amount",
                    "Category": "product_category",
                },
            },
            {
                "op": "static_value",
                "args": {"value": 2024, "col_name": "invoice_year"},
            },
        ],
    }   


    # prepare sales data
    executor = DataPlanExecutor(data, plans, registry=project_registry, strict=False)
    # create all sales data frame
    all_sales_data = {"all_sales": pd.concat([executor.processed_data["allsales_2025"], executor.processed_data["allsales_2024"]])}

    # add all sales data to be processed
    executor.processed_data.update(all_sales_data)
    processed = executor.processed_data

    all_sales_plan = {
        "all_sales": [
            {
                "op": "filter_in",
                "args": {
                    "column": "product_category",
                    "values": ["mount", "tv", "kiosk", "dvled"],
                    "case_insensitive": True,
                    "keep_na": False
                    },
                "op": "drop",
                "args": {
                    "keep":["acct_num", "product_category", "invoice_year", "amount"],
                    }
                },
            ]
        }

    all_sales_executor = DataPlanExecutor(processed, all_sales_plan,
                                          registry=project_registry, strict=False)
    
    # capture data to be imported into mssql
    all_sales = all_sales_executor.processed_data["all_sales"]
    customers = all_sales_executor.processed_data["customers"]

    # Inspect
    inspect = [all_sales, customers] 
    for i in inspect:
        print(i.head())

if __name__ == '__main__':
    main()

# paste to run during temp: python -m pipelines.status_reports.main



'''
order of plan execution:  
    add static year column to each
'''