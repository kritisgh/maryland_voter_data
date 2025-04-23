import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Print the first few rows of the original dataframe to check the data
print("Original DataFrame:")
print(df.head())

# Group the data by age bracket, gender, and party, then sum the counts
grouped_df = df.groupby(['age_bracket', 'Gender', 'Party']).sum().reset_index()

# Print the grouped dataframe to see the aggregation
print("\nGrouped DataFrame:")
print(grouped_df.head())

# Calculate total counts for each age bracket
total_counts = grouped_df.groupby('age_bracket')['Count'].sum().reset_index()
total_counts.rename(columns={'Count': 'Total'}, inplace=True)

# Print the total counts dataframe to verify totals
print("\nTotal Counts DataFrame:")
print(total_counts.head())