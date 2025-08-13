from data_toolkit.report import ReportBuilder
from config.paths import STATUS_REPORT_QUERY, STATUS_REPORT_JSON_PATH, DATABASE

def main():
    print(f"running statusreports.main")

    # refresh 'status_report_all_sales' table in sql
    # r = RefreshAllSales()

    rb = ReportBuilder(
    query_path=STATUS_REPORT_QUERY,
    mapping_path=STATUS_REPORT_JSON_PATH,
    db=DATABASE,
    query_params={"current_year": 2025, "previous_year": 2024},
    convert_at_params=True  # convert @vars in the .sql to :vars for SQLAlchemy
    )
    rb.run()

    for row, fname in rb.iter_reports(id_col="acct_num"):
        # Here you’d call write_to_template(row, template_path, out_path, ...)
        # e.g., ws[cell] = row[field] for each (cell, field) in _iter_cell_field_pairs()
        print("Would write file:", fname)

if __name__ == '__main__':
    main()

# paste to run during temp: python -m pipelines.status_reports.main