import pandas as pd
from ..registry import register_transform

@register_transform("fill_empty")
def fill_empty(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    # mapping: {"colA": 0, "colB": "N/A"}
    return df.fillna(value=mapping)
