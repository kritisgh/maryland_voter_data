from app import app, counties, counties2020           # imports from your existing app
from flask_frozen import Freezer

app.config.update(
    FREEZER_RELATIVE_URLS = True,   # erase the leading “/”
    FREEZER_DESTINATION   = 'build' # just to be explicit
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
def plot_gender():
    # /plot_gender?county=…&party=…
    parties = ['ALL', 'DEM', 'REP', 'UNA']
    for c in ['Statewide', *counties]:
        for p in parties:
            yield {'county': c, 'party': p}           # query-string params

@freezer.register_generator
def summary():
    # /summary/<county>   (if you decide to freeze these too)
    from app import summary_map
    for c in summary_map.keys():
        yield 'summary', {'county': c}

# ------------- run -------------
if __name__ == '__main__':
    freezer.freeze()          # writes everything into build/
