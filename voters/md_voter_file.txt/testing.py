import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('agg_MD.csv')  # Make sure the file path is correct

# Print column names to verify
print("Column names:", df.columns)

# Filter the data for Female Republicans (REP) if columns are verified
if 'Gender' in df.columns and 'Party' in df.columns:
    female_rep_df = df[(df['Gender'] == 'Female') & (df['Party'] == 'REP')]
    # Calculate the total number of voters who voted in 2020
    total_voted_2020 = female_rep_df['voted_2020'].sum()
    # Display the total number
    print("Total number of Female Republicans who voted in 2020:", total_voted_2020)
else:
    print("Column names are incorrect. Please verify the data.")