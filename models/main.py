import pandas as pd

path = '/home/toliman/Desktop/month=2021-6 (1).parquet'

data = pd.read_parquet(path)
print(data.columns)
print(data.head(20))
