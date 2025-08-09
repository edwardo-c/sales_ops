import pandas as pd
from ..registry import register_transform

@register_transform("join")
def join(df_left: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    # cfg: {"right": df2, "on": ["key"], "how": "inner"}
    right = cfg["right"]
    on = cfg["on"]
    how = cfg.get("how", "inner")
    return df_left.merge(right, on=on, how=how)
