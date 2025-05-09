from app import app, counties, counties2020           # imports from your existing app
from flask_frozen import Freezer

app.config.update(
    FREEZER_RELATIVE_URLS = True,   # keep links repo-relative
)

freezer = Freezer(app)

# ----  GENERATORS  ----
@freezer.register_generator
def county_data():
    # /data/<county>  JSON for 2024
    for c in counties:
        yield 'county_data', {'county': c}

@freezer.register_generator
def county_data_2020():
    # /data2020/<county>  JSON for 2020
    for c in counties2020:
        yield 'county_data_2020', {'county': c}

@freezer.register_generator
def summary():
    from app import summary_map            # same dict you already build
    for county in summary_map.keys():      # 'Statewide' is in there too
        yield 'summary', {'place': county}

@freezer.register_generator
def plot_gender():
    from app import counties               # list you already build
    parties = ['ALL', 'DEM', 'REP', 'UNA']
    for county in ['Statewide', *counties]:
        for p in parties:
            yield 'plot_gender', {'county': county, 'party': p}


# ------------- run -------------
if __name__ == '__main__':
    freezer.freeze()          # writes everything into build/
