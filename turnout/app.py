import csv
from flask import Flask
from flask import request
from flask import render_template
from peewee import *

app = Flask(__name__)

db = SqliteDatabase('turnout.db')

class CountyTurnout(Model):
    county = CharField(column_name='County')
    democrat_diff = DoubleField(column_name='democrat_diff')
    republican_diff = DoubleField(column_name='republican_diff')
    green_diff = DoubleField(column_name='green_diff')
    libertarian_diff = DoubleField(column_name='libertarian_diff')
    unaffiliated_diff = DoubleField(column_name='unaffiliated_diff')
    other_diff = DoubleField(column_name='other_diff')
    statewide_diff = DoubleField(column_name='statewide_diff')

    class Meta:
        table_name = "turnout_changes"
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

class EligibleInactiveDifferences(Model):
    county = CharField(column_name='county')
    democrat_diff = IntegerField(column_name='democrat_diff')
    republican_diff = IntegerField(column_name='republican_diff')
    green_diff = IntegerField(column_name='green_diff', null=True)
    libertarian_diff = IntegerField(column_name='libertarian_diff')
    unaffiliated_diff = IntegerField(column_name='unaffiliated_diff')
    other_diff = IntegerField(column_name='other_diff')
    
    class Meta:
        table_name = "inactivity_differences"
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

class EligibleActiveDifferences(Model):
    county = CharField(column_name='County')
    democrat_diff = IntegerField(column_name='democrat_diff')
    republican_diff = IntegerField(column_name='republican_diff')
    green_diff = IntegerField(column_name='green_diff')
    libertarian_diff = IntegerField(column_name='libertarian_diff')
    unaffiliated_diff = IntegerField(column_name='unaffiliated_diff')
    other_diff = IntegerField(column_name='other_diff')
    
    class Meta:
        table_name = "activity_differences"
        database = db
        primary_key = False

@app.route("/")
def index():
    template = 'index.html'
    return render_template(template)

@app.route("/official-turnout")
def official_turnout():
    object_list = CountyTurnout.select()
    template = 'official_turnout.html'
    
    return render_template(template, object_list=object_list)
    
@app.route("/eligible-inactive")
def eligible_inactive():
    template = 'eligible_inactive.html'

    object_list = EligibleInactiveDifferences.select()

    graph_query = EligibleInactiveDifferences.select()
    graph_data = [
        {
            "county": row.county,
            "democrat_diff": row.democrat_diff,
            "republican_diff": row.republican_diff,
            "green_diff": row.green_diff,
            "libertarian_diff": row.libertarian_diff,
            "unaffiliated_diff": row.unaffiliated_diff,
            "other_diff": row.other_diff
        }
        for row in graph_query
    ]
    
    return render_template(template, object_list=object_list, graph_data=graph_data)

@app.route("/eligible-active")
def eligible_active():
    template = 'eligible_active.html'
    
    object_list = EligibleActiveDifferences.select()

    graph_query = EligibleActiveDifferences.select()
    graph_data = [
        {
            "county": row.county,
            "democrat_diff": row.democrat_diff,
            "republican_diff": row.republican_diff,
            "green_diff": row.green_diff,
            "libertarian_diff": row.libertarian_diff,
            "unaffiliated_diff": row.unaffiliated_diff,
            "other_diff": row.other_diff
        }
        for row in graph_query
    ]

    return render_template(template, object_list=object_list, graph_data=graph_data)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)