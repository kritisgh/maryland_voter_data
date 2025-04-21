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

# Prepare data for Female_DEM
female_dem_data = grouped_df[
    (grouped_df['Gender'] == 'Female') & (grouped_df['Party'] == 'DEM')
]

# Merge total counts with the filtered data
female_dem_merged = pd.merge(female_dem_data, total_counts, on='age_bracket')

# Calculate the percentage of Female_DEM relative to the total for each age bracket
female_dem_merged['Percentage'] = (female_dem_merged['Count'] / female_dem_merged['Total']) * 100

# Define a custom color palette with distinct colors for each age group
custom_palette = ['brown', 'teal', 'lime', 'navy', 'gold']

# Plot the data using seaborn
plt.figure(figsize=(12, 8))
sns.barplot(
    data=female_dem_merged, 
    x='age_bracket', 
    y='Percentage', 
    palette=custom_palette
)
plt.title('Female DEM Participation for each Age Group')
plt.xticks(rotation=45)
plt.ylabel('Percentage')
plt.xlabel('Age Group')
plt.tight_layout()

# Save the plot to a file instead of displaying it
plt.savefig('female_dem_percentage_distribution_chart.png')
print("Chart saved as 'female_dem_percentage_distribution_chart.png'")