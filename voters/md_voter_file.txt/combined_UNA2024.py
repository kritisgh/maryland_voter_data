import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Filter for Male UNA voters who voted in 2024
male_una_data = df[
    (df['Gender'] == 'Male') & 
    (df['Party'] == 'UNA') & 
    (df['voted_2024'] > 0)
]

# Filter for Female UNA voters who voted in 2024
female_una_data = df[
    (df['Gender'] == 'Female') & 
    (df['Party'] == 'UNA') & 
    (df['voted_2024'] > 0)
]

# Group the data by age bracket and sum the counts for Male
male_grouped_df = male_una_data.groupby('age_bracket').sum().reset_index()
male_total_counts = df.groupby('age_bracket')['Count'].sum().reset_index()
male_total_counts.rename(columns={'Count': 'Total'}, inplace=True)
male_merged_df = pd.merge(male_grouped_df, male_total_counts, on='age_bracket')
male_merged_df['Percentage'] = (male_merged_df['Count'] / male_merged_df['Total']) * 100

# Group the data by age bracket and sum the counts for Female
female_grouped_df = female_una_data.groupby('age_bracket').sum().reset_index()
female_total_counts = df.groupby('age_bracket')['Count'].sum().reset_index()
female_total_counts.rename(columns={'Count': 'Total'}, inplace=True)
female_merged_df = pd.merge(female_grouped_df, female_total_counts, on='age_bracket')
female_merged_df['Percentage'] = (female_merged_df['Count'] / female_merged_df['Total']) * 100

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
    title='Male Unaffiliated Voter Turnout Higher than Female throughout all Age Groups',
    labels={'Percentage': 'Percentage of Votes', 'age_bracket': 'Age Group'},
    hover_data={
        'Percentage': ':.2f',  # Format percentage to two decimal places
        'Total': ':.0f',  # Include total count in hover data, formatted as integer
        'Count': ':.0f'  # Include the count of votes in hover data
    },
    color_discrete_map={'Male': 'lightblue', 'Female': 'pink'}  # Set custom colors
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