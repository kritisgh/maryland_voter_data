import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Group the data by age bracket, gender, and party, then sum the counts
grouped_df = df.groupby(['age_bracket', 'Gender', 'Party']).sum().reset_index()

# Calculate total counts for each age bracket across all genders and parties
total_counts = grouped_df.groupby('age_bracket')['Count'].sum().reset_index()
total_counts.rename(columns={'Count': 'Total'}, inplace=True)

# Prepare data for Male_UNA in voted_2024
male_una_data = grouped_df[
    (grouped_df['Gender'] == 'Male') & (grouped_df['Party'] == 'UNA')
]

# Merge total counts with the filtered data
male_una_merged = pd.merge(male_una_data, total_counts, on='age_bracket')

# Calculate the percentage of Male_UNA relative to the total for each age bracket
male_una_merged['Percentage'] = (male_una_merged['Count'] / male_una_merged['Total']) * 100

# Create an interactive bar chart using Plotly
fig = px.bar(
    male_una_merged, 
    x='age_bracket', 
    y='Percentage',
    title='Male UNA Participation in Voted 2024',
    labels={'Percentage': 'Percentage', 'age_bracket': 'Age Group'},
    hover_data={
        'Percentage': ':.2f',  # Format percentage to two decimal places
        'Total': ':.0f'  # Include total count in hover data, formatted as integer
    },
    color='age_bracket',  # Use distinct colors for each age group
    color_discrete_sequence=['green', 'green', 'green', 'green', 'green']  # Custom color palette
)

# Update layout for better aesthetics
fig.update_layout(
    xaxis_title='Age Group',
    yaxis_title='Percentage',
    xaxis_tickangle=-45
)

# Show the interactive plot
fig.show()