from data_toolkit.loaders.base_loader import BaseLoader
from datetime import datetime
import pandas as pd
from pathlib import Path

class RefreshLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.columns = ['timestamp', 'pipeline', 'status', 'records', 'notes']
        self._init_log()

    def _init_log(self):
        if not self.log_path.exists():
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.log_path, index=False)

    def log(self, pipeline: str, status: str, records: int = None, notes: str = ""):
        new_entry = {
            'timestamp': datetime.now().isoformat(timespec='seconds'),
            'pipeline': pipeline,
            'status': status,
            'records': records,
            'notes': notes
        }

        if not isinstance(self.log_path, Path):
            self.log_path = Path(self.log_path)

        df_dict = BaseLoader._read_temp_file('log', self.log_path)
        df = df_dict['log']
        pd.concat([df['log'], pd.DataFrame([new_entry])], ignore_index=True)
        df.sort_values(by='timestamp', ascending=False, inplace=True)
        df.to_csv(self.log_path, index=False)
