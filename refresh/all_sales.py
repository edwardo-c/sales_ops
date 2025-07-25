from config.paths import ALLSALES_2025, ALLSALES_2024
from data_toolkit.loaders.base_loader import BaseLoader
from data_toolkit.cleaning.plans import PLAN_DIRECT_SALES_ACU
from data_toolkit.cleaning.cleaner import Cleaner
from data_toolkit.exporter.exporter import Exporter

def main():
    file_map = [ALLSALES_2025, ALLSALES_2024]
    loader = BaseLoader(file_map)
    loader.load_data()

    cleaner = Cleaner(loader.data, PLAN_DIRECT_SALES_ACU, append=True)
    cleaner.clean()

    print(cleaner.output.head())
    print(cleaner.output.info())


if __name__ == "__main__":
    main()