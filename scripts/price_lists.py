from config.paths import PRICE_CLASS_EXPORTS_DIR
from data_toolkit.loaders.base_loader import BaseLoader
from data_toolkit.converter import ExcelConverter
from data_toolkit.transformer.transformer import Transformer
import shutil

def main():
    # make local temp copies of files
    safe_dir_with_files = BaseLoader._folder_to_temp_files(PRICE_CLASS_EXPORTS_DIR)
    
    # convert xlsx to csv
    converter = ExcelConverter(visible=False)
    try:
        converter.convert_xlsx_in_folder(safe_dir_with_files)
    finally:
        converter.quit()

    # load all price groups into single df
    df = BaseLoader._single_dataframe_dir_reader(
        '*.csv', safe_dir_with_files
        )

    # split into csvs by customer account number
    df_dict = Transformer.split_by_groups(df, 'Customer')

    # save into destination
    for acct, df in df_dict.items():
        print(acct)
        print(df.head())

    # delete temp
    shutil.rmtree(safe_dir_with_files)

if __name__ == "__main__":
    main()