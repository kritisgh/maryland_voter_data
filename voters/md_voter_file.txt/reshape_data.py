import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Group the data by age bracket, gender, and party, then sum the counts
grouped_df = df.groupby(['age_bracket', 'Gender', 'Party']).sum().reset_index()

# Create a pivot table to reshape the data
pivot_df = grouped_df.pivot_table(index='age_bracket', columns=['Gender', 'Party'], values='Count', fill_value=0)

# Flatten the multi-level columns
pivot_df.columns = ['_'.join(col).strip() for col in pivot_df.columns.values]

# Calculate the total for each age bracket
pivot_df['Total'] = pivot_df.sum(axis=1)

# Calculate the percentage of each group relative to the total
percentage_df = pivot_df.div(pivot_df['Total'], axis=0) * 100

# Format percentages to two decimal places
percentage_df = percentage_df.applymap(lambda x: f"{x:.2f}%")

# Drop the 'Total' column from the percentage DataFrame
percentage_df.drop(columns=['Total'], inplace=True)

# Reset the index to make age_bracket a column
percentage_df.reset_index(inplace=True)

# Print the reshaped DataFrame with percentages only
print(percentage_df)