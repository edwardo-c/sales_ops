from data_toolkit.report import ReportBuilder
from data_toolkit.exporter import Exporter
from config.paths import (
    STATUS_REPORT_QUERY, 
    STATUS_REPORT_JSON_PATH, 
    DATABASE,
    STATUS_REPORT_TEMPLATE_PATH,
    STATUS_REPORT_DIR,
    STATUS_REPORT_DIMENSIONS
)
import pandas as pd


def main():
    print(f"running statusreports.main")

    # refresh sql table status_report_all_sales
    # r = RefreshAllSales()

    # refresh sql table std_cat_customers 
    df = pd.read_excel(STATUS_REPORT_DIMENSIONS, sheet_name="std_cat_customers")
    e = Exporter(df)
    e.to_sql("std_cat_customers", DATABASE, if_exists="replace")

    rb = ReportBuilder(
    query_path=STATUS_REPORT_QUERY,
    mapping_path=STATUS_REPORT_JSON_PATH,
    db=DATABASE,
    query_params={"current_year": 2025, "previous_year": 2024},
    convert_at_params=True  # convert @vars in the .sql to :vars for SQLAlchemy
    )

    outputs = rb.export_all_reports(
        template_path=STATUS_REPORT_TEMPLATE_PATH,
        out_dir=STATUS_REPORT_DIR,
        sheet_name="Summary"
    )

    print(f"created {len(outputs)} files")

if __name__ == '__main__':
    main()

# paste to run during temp: python -m pipelines.status_reports.main