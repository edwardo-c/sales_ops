from sqlalchemy import create_engine, text
import pandas as pd
from pathlib import Path
import json
import re


class ReportBuilder:
    def __init__(self, query_path, mapping_path, db, query_params=None, convert_at_params=False):
        """
        query_params: dict of params for :named_params (e.g., {"current_year": 2025, "previous_year": 2024})
        convert_at_params: if True, will convert @param to :param so SSMS-style SQL can run via SQLAlchemy
        """
        self.db = db
        self.query_path = query_path
        self.mapping = self._load_mapping(mapping_path)   # JSON map stays the same
        self.query_params = query_params or {}
        self.convert_at_params = convert_at_params

        # load data immediately (keeps your original flow)
        self.data = self._query(self.query_path, self.db, self.query_params, self.convert_at_params)

    def run(self):
        # for now, just show what we pulled + mapping available
        print(self.data.head())
        print(self.mapping)

    def _load_mapping(self, mapping_path):
        raw = json.loads(Path(mapping_path).read_text(encoding='UTF-8'))
        # Your JSON root key typo ("status repot") is handled by taking first value
        return next(iter(raw.values()))

    def _query(self, query_path, db, params: dict, convert_at_params: bool):
        engine = create_engine(db)
        sql = Path(query_path).read_text(encoding='UTF-8')

        # Optional: allow writing @current_year in the .sql file and run via SQLAlchemy
        # Converts @name -> :name (and removes DECLARE blocks if present for testing)
        if convert_at_params:
            # strip DECLARE blocks (handy if your file includes SSMS test harness)
            sql = re.sub(r"(?is)^\s*DECLARE\b.*?;\s*", "", sql)
            sql = re.sub(r"@([A-Za-z_]\w*)", r":\1", sql)

        with engine.begin() as conn:
            df = pd.read_sql_query(text(sql), conn, params=params)
        return df

    def _iter_cell_field_pairs(self):
        for section, inner in self.mapping.items():
            if isinstance(inner, dict):
                for cell, field in inner.items():
                    yield cell, field

    # -------- Optional helpers for batch reporting (multi-row result) --------
    def iter_reports(self, id_col="acct_num"):
        """
        Yields one dict per report row. Perfect for looping and writing one Excel per account.
        """
        for row in self.data.to_dict("records"):
            # suggest a filename based on id_col if present
            filename = f"{row[id_col]}.xlsx" if id_col in row else "report.xlsx"
            yield row, filename

        
# python -m pipelines.status_reports.main