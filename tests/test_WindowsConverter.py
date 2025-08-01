import win32com.client as win32
from data_toolkit.converter import WindowsConverter

def test_xlsx_to_csv():
    try:
        save_path = r"C:\Users\eddiec11us\Desktop\test_2.xlsx"
        
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False

        wb = excel.Workbooks.Add()
        wb.SaveAs(save_path, FileFormat=51) 
    finally:
        excel.Quit()
        

# pytest .\tests\test_WindowsConverter.py 