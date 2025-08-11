import pandas as pd
from ..registry import register_transform

@register_transform("filter_in")
def filter_in(df: pd.DataFrame, cfg: dict):
    """
    keep rows where 'cfg['column']' is in 'cfg['values']'
    cfg:
        column: str                 # e.g., "product_category
        values: list[str]           # e.g, ["mounts", "dvled", "kiosk", "dvled"]
        case_insensative: bool = True
        keep_na: bool = False       # if True, NaNs are retained  
    """
    col = cfg["column"]
    values = cfg["values"]
    case_insensitive = cfg.get("case_insensative", True)
    keep_na = cfg.get("keep_na", False)

    if col not in df.columns:
        raise KeyError(f"filter_in: column '{col}' not in dataframe")
    
    if case_insensitive:
        # normalize both sides
        series = df[col].astype(str).str.strip().str.lower()
        allowed = {str(v).strip().lower() for v in values}
        mask = series.isin(allowed)
    else:
        mask = df[col].isin(values)

    if keep_na:
        mask = mask | df[col].isna()

    return df.loc[mask].copy()

