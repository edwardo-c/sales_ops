from config.paths import STATUS_REPORT_PATH, ALLSALES_2024, ALLSALES_2025
from data_toolkit.loaders.base_loader import BaseLoader
from data_toolkit.exporter.exporter import Exporter
import pandas as pd

# BaseLoader needs to select columns on import
# and return single dataframe if needed


def main():
   pipeline = StatusReportPipeline()
   pipeline.run()

class StatusReportPipeline():
    def __init__(self):
        self.benefits_loader = BaseLoader.from_map_components(
            alias='status_report_benefits', 
            file=STATUS_REPORT_PATH,
            sheet_name='benefits',
            row=0
        )
        self.facts_loader = BaseLoader([ALLSALES_2024, ALLSALES_2025])
        self.benefits_data = pd.DataFrame
        self.facts_data = pd.DataFrame

    def run(self):
        self.load_data()

    def load_data(self):
        self.benefits_data = self.benefits_loader._read_file_with_temp_copy(self.benefits.file_map)


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