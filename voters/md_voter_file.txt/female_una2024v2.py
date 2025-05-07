import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Filter for Female UNA voters who voted in 2024
female_una_data = df[
    (df['Gender'] == 'Female') & 
    (df['Party'] == 'UNA') & 
    (df['voted_2024'] > 0)
]

# Group the data by age bracket and sum the counts
grouped_df = female_una_data.groupby('age_bracket').sum().reset_index()

# Calculate total counts for each age bracket across all genders and parties
total_counts = df.groupby('age_bracket')['Count'].sum().reset_index()
total_counts.rename(columns={'Count': 'Total'}, inplace=True)

# Merge total counts with the filtered data
merged_df = pd.merge(grouped_df, total_counts, on='age_bracket')

# Calculate the percentage of Female UNA relative to the total for each age bracket
merged_df['Percentage'] = (merged_df['Count'] / merged_df['Total']) * 100

# Create an interactive bar chart using Plotly
fig = px.bar(
    merged_df, 
    x='age_bracket', 
    y='Percentage',
    title='Percentage of Female UNA Voters in 2024 by Age Bracket',
    labels={'Percentage': 'Percentage of Votes', 'age_bracket': 'Age Group'},
    hover_data={
        'Percentage': ':.2f',  # Format percentage to two decimal places
        'Total': ':.0f',  # Include total count in hover data, formatted as integer
        'Count': ':.0f'  # Include the count of Female UNA votes in hover data
    },
    color_discrete_sequence=['pink'],  # Use distinct colors for each age group
)

# Update layout for better aesthetics
fig.update_layout(
    xaxis_title='Age Group',
    yaxis_title='Percentage of Votes',
    xaxis_tickangle=-45
)

# Show the interactive plot
fig.show()