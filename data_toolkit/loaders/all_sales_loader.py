# used to refresh data from category sales raw data source
# specifically used for customer analysis NOT rep credit

from base_loader import BaseLoader

class AllSales(BaseLoader):
    # return and upload into sql
    def __init__(self):
        ...

    # convert ifs data to acumatica schema
    def 