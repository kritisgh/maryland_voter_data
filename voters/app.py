import pandas as pd
import plotly.express as px
from flask import Flask, render_template, jsonify, request
import json
import os, re                                   #  <-- NEW
import plotly.io as pio                          #  <-- already have plotly.express

    
app = Flask(__name__)
PLOTS_DIR = os.path.join(app.root_path, "static", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)   
# Load the dataset.
df = pd.read_csv("md_voter_file.txt/agg_MD_noGenderSplit_County.csv")
df['County'] = df['County'].str.replace("Saint Mary's", "St. Mary's", regex=False)
df['voted_2024'] = pd.to_numeric(df['voted_2024'], errors='coerce')
df['Count']     = pd.to_numeric(df['Count'],     errors='coerce')

df_gender = pd.read_csv('md_voter_file.txt/agg_MD_GenderSplit_County.csv')
df_gender['County'] = df_gender['County'].str.replace("Saint Mary's", "St. Mary's", regex=False)
df_gender['turnout'] = df_gender['voted_2024'] / df_gender['Count'] * 100

# list of counties for dropdown
counties = sorted(df_gender['County'].unique())


df2020 = pd.read_csv("md_voter_file.txt/agg_MD_noGenderSplit_County.csv")
df2020['County'] = df2020['County'].str.replace("Saint Mary's", "St. Mary's", regex=False)
df2020['voted_2020'] = pd.to_numeric(df2020['voted_2020'], errors='coerce')
df2020 = df2020.dropna(subset=['County', 'age_bracket', 'Party', 'voted_2020'])

turnout2020 = pd.read_csv("md_voter_file.txt/county x 100_2020.csv")
turnout2020['County'] = turnout2020['County'].str.replace("Saint Mary's", "St. Mary's", regex=False)

statewide2020 = pd.read_csv("md_voter_file.txt/statewide_2020.csv")
statewide2020['turnout_pct'] = statewide2020['turnout'] * 100

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
countyTotals2020 = df2020.groupby('County')['voted_2020'].sum().to_dict()

# partyAverages for 2020
party_averages_2020 = {
    'DEM': dict(zip(turnout2020['County'], turnout2020['DEM'])),
    'REP': dict(zip(turnout2020['County'], turnout2020['REP'])),
    'UNA': dict(zip(turnout2020['County'], turnout2020['UNA']))
}
# partyRanges for 2020
party_ranges_2020 = {
    p: {'min': min(vals.values()), 'max': max(vals.values())}
    for p, vals in party_averages_2020.items()
}

# statewideAverages for 2020
statewideAverages2020 = dict(zip(statewide2020['Party'], statewide2020['turnout_pct']))

# sorted county list
counties2020 = sorted(df2020['County'].unique())
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
@app.route("/election_2020")
def election_2020():
    return render_template(
        "election_2020.html",
        counties=counties2020,
        partyAverages=party_averages_2020,
        partyRanges=party_ranges_2020,
        statewideAverages=statewideAverages2020,
        countyTotals=countyTotals2020
    )

@app.route('/gender')
def gender():
    return render_template(
        'gender.html',
        counties=['Statewide'] + counties)
    

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
@app.route("/data2020/<county>")
def county_data_2020(county):
    sub = df2020[df2020['County']==county].copy()
    sub['bracket_order'] = sub['age_bracket'].apply(get_bracket_lower)
    sub = sub.sort_values("bracket_order")
    pivot = sub.pivot_table(
        index="age_bracket",
        columns="Party",
        values="voted_2020",
        aggfunc='sum'
    ).fillna(0)
    pivot['total'] = pivot.sum(axis=1)
    pivot["Dem_pct"] = pivot.get("DEM",0) / pivot['total'] * 100
    pivot["Rep_pct"] = pivot.get("REP",0) / pivot['total'] * 100
    pivot["Unaffiliated_pct"] = pivot.get("UNA",0) / pivot['total'] * 100
    pivot["Oth_pct"] = pivot.get("OTH",0) / pivot['total'] * 100
    pivot.reset_index(inplace=True)

    return jsonify({
        "ages": pivot["age_bracket"].tolist(),
        "dem": pivot["Dem_pct"].tolist(),
        "rep": pivot["Rep_pct"].tolist(),
        "unaffiliated": pivot["Unaffiliated_pct"].tolist(),
        "other": pivot["Oth_pct"].tolist()
    })
@app.route('/plot_gender')
def plot_gender():
    county = request.args.get('county', 'Statewide')
    party  = request.args.get('party', 'ALL')

    # --- your existing filtering & summary code unchanged ---
    if county != 'Statewide':
        dff = df_gender[df_gender['County'] == county]
    else:
        dff = df_gender

    if party != 'ALL':
        dff = dff[dff['Party'] == party]

    summary = (
        dff
        .groupby(['age_bracket','Gender'])
        .agg({'voted_2024':'sum','Count':'sum'})
        .reset_index()
    )
    summary['turnout'] = summary['voted_2024'] / summary['Count'] * 100

    party_names = {
        'ALL': 'All Parties',
        'DEM': 'Democrats',
        'REP': 'Republicans',
        'UNA': 'Unaffiliated'
    }

    # 1) Define your custom statewide titles
    statewide_titles = {
        'ALL': 'Statewide Female Voter Turnout is Higher than Male Turnout in 2024',
        'DEM': 'Female Democratic Voter Turnout is Significantly Higher Compared to Male Turnout Among all Age Groups in 2024',
        'REP': 'Male Republican Voter Turnout is Higher than Female Turnout in Majority of Age Groups in 2024',
        'UNA': 'Young Male Unaffiliated Voter Turnout Lower than Young Female Turnout'
    }

    # 2) Build the bar chart (we’ll override the title just below)
    fig = px.bar(
        summary,
        x='age_bracket',
        y='turnout',
        color='Gender',
        barmode='group',
        labels={'age_bracket':'Age Bracket','turnout':'Turnout %'},
        # you can leave title blank here since we'll set it explicitly
        title='',
        category_orders={'Gender': ['Male','Female']},
        color_discrete_map={'Male':'#1FC3AA','Female':'#DBA3FD'},
        text='turnout',
        custom_data=['Gender']
    )
    fig.update_traces(
        texttemplate='%{customdata[0]}: <br>%{text:.2f}%',
        textposition='inside',
        textfont_color='white',
        insidetextanchor='middle'
    )

    # 3) Override the title based on county vs statewide
    if county == 'Statewide':
        # use one of your four special statewide titles
        fig.update_layout(
            title=statewide_titles[party]
        )
    else:
        # append " County" to every county except Baltimore City & Baltimore County
        if county not in ['Baltimore County', 'Baltimore City'] \
           and not county.endswith('County'):
            display_name = f"{county} County"
        else:
            display_name = county

        fig.update_layout(
            title=f"{party_names[party]} Turnout in 2024 – {display_name}"
        )

    # ---------- save a copy ----------
    # build a clean file name like  "Allegany_All-Parties.png"
    clean_county = re.sub(r"[^\w\-]", "_", county)        # keep letters, numbers, _
    party_label  = party_names[party].replace(" ", "-")    # e.g. "All-Parties"
    fname        = f"{clean_county}_{party_label}.png"
    out_path     = os.path.join(PLOTS_DIR, fname)

    # choose whatever size you like
    fig.write_image(out_path, width=1200, height=700, scale=2)  # needs kaleido
    # ----------------------------------
    # 4) Return as before
    return jsonify(json.loads(fig.to_json()))

if __name__ == "__main__":
    app.run(debug=True)
