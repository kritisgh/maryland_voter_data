from sklearn.decomposition import PCA
import pandas as pd


df = pd.read_csv("md_voter_file.txt/county x 100.csv")

pca = PCA(n_components=1)
df['pc_score'] = pca.fit_transform(df[['DEM','REP','UNA','OTH']])
# then rescale: 
df['pc_score_norm'] = (df['pc_score'] - df['pc_score'].min()) / \
                     (df['pc_score'].max() - df['pc_score'].min()) * 2 - 1

df.to_csv('county_normalized.csv')