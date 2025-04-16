import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Set the matplotlib backend to Agg for headless environments
matplotlib.use('Agg')

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

# Drop the 'Total' column from the percentage DataFrame
percentage_df.drop(columns=['Total'], inplace=True)

# Reset the index to make age_bracket a column
percentage_df.reset_index(inplace=True)

# Melt the DataFrame for easier plotting with seaborn
melted_df = percentage_df.melt(id_vars='age_bracket', var_name='Category', value_name='Percentage')

# Plot the data using seaborn
plt.figure(figsize=(12, 8))
sns.barplot(data=melted_df, x='age_bracket', y='Percentage', hue='Category')
plt.title('Percentage Distribution by Age Bracket, Gender, and Party')
plt.xticks(rotation=45)
plt.ylabel('Percentage')
plt.xlabel('Age Group')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save the plot to a file instead of displaying it
plt.savefig('percentage_distribution_chart.png')