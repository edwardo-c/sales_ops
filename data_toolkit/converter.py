import win32com.client as win32
from pathlib import Path

class ExcelConverter():
    def __init__(self, visible: bool):
        self.excel = win32.gencache.EnsureDispatch('Excel.Application')
        self.excel.Visible = visible

    def convert_xlsx_to_csv(self, file: Path, csv_path: str):
        wb = self.excel.Workbooks.Open(file)
        wb.SaveAs(csv_path, FileFormat=6)
        wb.Close(False)

    def convert_xlsx_in_folder(self, folder: Path):
        
        for file in folder.glob('*xlsx'):
            csv_path = file.with_suffix('.csv')
            self.convert_xlsx_to_csv(file, csv_path)

    def quit(self):
        self.excel.Quit()
    