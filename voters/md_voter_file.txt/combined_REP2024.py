import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Filter the data for Female Republicans (REP) and Male Republicans (REP)
female_rep_df = df[(df['Gender'] == 'Female') & (df['Party'] == 'REP')]
male_rep_df = df[(df['Gender'] == 'Male') & (df['Party'] == 'REP')]

# Group the data by age bracket and sum the counts for voted_2024
female_age_bracket_voted_2024 = female_rep_df.groupby('age_bracket')['voted_2024'].sum().reset_index()
male_age_bracket_voted_2024 = male_rep_df.groupby('age_bracket')['voted_2024'].sum().reset_index()

# Add a column to identify the gender
female_age_bracket_voted_2024['Gender'] = 'Female'
male_age_bracket_voted_2024['Gender'] = 'Male'

# Combine the data for both genders
combined_voted_2024 = pd.concat([female_age_bracket_voted_2024, male_age_bracket_voted_2024])

# Calculate total counts for each age bracket across all genders and parties for comparison
total_counts = df.groupby('age_bracket')['Count'].sum().reset_index()
total_counts.rename(columns={'Count': 'Total'}, inplace=True)

# Merge total counts with the combined REP data
merged_data = pd.merge(combined_voted_2024, total_counts, on='age_bracket')

# Calculate the percentage of voters who voted in 2024 relative to the total for each age bracket
merged_data['Percentage'] = (merged_data['voted_2024'] / merged_data['Total']) * 100

# Create an interactive bar chart using Plotly
fig = px.bar(
    merged_data,
    x='age_bracket',
    y='Percentage',
    color='Gender',
    title='Male REP Voter Turnout Higher in Majority of Age Groups',
    labels={'Percentage': 'Percentage of Votes', 'age_bracket': 'Age Group'},
    hover_data={
        'Percentage': ':.2f',  # Format percentage to two decimal places
        'voted_2024': ':.0f',  # Include total votes in hover data, formatted as integer
    },
    barmode='group',  # Group bars for comparison
    color_discrete_map={'Female': 'pink', 'Male': 'blue'}  # Custom color palette
)

# Update layout for better aesthetics
fig.update_layout(
    xaxis_title='Age Group',
    yaxis_title='Percentage of Votes',
    xaxis_tickangle=-45
)

# Display the figure
fig.show()