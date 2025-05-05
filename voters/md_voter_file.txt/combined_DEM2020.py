import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Filter the data for Female Democrats (DEM) and Male Democrats (DEM)
female_dem_df = df[(df['Gender'] == 'Female') & (df['Party'] == 'DEM')]
male_dem_df = df[(df['Gender'] == 'Male') & (df['Party'] == 'DEM')]

# Group the data by age bracket and sum the counts for voted_2020
female_age_bracket_voted_2020 = female_dem_df.groupby('age_bracket')['voted_2020'].sum().reset_index()
male_age_bracket_voted_2020 = male_dem_df.groupby('age_bracket')['voted_2020'].sum().reset_index()

# Add a column to identify the gender
female_age_bracket_voted_2020['Gender'] = 'Female'
male_age_bracket_voted_2020['Gender'] = 'Male'

# Combine the data for both genders
combined_voted_2020 = pd.concat([female_age_bracket_voted_2020, male_age_bracket_voted_2020])

# Calculate total counts for each age bracket across all genders and parties for comparison
total_counts = df.groupby('age_bracket')['Count'].sum().reset_index()
total_counts.rename(columns={'Count': 'Total'}, inplace=True)

# Merge total counts with the combined DEM data
merged_data = pd.merge(combined_voted_2020, total_counts, on='age_bracket')

# Calculate the percentage of voters who voted in 2020 relative to the total for each age bracket
merged_data['Percentage'] = (merged_data['voted_2020'] / merged_data['Total']) * 100

# Create an interactive bar chart using Plotly
fig = px.bar(
    merged_data,
    x='age_bracket',
    y='Percentage',
    color='Gender',
    title='Combined Female and Male DEM Voter Participation in 2020 by Age Group',
    labels={'Percentage': 'Percentage of Votes', 'age_bracket': 'Age Group'},
    hover_data={
        'Percentage': ':.2f',  # Format percentage to two decimal places
        'voted_2020': ':.0f',  # Include total votes in hover data, formatted as integer
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