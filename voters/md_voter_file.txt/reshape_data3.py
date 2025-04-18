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

# Calculate total counts for each age bracket
total_counts = grouped_df.groupby('age_bracket')['Count'].sum().reset_index()
total_counts.rename(columns={'Count': 'Total'}, inplace=True)

# Filter the data to include only the specified categories
filtered_df = grouped_df[
    ((grouped_df['Gender'] == 'Female') & (grouped_df['Party'].isin(['DEM', 'REP']))) |
    ((grouped_df['Gender'] == 'Male') & (grouped_df['Party'].isin(['DEM', 'REP'])))
]

# Merge total counts with the filtered data
merged_df = pd.merge(filtered_df, total_counts, on='age_bracket')

# Calculate the percentage of each category relative to the total for each age bracket
merged_df['Percentage'] = (merged_df['Count'] / merged_df['Total']) * 100

# Create a new column for combined gender and party for easy plotting
merged_df['Category'] = merged_df['Gender'] + '_' + merged_df['Party']

# Plot the data using seaborn
plt.figure(figsize=(14, 8))
sns.barplot(data=merged_df, x='age_bracket', y='Percentage', hue='Category')
plt.title('Percentage Distribution by Age Bracket for Selected Categories')
plt.xticks(rotation=45)
plt.ylabel('Percentage')
plt.xlabel('Age Group')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save the plot to a file instead of displaying it
plt.savefig('selected_categories_percentage_distribution_chart.png')
print("Chart saved as 'selected_categories_percentage_distribution_chart.png'")