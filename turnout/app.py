import csv
from flask import Flask
from flask import request
from flask import render_template
from peewee import *

app = Flask(__name__)

db = SqliteDatabase('turnout.db')

class OfficialTurnout(Model):
    county = CharField(column_name='County')
    election_day = IntegerField(column_name='Election Day')
    early_voting = IntegerField(column_name='Early Voting')
    vote_by_mail = IntegerField(column_name='Vote By Mail')
    provisional = IntegerField(column_name='Provisional')
    eligible_voters = IntegerField(column_name='Eligible Voters')
    turnout_percent = DoubleField(column_name='Turnout Percentage')
    party = CharField(column_name='Party')
    year = IntegerField(column_name='Year')

    class Meta:
        table_name = "official_turnout"
        database = db
        primary_key = False

class EligibleInactive(Model):
    county = CharField(column_name='County')
    democrat_inactive = IntegerField(column_name='Democrat')
    republican_inactive = IntegerField(column_name='Republican')
    bread_and_roses_inactive = IntegerField(column_name='Bread and Roses')
    green_inactive = IntegerField(column_name='Green')
    libertarian_inactive = IntegerField(column_name='Libertarian')
    working_class_inactive = IntegerField(column_name='Working Class Party')
    other_inactive = IntegerField(column_name='Other')
    unaffiliated_inactive = IntegerField(column_name='Unaffiliated')
    no_labels_inactive = IntegerField(column_name='No Labels Maryland')
    year_inactive = IntegerField(column_name='Year')

    class Meta:
        table_name = "eligible_inactive"
        database = db
        primary_key = False

class EligibleActive(Model):
    county = CharField(column_name='County')
    democrat_active = IntegerField(column_name='Democrat')
    republican_active = IntegerField(column_name='Republican')
    bread_and_roses_active = IntegerField(column_name='Bread and Roses')
    green_active = IntegerField(column_name='Green')
    libertarian_active = IntegerField(column_name='Libertarian')
    working_class_active = IntegerField(column_name='Working Class Party')
    other_active = IntegerField(column_name='Other')
    unaffiliated_active = IntegerField(column_name='Unaffiliated')
    no_labels_active = IntegerField(column_name='No Labels Maryland')
    year_active = IntegerField(column_name='Year')

    class Meta:
        table_name = "eligible_active"
        database = db
        primary_key = False

def paginate_by_year(data, year=None):
    # Extract all available years and sort them
    all_years = sorted(list(set(int(item['Year']) for item in data)))
    
    # If no year specified, use the first year
    if year is None and all_years:
        year = all_years[0]
    
    # Filter data by selected year
    year_data = [item for item in data if int(item['Year']) == year]
    
    # Find previous and next years
    if year in all_years:
        current_year_index = all_years.index(year)
        prev_year = all_years[current_year_index - 1] if current_year_index > 0 else None
        next_year = all_years[current_year_index + 1] if current_year_index < len(all_years) - 1 else None
    else:
        prev_year = None
        next_year = None
    
    return {
        'data': year_data,
        'year': year,
        'all_years': all_years,
        'has_prev': prev_year is not None,
        'has_next': next_year is not None,
        'prev_year': prev_year,
        'next_year': next_year
    }

@app.route("/")
def index():
    template = 'index.html'
    return render_template(template)

@app.route("/official-turnout")
def official_turnout():
    object_list = OfficialTurnout.select(
        OfficialTurnout.county,
        OfficialTurnout.election_day,
        OfficialTurnout.early_voting,
        OfficialTurnout.vote_by_mail,
        OfficialTurnout.provisional,
        OfficialTurnout.eligible_voters,
        OfficialTurnout.turnout_percent,
        OfficialTurnout.party,
        OfficialTurnout.year
    )
    template = 'official_turnout.html'
    
    # Get year parameter instead of page
    requested_year = request.args.get('year')
    if requested_year:
        requested_year = int(requested_year)
    
    object_list = get_official_turnout_csv()
    paginated = paginate_by_year(object_list, requested_year)
    
    return render_template(
        template,
        object_list=paginated['data'],
        year=paginated['year'],
        all_years=paginated['all_years'],
        has_prev=paginated['has_prev'],
        has_next=paginated['has_next'],
        prev_year=paginated['prev_year'],
        next_year=paginated['next_year']
    )
    
@app.route("/eligible-inactive")
def eligible_inactive():
    template = 'eligible_inactive.html'
    
    # Get year parameter instead of page
    requested_year = request.args.get('year')
    if requested_year:
        requested_year = int(requested_year)
    
    object_list = get_eligible_inactive_csv()
    paginated = paginate_by_year(object_list, requested_year)
    
    return render_template(
        template,
        object_list=paginated['data'],
        year=paginated['year'],
        all_years=paginated['all_years'],
        has_prev=paginated['has_prev'],
        has_next=paginated['has_next'],
        prev_year=paginated['prev_year'],
        next_year=paginated['next_year']
    )

@app.route("/eligible-active")
def eligible_active():
    template = 'eligible_active.html'
    
    # Get year parameter instead of page
    requested_year = request.args.get('year')
    if requested_year:
        requested_year = int(requested_year)
    
    object_list = get_eligible_active_csv()
    paginated = paginate_by_year(object_list, requested_year)
    
    return render_template(
        template,
        object_list=paginated['data'],
        year=paginated['year'],
        all_years=paginated['all_years'],
        has_prev=paginated['has_prev'],
        has_next=paginated['has_next'],
        prev_year=paginated['prev_year'],
        next_year=paginated['next_year']
    )

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)