# dataplan/transforms/rename.py
import pandas as pd
from ..registry import register_transform

@register_transform("rename_columns")
def rename_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    return df.rename(columns=mapping)
