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

# Create a function to prepare the data for plotting
def prepare_data(gender, parties):
    # Filter the data for the specified gender and parties
    filtered_df = grouped_df[
        (grouped_df['Gender'] == gender) & (grouped_df['Party'].isin(parties))
    ]

    # Merge total counts with the filtered data
    merged_df = pd.merge(filtered_df, total_counts, on='age_bracket')

    # Calculate the percentage of each category relative to the total for each age bracket
    merged_df['Percentage'] = (merged_df['Count'] / merged_df['Total']) * 100

    # Create a new column for combined gender and party for easy plotting
    merged_df['Category'] = merged_df['Gender'] + '_' + merged_df['Party']

    return merged_df

# Prepare data for each chart
female_data = prepare_data(gender='Female', parties=['DEM', 'REP'])
male_data = prepare_data(gender='Male', parties=['DEM', 'REP'])

# Plot the data using seaborn
plt.figure(figsize=(14, 16))

# Create subplot for Female_DEM and Female_REP
plt.subplot(2, 1, 1)
sns.barplot(
    data=female_data, 
    x='age_bracket', 
    y='Percentage', 
    hue='Category',
    palette={'Female_DEM': 'blue', 'Female_REP': 'red'}
)
plt.title('Higher Female REP and DEM Participation in Older Age Groups')
plt.xticks(rotation=45)
plt.ylabel('Percentage')
plt.xlabel('Age Group')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Create subplot for Male_DEM and Male_REP
plt.subplot(2, 1, 2)
sns.barplot(
    data=male_data, 
    x='age_bracket', 
    y='Percentage', 
    hue='Category',
    palette={'Male_DEM': 'blue', 'Male_REP': 'red'}
)
plt.title('Balanced Male DEM and REP Participation Across Age Groups')
plt.xticks(rotation=45)
plt.ylabel('Percentage')
plt.xlabel('Age Group')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save the plot to a file instead of displaying it
plt.savefig('combined_gender_party_distribution_chart.png')
print("Chart saved as 'combined_gender_party_distribution_chart.png'")