import pandas as pd
import logging
from typing import Callable, Dict, Any, List

logging.basicConfig(level=logging.INFO)
# dataplan/executor.py
import logging
import pandas as pd
from typing import Callable, Dict, Any, List

class DataPlanExecutor:
    def __init__(self, data_dict: dict, plans: dict, *, registry: Dict[str, Callable], strict: bool = False):
        self.registry = registry
        self.strict = strict
        self.processed_data: dict[str, pd.DataFrame] = {}
        self._execute_plan(data_dict, plans)

    def _execute_plan(self, data_dict, plans) -> None:
        for alias, df in data_dict.items():
            steps: List[dict] = plans.get(alias, [])
            if not steps:
                logging.info(f"No plan for '{alias}'. Returning unchanged.")
                self.processed_data[alias] = df
                continue
            self.processed_data[alias] = self._process_steps(df, steps)

    def _process_steps(self, df: pd.DataFrame, steps: List[dict]) -> pd.DataFrame:
        for step in steps:
            op = step.get("op")
            args = step.get("args", {})
            fn = self.registry.get(op)
            if not fn:
                msg = f"Unknown transform '{op}'."
                if self.strict:
                    raise KeyError(msg)
                logging.warning(msg + " Skipping.")
                continue
            df = fn(df, args)
        return df



'''
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
            df = df.astype(plan["data_types"])

        return df

'''

'''
class Transformer():
    Used for transforming and reshaping data

    def __init__(self):
        self.output_df = {}
    
    @staticmethod
    def split_by_groups(df: pd.DataFrame, group_by: str) -> dict[str, pd.DataFrame]:
        
        splits entire data frame
        args:
            df: the data frame to split
            group_by: column to group by and use as return key
        returns: 
            dictionary containing group_by (key) and individual 
            data frame for specified group (value)
        
        return {name: group for name, group in df.groupby(group_by)}

'''