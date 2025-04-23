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
    year = IntegerField(column_name='Year')

    class Meta:
        table_name = "eligible_inactive"
        database = db
        primary_key = False

class EligibleInactiveCalculations(Model):
    county = CharField(column_name='County')
    democrat_diff = IntegerField(column_name='Democrat_Diff')
    republican_diff = IntegerField(column_name='Republican_Diff')
    bread_and_roses_diff = IntegerField(column_name='Bread_and_Roses_Diff')
    green_diff = IntegerField(column_name='Green_Diff')
    libertarian_diff = IntegerField(column_name='Libertarian_Diff')
    working_class_party_diff = IntegerField(column_name='Working_Class_Party_Diff')
    no_labels_maryland_diff = IntegerField(column_name='No_Labels_Maryland_Diff')
    other_diff = IntegerField(column_name='Other_Diff')
    unaffiliated_diff = IntegerField(column_name='Unaffiliated_Diff')

    class Meta:
        table_name = "eligible_inactive_calculations"
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
    year = IntegerField(column_name='Year')

    class Meta:
        table_name = "eligible_active"
        database = db
        primary_key = False

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
    
    return render_template(template, object_list=object_list)
    
@app.route("/eligible-inactive")
def eligible_inactive():
    template = 'eligible_inactive.html'

    object_list = EligibleInactive.select()

    graph_query = EligibleInactiveCalculations.select()
    graph_data = [
        {
            "county": row.county,
            "democrat_diff": row.democrat_diff,
            "republican_diff": row.republican_diff,
            "bread_and_roses_diff": row.bread_and_roses_diff,
            "green_diff": row.green_diff,
            "libertarian_diff": row.libertarian_diff,
            "working_class_party_diff": row.working_class_party_diff,
            "no_labels_maryland_diff": row.no_labels_maryland_diff,
            "unaffiliated_diff": row.unaffiliated_diff,
            "other_diff": row.other_diff
        }
        for row in graph_query
    ]

    return render_template(template, object_list=object_list, graph_data=graph_data)

@app.route("/eligible-active")
def eligible_active():
    template = 'eligible_active.html'
    
    object_list = EligibleActive.select()
    
    return render_template(template, object_list=object_list)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)