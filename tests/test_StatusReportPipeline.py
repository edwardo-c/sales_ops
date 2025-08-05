from data_toolkit.loaders.base_loader import BaseLoader
from config.paths import STATUS_REPORT_PATH
import logging

logging.basicConfig(level=logging.INFO)

def test_pipeline():
    # shortcut paster to run: 
    # pytest .\tests\test_StatusReportPipeline.py --log-cli-level=info
    status_report_customers = BaseLoader.load_data([STATUS_REPORT_PATH])
    status_report_benefits = BaseLoader.load_data([{'file': STATUS_REPORT_PATH, 'sheet_name': 'benefits'}])

    logging.info(f"Customer Keys: {status_report_customers.keys()}")
    logging.info(f"Customer Keys: {status_report_benefits.keys()}")

