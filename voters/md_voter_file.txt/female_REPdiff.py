import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')

# Filter the data for Female Republicans (REP)
female_rep_df = df[(df['Gender'] == 'Female') & (df['Party'] == 'REP')]

# Group the data by age bracket and sum the counts for voted_2024 and voted_2020
age_bracket_votes = female_rep_df.groupby('age_bracket')[['voted_2024', 'voted_2020']].sum().reset_index()

# Calculate the percentage of votes for 2024 and 2020
total_counts = female_rep_df.groupby('age_bracket')['Count'].sum().reset_index()
total_counts.rename(columns={'Count': 'Total'}, inplace=True)

# Merge total counts with the votes data
merged_data = pd.merge(age_bracket_votes, total_counts, on='age_bracket')

# Calculate percentages
merged_data['Percentage_Voted_2024'] = (merged_data['voted_2024'] / merged_data['Total']) * 100
merged_data['Percentage_Voted_2020'] = (merged_data['voted_2020'] / merged_data['Total']) * 100

# Calculate the percentage difference
merged_data['Percentage_Difference'] = merged_data['Percentage_Voted_2024'] - merged_data['Percentage_Voted_2020']

# Create an interactive bar chart using Plotly
fig = px.bar(
    merged_data,
    x='age_bracket',
    y='Percentage_Difference',
    title='Percentage Difference Between Voted 2024 and Voted 2020 for Female Republicans by Age Group',
    labels={'Percentage_Difference': 'Percentage Difference (Voted 2024 - Voted 2020)', 'age_bracket': 'Age Group'},
    hover_data={
        'Percentage_Difference': ':.2f',  # Format percentage difference to two decimal places
        'Percentage_Voted_2024': ':.2f',   # Include percentage for 2024 in hover data
        'Percentage_Voted_2020': ':.2f',   # Include percentage for 2020 in hover data
    },
    color_discrete_sequence=['#007BFF'],  # Set uniform color to medium blue
)

# Update layout for better aesthetics
fig.update_layout(
    xaxis_title='Age Group',
    yaxis_title='Percentage Difference (Voted 2024 - Voted 2020)',
    xaxis_tickangle=-45,
    yaxis=dict(range=[-5, 40]),  # Set y-axis range with minimum at -2100 and maximum at 15,000
)

# Show the interactive plot
fig.show()