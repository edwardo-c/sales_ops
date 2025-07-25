# used for loading original data into dataframes
# creates temporary file for faster upload
from pathlib import Path
import tempfile
import shutil
import pandas as pd

class BaseLoader():
    def __init__(self, file_map):
        self.file_map = file_map
        self.data = {}

    @staticmethod
    def _read_file(path: Path, file_meta: dict) -> pd.DataFrame:
        match path.suffix:
            case '.xlsx':
                return pd.read_excel(
                    path,
                    sheet_name=file_meta['sheet_name'],
                    header=file_meta['row']
                )
            case '.csv':
                return pd.read_csv(path)
            case _:
                raise ValueError(f"Unsupported file type: {path.suffix}")    
        

    def load_data(self):
        ''' create a temp copy and read data frame '''
        temp_dir = Path(tempfile.mkdtemp())

        try: 
            for file in self.file_map:
                
                # create path object
                src_path = Path(file['file'])
                
                # build destination path
                dst_path = temp_dir / src_path.name
                
                # create a copy in temp directory
                shutil.copy2(src_path, dst_path)

            self.data[file['alias']] = self._read_file(dst_path, file)

        finally:
            shutil.rmtree(temp_dir)

    @staticmethod
    def _read_temp_file(alias: str, file_path: Path):
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        # initiate temp directory
        temp_dir = Path(tempfile.mkdtemp())

        # build temp file path
        dst_path = temp_dir / file_path
        
        # copy over path to temp file
        shutil.copy2(file_path, dst_path)

        df = self._read_file(dst_path)

        return {alias: df}