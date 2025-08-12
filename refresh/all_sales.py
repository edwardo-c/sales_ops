from data_toolkit.base_loader import BaseLoader
from data_toolkit.plans.file_reader_details import STATUS_REPORT_SALES_2024, STATUS_REPORT_SALES_2025
from config.paths import DATABASE
from data_toolkit.dataplan import transforms  # noqa: triggers auto-registration
from data_toolkit.dataplan.registry import GLOBAL_REGISTRY, build_registry
from data_toolkit.dataplan.executor import DataPlanExecutor
from data_toolkit.exporter import Exporter
import pandas as pd

project_registry = build_registry(
    include=["rename_columns", "static_value",]
)

class RefreshAllSales:
    def __init__(self):
        self.dirty_data = None
        self.all_sales = None

    def run(self):
        self.dirty_data = self._get_dirty_data()
        self.all_sales = self._execute_clean_plan()
        self._import_into_mssql()
        print(self.all_sales.head())
        return self.all_sales  # handy for tests or chaining

    def _get_dirty_data(self):
        base_loader = BaseLoader(
            STATUS_REPORT_SALES_2024,
            STATUS_REPORT_SALES_2025,
        )
        return base_loader.data  # {'alias': df}

    def _execute_clean_plan(self):
        plans = {
            "allsales_2025": [
                {"op": "rename_columns", "args": {
                    "Customer Account Number": "acct_num",
                    "Amount": "amount",
                    "Classification(Sales Category)": "product_category",
                    "Invoice Date": "invoice_date",
                    "Inventory CD": "part_number",
                }},
                {"op": "static_value", "args": {"value": 2025, "col_name": "invoice_year"}},
            ],
            "allsales_2024": [
                {"op": "rename_columns", "args": {
                    "Account No.": "acct_num",
                    "Amount": "amount",
                    "Category": "product_category",
                    "Invoice Date": "invoice_date",
                    "Inventory CD": "part_number",
                }},
                {"op": "static_value", "args": {"value": 2024, "col_name": "invoice_year"}},
            ],
        }

        executor = DataPlanExecutor(self.dirty_data, plans, registry=project_registry, strict=False)
        all_sales_dict = {'all_sales': pd.concat(executor.processed_data.values())}
        # TODO: Execute a clean plan on all sales
        return all_sales_dict['all_sales']

    def _import_into_mssql(self):
        e = Exporter(self.all_sales)
        e.to_sql(
            table_name="status_report_all_sales",
            engine_url=DATABASE,
            if_exists="replace"
        )

def main():
    print("running refresh.all_sales")
    RefreshAllSales().run()
    print("refresh.all_sales complete")

if __name__ == "__main__":
    main()
