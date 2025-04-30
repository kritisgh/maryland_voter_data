import pandas as pd
import plotly.express as px
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Load the dataset.
df = pd.read_csv("md_voter_file.txt/agg_MD_noGenderSplit_County.csv")
df['County'] = df['County'].str.replace("Saint Mary's", "St. Mary's", regex=False)

# Convert voted_2024 to numeric (this is critical if the column is read as strings)
df['voted_2024'] = pd.to_numeric(df['voted_2024'], errors='coerce')

# Remove rows missing critical data.
df = df.dropna(subset=['County', 'age_bracket', 'Party', 'voted_2024'])
countyTotals = df.groupby('County')['voted_2024'].sum().to_dict()
# Get a sorted list of unique counties for the dropdown menu.
counties = sorted(df['County'].unique())
turnout_df = pd.read_csv("md_voter_file.txt/county x 100.csv")
turnout_df['County'] = turnout_df['County'].str.replace("Saint Mary's", "St. Mary's", regex=False)

party_averages = {
    'DEM': dict(zip(turnout_df['County'], turnout_df['DEM'])),
    'REP': dict(zip(turnout_df['County'], turnout_df['REP'])),
    'UNA': dict(zip(turnout_df['County'], turnout_df['UNA']))
}

# Compute min/max for each party
party_ranges = {
    party: {
        'min': min(avgs.values()),
        'max': max(avgs.values())
    }
    for (party, avgs) in party_averages.items()
}

statewide_df = pd.read_csv("md_voter_file.txt/statewide_2024.csv")
# convert fraction→percent
statewide_df['turnout_pct'] = statewide_df['turnout'] * 100
# build Party → % dict
statewideAverages = dict(zip(statewide_df['Party'], statewide_df['turnout_pct']))

def get_bracket_lower(bracket):
    """
    Extract the lower bound from a given age_bracket string.
    e.g., '18-24' returns 18 as an integer.
    """
    try:
        return int(bracket.split('-')[0])
    except Exception:
        return float('inf')
def create_graphs(gender_label):
    # load and group the data (same as in your male_*.py / female_*.py scripts) :contentReference[oaicite:0]{index=0}
    df = pd.read_csv('md_voter_file.txt/agg_MD.csv')
    grouped = df.groupby(['age_bracket', 'Gender', 'Party']).sum().reset_index()
    total = (grouped
             .groupby('age_bracket')['Count']
             .sum()
             .reset_index()
             .rename(columns={'Count':'Total'}))

    graphs = {}
    for party in ['DEM','REP','UNA']:
        sub = grouped[
            (grouped['Gender'] == gender_label) &
            (grouped['Party'] == party)
        ]
        merged = pd.merge(sub, total, on='age_bracket')
        merged['Percentage'] = merged['Count'] / merged['Total'] * 100

        # build figure
        fig = px.bar(
            merged,
            x='age_bracket',
            y='Percentage',
            title=f'{gender_label} {party} Participation by Age',
            labels={'age_bracket': 'Age Group','Percentage':'%'},
            hover_data={'Percentage':':.2f','Total':':.0f'},
            color='age_bracket'
        )
        # rotate labels
        fig.update_layout(xaxis_tickangle=-45)

        # <<< add these three lines >>>
        fig.update_layout(bargap=0.2, bargroupgap=0.1)
        fig.update_traces(width=0.6)

        # grab just the div+js (we'll include plotly.js once in the template)
        graphs[party.lower()] = fig.to_html(full_html=False, include_plotlyjs=False)

    return graphs

@app.route("/")
def index():
    return render_template("index.html", counties=counties)

@app.route("/election_2024")
def election_2024():
    return render_template(
        "election_2024.html",
        counties=counties,
        partyAverages=party_averages,
        partyRanges=party_ranges,
        statewideAverages=statewideAverages,
        countyTotals=countyTotals
    )

@app.route('/gender')
def gender():
    male_graphs   = create_graphs('Male')
    female_graphs = create_graphs('Female')
    return render_template(
        'gender.html',
        male_graphs=male_graphs,
        female_graphs=female_graphs
    )

@app.route("/nonvoters")
def nonvoters():
    # pass in any data your nonvoters page needs
    return render_template("nonvoters.html", counties=counties)



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
