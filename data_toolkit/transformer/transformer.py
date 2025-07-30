import pandas as pd


class Transformer():
    '''
    Used for transforming and reshaping data
    '''
    def __init__(self):
        self.output_df = {}
    
    @staticmethod
    def split_by_groups(df: pd.DataFrame, group_by: str) -> dict[str, pd.DataFrame]:
        '''
        splits entire data frame
        args:
            df: the data frame to split
            group_by: column to group by and use as return key
        returns: 
            dictionary containing group_by (key) and individual 
            data frame for specified group (value)
        '''
        return {name: group for name, group in df.groupby(group_by)}