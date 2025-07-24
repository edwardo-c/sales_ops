from data_toolkit.loaders.base_loader import BaseLoader
import pandas as pd

class Cleaner():
    def __init__(self, data: dict[str: pd.DataFrame], clean_plan: dict[str: list]):
        self.data = data
    
    def clean(self, plan):
        for alias, df in self.data.items():
            df = self._apply_clean(df, plan)
            self.data[alias] = df
    
    def _apply_clean(self, df: pd.DataFrame, plan: dict):
        if plan.get("keep_columns"):
            df = df[plan["keep_columns"]]      