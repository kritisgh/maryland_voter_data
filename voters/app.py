import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Load the dataset.
df = pd.read_csv("md_voter_file.txt/agg_MD_noGenderSplit_County.csv")
df['County'] = df['County'].str.replace("Saint Mary's", "St. Mary's", regex=False)

# Convert voted_2024 to numeric (this is critical if the column is read as strings)
df['voted_2024'] = pd.to_numeric(df['voted_2024'], errors='coerce')

# Remove rows missing critical data.
df = df.dropna(subset=['County', 'age_bracket', 'Party', 'voted_2024'])

# Get a sorted list of unique counties for the dropdown menu.
counties = sorted(df['County'].unique())

def get_bracket_lower(bracket):
    """
    Extract the lower bound from a given age_bracket string.
    e.g., '18-24' returns 18 as an integer.
    """
    try:
        return int(bracket.split('-')[0])
    except Exception:
        return float('inf')

@app.route("/")
def index():
    return render_template("index.html", counties=counties)
@app.route("/gender")
def gender():
    # pass in any data your gender page needs
    return render_template("gender.html")

@app.route("/nonvoters")
def nonvoters():
    # pass in any data your nonvoters page needs
    return render_template("nonvoters.html")

@app.route("/data/<county>")
def county_data(county):
    # Filter the data for the selected county.
    county_df = df[df['County'] == county].copy()
    
    # Sort by age_bracket using the lower bound of the bracket.
    county_df['bracket_order'] = county_df['age_bracket'].apply(get_bracket_lower)
    county_df = county_df.sort_values("bracket_order")
    
    # Use pivot_table instead of pivot to aggregate duplicate rows by summing.
    pivot_df = county_df.pivot_table(
        index="age_bracket",
        columns="Party",
        values="voted_2024",
        aggfunc='sum'
    )
    
    # Fill NaNs with zeros.
    pivot_df = pivot_df.fillna(0)
    
    # Calculate total votes for each age bracket.
    pivot_df['total'] = pivot_df.sum(axis=1)
    
    # Calculate percentages for each party:
    if "DEM" in pivot_df.columns:
        pivot_df["Dem_pct"] = (pivot_df["DEM"] / pivot_df["total"]) * 100
    else:
        pivot_df["Dem_pct"] = 0
    if "REP" in pivot_df.columns:
        pivot_df["Rep_pct"] = (pivot_df["REP"] / pivot_df["total"]) * 100
    else:
        pivot_df["Rep_pct"] = 0
    if "UNA" in pivot_df.columns:
        pivot_df["Unaffiliated_pct"] = (pivot_df["UNA"] / pivot_df["total"]) * 100
    else:
        pivot_df["Unaffiliated_pct"] = 0
    if "OTH" in pivot_df.columns:
        pivot_df["Oth_pct"] = (pivot_df["OTH"] / pivot_df["total"]) * 100
    else:
        pivot_df["Oth_pct"] = 0

    # Reset the index so that age_bracket becomes a column.
    pivot_df.reset_index(inplace=True)

    # Prepare the lists for JSON output.
    age_brackets = pivot_df["age_bracket"].tolist()
    dem_pct = pivot_df["Dem_pct"].tolist()
    rep_pct = pivot_df["Rep_pct"].tolist()
    unaffiliated_pct = pivot_df["Unaffiliated_pct"].tolist()
    other_pct = pivot_df["Oth_pct"].tolist()
    
    return jsonify({
        "ages": age_brackets,
        "dem": dem_pct,
        "rep": rep_pct,
        "other": other_pct,
        "unaffiliated": unaffiliated_pct
    })

if __name__ == "__main__":
    app.run(debug=True)
