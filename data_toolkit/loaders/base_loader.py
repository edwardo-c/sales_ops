from data_toolkit.logger import logger
from pathlib import Path
import tempfile
import shutil
import pandas as pd
import time

class BaseLoader:
    def __init__(self, file_map):
        self.file_map = file_map
        self.data = {}

    @staticmethod
    def _read_file(path: Path, file_meta: dict = None) -> pd.DataFrame:
        try:
            match path.suffix:
                case '.xlsx':
                    return pd.read_excel(
                        path,
                        sheet_name=file_meta.get('sheet_name'),
                        header=file_meta.get('row', 0)
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

    def load_data(self):
        """Reads and stores all files listed in file_map using a temp copy"""
        for file_meta in self.file_map:
            try:
                df = BaseLoader._read_file_with_temp_copy(file_meta)
                self.data[file_meta['alias']] = df
            except Exception as e:
                logger.error(f"Failed to load data for alias '{file_meta['alias']}'", exc_info=True)

    @staticmethod
    def _read_temp_file(alias: str, file_path: Path) -> dict:
        """Backwards-compatible helper for reading a single temp file"""
        dummy_file_map = {"file": str(file_path), "alias": alias}
        df = BaseLoader._read_file_with_temp_copy(dummy_file_map)
        return {alias: df}
    
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

