import pandas as pd

df = pd.read_csv('agg_MD.csv', index_col=0)

df_No_2020 = df.drop('voted_2020', axis='columns', inplace =True)
df_No_2016 = df.drop('voted_2016', axis='columns', inplace =True)
df_No_gender = df.drop('Gender', axis='columns', inplace =True)

df.to_csv('2024_agg_md.csv', index=False)



