import pandas as pd

# Load the CSV
df = pd.read_csv("registration/static/annual_bycounty_with_cycles.csv")

# Ensure year is numeric
df['year'] = pd.to_numeric(df['year'])

# Create a label for the election cycle (e.g. 2008, 2012, etc.)
df['election_cycle'] = df['year'] - df['election_cycle_year'] + 1

# Pivot so that each row = one county + one election cycle
pivot = df.pivot_table(
    index=['county', 'election_cycle'],
    columns='election_cycle_year',
    values='total',
    aggfunc='sum'  # Just in case there's overlap
).reset_index()

# Rename columns
pivot.columns.name = None
pivot = pivot.rename(columns={
    1: 'Year 1',
    2: 'Year 2',
    3: 'Year 3',
    4: 'Year 4'
})

# Sort for clean output
pivot = pivot.sort_values(by=['county', 'election_cycle'])

# Save to CSV
pivot.to_csv("registration/static/datawrapper_allcounties_multiline.csv", index=False)

print("📊 Saved: registration/static/datawrapper_allcounties_multiline.csv — ready for Datawrapper!")
