from config.paths import STATUS_REPORT_PATH, ALLSALES_2024, ALLSALES_2025
from data_toolkit.loaders.base_loader import BaseLoader
from data_toolkit.exporter.exporter import Exporter
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

def main():
   pipeline = StatusReportPipeline()
   pipeline.run()

class StatusReportPipeline():
    def __init__(self):
        self.status_report_customers = BaseLoader.load_data([STATUS_REPORT_PATH])
        self.status_report_benefits = BaseLoader.load_data([
            {'file': STATUS_REPORT_PATH, 'sheet_name': 'benefits'},
            ])
        # self.fact_table = BaseLoader() #TODO: Load fact table
        
    def run(self):
        # used only for inspection, workflow 
        customer_df = list(self.status_report_customers.values())[0]
        benefits_df = list(self.status_report_benefits.values())[0]

        print("Customer Data (head):")
        print(customer_df.head())

        print("\nBenefits Data (head):")
        print(benefits_df.head())


    def load_data(self):
        self.benefits_data = self.benefits_loader._read_file_with_temp_copy(
            self.benefits.file_map)

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