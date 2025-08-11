import pandas as pd
from ..registry import register_transform

@register_transform("static_value")
def static_value(df: pd.DataFrame, cfg: dict):
    col_name = cfg["col_name"]
    val = cfg["value"]

    df_copy = df.copy()
    df_copy[col_name] = val
    return df_copy
