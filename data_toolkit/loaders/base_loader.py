from data_toolkit.logger import logger
from pathlib import Path
import tempfile
import shutil as sh
import pandas as pd
import time

class BaseLoader:
    def __init__(self, *file_details):
        self.file_details = self._normalize_file_detail(file_details)
        self.data = self.load_data()
        self.concat_data = pd.DataFrame
        self._all_paths = False
        self.temp_dir = Path(tempfile.mkdtemp())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # delete temp dir
        sh.rmtree(self.temp_dir, ignore_errors=True)

    def load_data(self):
        if self._all_paths: # standardize data structure
            file_details = self._set_default_file_params()
        else:
            file_details = self.file_details

        result = {
                file_detail['alias']: self._read_file_with_temp_copy(file_detail) 
                for file_detail in file_details
            }
        return result

    def _read_file_with_temp_copy(self, file_details: dict) -> pd.DataFrame:
        src_path = Path(file_details['file'])
        file_meta = file_details['file_meta']
        dst_path = self.temp_dir / src_path.name

        self._safe_copy_file(src_path, dst_path)
        df = self._read_file(dst_path, file_meta)
        logger.info(f"Read {dst_path} successfully as alias '{file_meta['alias']}'")

        return df

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
                sh.copy2(src, dst)
                logger.info(f"Copied {src.name} to temp dir")
                return
            except PermissionError:
                logger.warning(f"PermissionError while copying {src}. Retrying...")
                time.sleep(delay)
        logger.error(f"Failed to copy file after {retries} attempts: {src}")
        raise PermissionError(f"Could not copy {src} after {retries} attempts")

    @staticmethod
    def _default_file_params(self, detail):
        return {
            'file': detail,
            'alias': Path(detail).stem,
        }

    @staticmethod
    def _normalize_file_detail(detail):
        '''
        Ensures every input becomes a standardized file map:
        {
            'file': path,
            'file_meta': {
                'alias': ...,
                'sheet_name': ...,
                ...
            }
        }
        '''
        if isinstance(detail, str):
            if not Path(detail).is_file():
                raise FileNotFoundError(f"File does not exist: {detail}")
            return {
                'file': detail,
                'file_meta': BaseLoader._default_file_params(detail)
            }

        elif isinstance(detail, dict):
            file_path = detail.get('file')
            if not file_path:
                raise ValueError(f"Missing 'file' key in: {detail}")
            if not Path(file_path).is_file():
                raise FileNotFoundError(f"File does not exist: {file_path}")

            # Merge default params with overrides from the user
            default_meta = BaseLoader._default_file_params(file_path)
            user_meta = detail.get('file_meta', {})
            default_meta.update(user_meta)

            return {
                'file': file_path,
                'file_meta': default_meta
            }

        else:
            raise TypeError("Each input must be a str (file path) or dict (file plan).")
