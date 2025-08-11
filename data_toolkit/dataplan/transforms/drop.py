import pandas as pd
from ..registry import register_transform

@register_transform("drop")
def drop_columns(df: pd.DataFrame, cfg: dict):
    keep = cfg.get('keep')
    if not keep:
        raise KeyError("drop_columns: 'keep' must be provided and non-empty")

    return df.drop(columns=[c for c in df.columns if c not in keep])