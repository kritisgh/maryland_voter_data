import pandas as pd

df = pd.read_csv('agg_MD.csv')

df_No_2020 =df.drop('voted_2020', axis=1)
df.drop('voted_2016', axis=1)


print(df_No_2020)
