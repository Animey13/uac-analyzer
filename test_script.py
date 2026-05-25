import pandas as pd
df = pd.read_csv('data/uac_with_kpis.csv', parse_dates=['date'])
print(df.columns)
