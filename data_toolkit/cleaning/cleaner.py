from data_toolkit.loaders.base_loader import BaseLoader
import pandas as pd

class Cleaner():
    def __init__(self, data: dict[str: pd.DataFrame], clean_plan: dict[str: list], append: bool=False):
        self.data = data
        self.clean_plan = clean_plan
        self.append = append,
        self.output = None
    
    def clean(self):
        # append then clean, else clean individually
        if self.append:
            combined = pd.concat(list(self.data.values()), ignore_index=True)
            self.output = self._apply_clean(combined, self.clean_plan)
        else:
            cleaned = {}
            for alias, df in self.data.items():
                df = self._apply_clean(df, self.clean_plan)
                cleaned[alias] = df
            self.output = cleaned
    
    def _apply_clean(self, df: pd.DataFrame, plan: dict):
        #TODO: format date columns to isoformat for sql upload
        if plan.get("keep_columns"):
            df = df[plan["keep_columns"]]

        if plan.get("rename_columns"):
            df = df.rename(columns=plan["rename_columns"])

        if plan.get("data_types"):
            df = df.astype(plan["data_types"]).dtypes

        return df


