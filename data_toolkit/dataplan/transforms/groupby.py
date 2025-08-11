import pandas as pd
from ..registry import register_transform

@register_transform("groupby_sum")
def groupby_sum(df: pd.DataFrame, cfg: dict):    
    by = cfg["by"]
    sort = cfg.get("sort", False)
    dropna = cfg.get("dropna", True)
    as_index = cfg.get("as_index", False)



    if isinstance(by, list):
        for c in by:
            if c not in df.columns:
                raise KeyError(f"groupby_sum: column {c} not in dataframe")
    elif isinstance(by, str):
        if by not in df.columns:
            raise KeyError(f"groupby_sum: column {c} not in dataframe")
    else:
        raise ValueError(f"incorrect data type passed to by arg: {type(by)}")

    return df.groupby(by=by, sort=sort, dropna=dropna, as_index=as_index).sum(numeric_only=True)
