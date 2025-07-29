from data_toolkit.logger import logger
from config.paths import ALLSALES_2025, ALLSALES_2024, DATABASE, ALL_SALES_LOG
from data_toolkit.refresh_logger.refresh_logger import RefreshLogger
from data_toolkit.loaders.base_loader import BaseLoader
from data_toolkit.cleaning.plans import PLAN_DIRECT_SALES_ACU
from data_toolkit.cleaning.cleaner import Cleaner
from data_toolkit.exporter.exporter import Exporter
from pathlib import Path

def main():
    logger.info(f"running refresh.all_sales.py")

    data_log_path = Path(ALL_SALES_LOG)
    data_log = RefreshLogger(data_log_path)

    try: 
        file_map = [ALLSALES_2025, ALLSALES_2024]
        loader = BaseLoader(file_map)
        loader.load_data()

        cleaner = Cleaner(loader.data, PLAN_DIRECT_SALES_ACU, append=True)
        cleaner.clean()

        exporter = Exporter(cleaner.output)
        exporter.to_sql(DATABASE, 'allsales')

        logger.info(f"all_sales | status=success | rows={len(cleaner.output)}")

    except Exception as e:
        data_log.log('all_sales', 'failed', notes={e})

if __name__ == "__main__":
    main()


'''transformer class ideas:
unpivot
break apart into separate groups with group by
'''