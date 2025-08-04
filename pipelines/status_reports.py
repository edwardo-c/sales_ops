from config.paths import STATUS_REPORT_PATH
from data_toolkit.loaders.base_loader import BaseLoader
from data_toolkit.exporter.exporter import Exporter


def main():
    status_report_customers_to_sql()
    
    # queries to data frame
    # dataframe to template

def status_report_customers_to_sql():
    # load the status report customers into sql table
    base_loader = BaseLoader.from_map_components(
        alias='status_report_customers',
        file=STATUS_REPORT_PATH,
        sheet_name='status_reports',
        row=0
    )

    df = base_loader._read_file_with_temp_copy(base_loader.file_map)

    e = Exporter(df)
    e.to_sql(base_loader.file_map['alias'])


if __name__ == '__main__':
    main()