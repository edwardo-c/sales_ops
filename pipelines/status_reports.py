from data_toolkit.plans.file_reader_details import (
    STATUS_REPORT_SALES_2024, 
    STATUS_REPORT_SALES_2025,
    STATUS_REPORT_CUSTOMERS,
    STATUS_REPORT_BENEFITS
) 
from data_toolkit.loaders.base_loader import BaseLoader
from data_toolkit.cleaning.cleaner import Cleaner
import logging
import pandas as pd

# paste to run during temp: python -m pipelines.status_reports

logging.basicConfig(level=logging.WARNING)

def main():
   pipeline = StatusReportPipeline()
   pipeline.run()

# benefits, customers, sales

class StatusReportPipeline():
    def __init__(self):
        self.data = BaseLoader(
            STATUS_REPORT_SALES_2024, 
            STATUS_REPORT_SALES_2025,
            STATUS_REPORT_CUSTOMERS,
            STATUS_REPORT_BENEFITS
            )
        
    def run(self):
        data = self.data.data

        # clean fact table in order to concat
            # rename columns
            # consolidate data

        # --- used only for inspection, workflow --- #
        for d in data:
            try: 
                print(f"\nDataframe head for {d['alias']}: ")
                print(f"\n{d['data'].head()}")
            except Exception as e:
                raise ValueError(f"Expected dictionary, recieved {type(d)}")

    def _prepare_data(self):
        # SQL: inner join benefits and facts:
        # SQL: agg by category totals():
        ...

    def _map_data_to_json(self):
        ...
    
    def _fill_template_with_data(self):
        ...

    def _save_report(self):
        ...

if __name__ == '__main__':
    main()