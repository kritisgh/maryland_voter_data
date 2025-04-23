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

# Prepare data for Male_UNA
male_una_data = grouped_df[
    (grouped_df['Gender'] == 'Male') & (grouped_df['Party'] == 'UNA')
]

# Merge total counts with the filtered data
male_una_merged = pd.merge(male_una_data, total_counts, on='age_bracket')

# Calculate the percentage of Male_UNA relative to the total for each age bracket
male_una_merged['Percentage'] = (male_una_merged['Count'] / male_una_merged['Total']) * 100

# Define a uniform green color palette
custom_palette = ['brown', 'teal', 'lime', 'navy', 'gold']

# Plot the data using seaborn
plt.figure(figsize=(12, 8))
sns.barplot(
    data=male_una_merged, 
    x='age_bracket', 
    y='Percentage', 
    palette=custom_palette
)
plt.title('Male UNA Participation in each Age Group')
plt.xticks(rotation=45)
plt.ylabel('Percentage')
plt.xlabel('Age Group')
plt.tight_layout()

# Save the plot to a file instead of displaying it
plt.savefig('male_una_percentage_distribution_chart.png')
print("Chart saved as 'male_una_percentage_distribution_chart.png'")