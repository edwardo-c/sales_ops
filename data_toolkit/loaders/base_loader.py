from data_toolkit.logger import logger
from pathlib import Path
import tempfile
import shutil
import pandas as pd
import time

class BaseLoader:
    '''
    FileMap: {
        'alias':'my_alias', 
        'file': 'my_file_path',
        'sheet_name': 'my_sheet_name',
        'row': int
    }
    '''
    def __init__(self, file_map):
        self.file_map = file_map
        self.data = self.load_data()
        self.concat_data = pd.DataFrame

    @classmethod
    def from_map_components(cls, alias: str, file: str, sheet_name: str, row: int, usecols: list = None):
        file_map = {
            'alias': alias, 'file': file, 
            'sheet_name': sheet_name, 
            'row': row, 'usecols': usecols
            }
        return cls(file_map)

    @staticmethod
    def _read_temp_file(file_path: Path, sheet_name: str, usecols: list = None) -> pd.DataFrame:
        '''
        Backwards-compatible helper for reading a single temp file
        args:
            file_path: file to be read safely
            sheet_name: sheet name from file path to read
            usecols: columns to use in returned data frame, default all columns
        '''
        dummy_file_map = {
            'alias': 'dummy', 
            'file': str(file_path),
            'sheet_name': sheet_name,
            'usecols': usecols
            }
        df = BaseLoader._read_file_with_temp_copy(dummy_file_map)
        return df
    
    @staticmethod
    def _single_dataframe_dir_reader(pattern: str, dir: Path):
        '''
        reads files from dir and returns a single dataframe 
        of the files matching the pattern
        '''
        # return a list containing all file names
        files = list(Path(dir).glob(pattern=pattern, case_sensitive=False))

        # read those file names
        return pd.concat([pd.read_csv(file) for file in files])
        
    @staticmethod
    def _folder_to_temp_files(src_dir: Path):
        '''
        copies all files into a local temp folder
        args:
            src_dir: directory to be copied recursively
        '''
        if not Path(src_dir).is_dir():
            raise ValueError(f"src_dir: {src_dir} is not a directory")

        dst_dir = Path(tempfile.mkdtemp())

        return shutil.copytree(src_dir, dst_dir)
    
    # ------ Working on clean up of class, these are in use, modify with caution ------ #
    @staticmethod
    def _read_file(path: Path, file_meta: dict = None) -> pd.DataFrame:
        '''attempt to read provided file by suffix, only xlsx and csv at this time'''
        try:
            match path.suffix:
                case '.xlsx':
                    # TODO: implement usecols in df.read
                    return pd.read_excel(
                        path,
                        sheet_name=file_meta.get('sheet_name'),
                        header=file_meta.get('row', 0),
                        usecols=file_meta.get('usecols', None),
                        dtype=file_meta.get('dtype', None),
                    )
                case '.csv':
                    return pd.read_csv(path)
                case _:
                    raise ValueError(f"Unsupported file type: {path.suffix}")
        except Exception as e:
            logger.error(f"Failed to read file: {path}", exc_info=True)
            raise

    @staticmethod
    def _safe_copy_file(src: Path, dst: Path, retries: int = 3, delay: float = 0.5):
        for attempt in range(retries):
            try:
                logger.debug(f"Attempting to copy {src} to {dst} (Attempt {attempt + 1})")
                shutil.copy2(src, dst)
                logger.info(f"Copied {src.name} to temp dir")
                return
            except PermissionError:
                logger.warning(f"PermissionError while copying {src}. Retrying...")
                time.sleep(delay)
        logger.error(f"Failed to copy file after {retries} attempts: {src}")
        raise PermissionError(f"Could not copy {src} after {retries} attempts")

    @staticmethod
    def _read_file_with_temp_copy(file_meta: dict) -> pd.DataFrame:
        src_path = Path(file_meta['file'])
        temp_dir = Path(tempfile.mkdtemp())
        dst_path = temp_dir / src_path.name

        try:
            BaseLoader._safe_copy_file(src_path, dst_path)
            df = BaseLoader._read_file(dst_path, file_meta)
            logger.info(f"Read {dst_path} successfully as alias '{file_meta['alias']}'")
            return df
        finally:
            try:
                dst_path.unlink(missing_ok=True)
                temp_dir.rmdir()
            except Exception as e:
                logger.warning(f"Could not fully clean up temp file: {dst_path}", exc_info=True)

    @staticmethod
    def _standardize_file_meta(file_meta):
        '''
        Fills single file paths with dummy file map
        dependency for reading in this class
        '''
        if isinstance(file_meta, dict):
            # If it's a dictionary, ensure required keys exist
            file_meta.setdefault('alias', 'dummy')
            file_meta.setdefault('file', file_meta.get('file')) 
            file_meta.setdefault('sheet_name', 0)
            file_meta.setdefault('row', 0)
            file_meta.setdefault('usecols', None)
            file_meta.setdefault('dtype', None)
            return file_meta

        # Try converting it to a Path to validate it's a file
        try:
            Path(file_meta)
        except TypeError:
            raise ValueError("Invalid data type passed to _standardize_file_meta")

        # If successful, return a default file_meta dict
        return {
            'alias': 'dummy',
            'file': file_meta,
            'sheet_name': 0,
            'row': 0,
            'usecols': None,
            'dtype': None,
        }

    @staticmethod
    def concat_data(data: dict):
        '''Collapses a data dict {'alias': df,} into a single data frame'''
        return pd.concat(list(data.values()))

    @staticmethod
    def load_data(file_map: list):
        '''
        Reads and returns all files listed in file_map using a temp copy.
        
        Args:
            file_map: list of file paths or file_meta dicts

        Returns:
            Dict[str, pd.DataFrame]: alias -> DataFrame
        '''
        if not isinstance(file_map, list):
            raise TypeError("file_map must be a list of file paths or file_meta dictionaries")

        clean_file_meta = [
            BaseLoader._standardize_file_meta(file_meta)
            for file_meta in file_map
        ]

        data_dict = {}
        for meta in clean_file_meta:
            try:
                df = BaseLoader._read_file_with_temp_copy(meta)
                data_dict[meta['alias']] = df
            except Exception as e:
                logger.error(f"Failed to load data for alias '{meta['alias']}': {e}", exc_info=True)

        return data_dict
