import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Filter for Democratic voters
dem_data = df[df['Party'] == 'DEM']

# Filter for Male Democratic voters
male_dem_data = dem_data[dem_data['Gender'] == 'Male']

# Filter for Female Democratic voters
female_dem_data = dem_data[dem_data['Gender'] == 'Female']

# Group the data by age bracket and sum the counts for voted_2024
male_grouped_df = male_dem_data.groupby('age_bracket').sum().reset_index()
female_grouped_df = female_dem_data.groupby('age_bracket').sum().reset_index()

# Calculate total counts for each age bracket across all Democratic voters
total_counts = dem_data.groupby('age_bracket')['Count'].sum().reset_index()
total_counts.rename(columns={'Count': 'Total'}, inplace=True)

# Merge total counts with the gender-specific data
male_merged_df = pd.merge(male_grouped_df, total_counts, on='age_bracket')
female_merged_df = pd.merge(female_grouped_df, total_counts, on='age_bracket')

# Calculate the percentage of voters who voted in 2024 relative to the total for each age bracket
male_merged_df['Percentage'] = (male_merged_df['voted_2024'] / male_merged_df['Total']) * 100
female_merged_df['Percentage'] = (female_merged_df['voted_2024'] / female_merged_df['Total']) * 100

# Combine both Male and Female data for plotting
combined_df = pd.concat([
    male_merged_df.assign(Gender='Male'),
    female_merged_df.assign(Gender='Female')
])

# Create an interactive bar chart using Plotly
fig = px.bar(
    combined_df, 
    x='age_bracket', 
    y='Percentage',
    color='Gender',  # Differentiate by Gender
    title='Female Democratic Voter Turnout Significantly Higher Versus Male Among all Age Groups',
    labels={'Percentage': 'Percentage of Votes', 'age_bracket': 'Age Group'},
    hover_data={
        'Percentage': ':.2f',  # Format percentage to two decimal places
        'Total': ':.0f',  # Include total count in hover data, formatted as integer
        'voted_2024': ':.0f'  # Include the count of votes in hover data
    },
    color_discrete_map={'Male': 'blue', 'Female': 'pink'}  # Set custom colors
)

# Update layout for better aesthetics
fig.update_layout(
    barmode='group',  # Set bars to be side by side
    xaxis_title='Age Group',
    yaxis_title='Percentage of Votes',
    xaxis_tickangle=-45
)

# Show the interactive plot
fig.show()