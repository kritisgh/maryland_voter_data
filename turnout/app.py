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

class EligibleInactiveDifferences(Model):
    county = CharField(column_name='county')
    democrat_diff = DoubleField(column_name='democrat_diff')
    republican_diff = DoubleField(column_name='republican_diff')
    green_diff = DoubleField(column_name='green_diff', null=True)
    libertarian_diff = DoubleField(column_name='libertarian_diff')
    unaffiliated_diff = DoubleField(column_name='unaffiliated_diff')
    other_diff = DoubleField(column_name='other_diff')
    
    class Meta:
        table_name = "inactivity_differences"
        database = db
        primary_key = False


class EligibleActiveDifferences(Model):
    county = CharField(column_name='County')
    democrat_diff = DoubleField(column_name='democrat_diff')
    republican_diff = DoubleField(column_name='republican_diff')
    green_diff = DoubleField(column_name='green_diff', null=True)
    libertarian_diff = DoubleField(column_name='libertarian_diff')
    unaffiliated_diff = DoubleField(column_name='unaffiliated_diff')
    other_diff = DoubleField(column_name='other_diff')
    
    class Meta:
        table_name = "activity_differences"
        database = db
        primary_key = False

@app.route("/")
def index():
    template = 'index.html'
    return render_template(template)

@app.route("/county")
def county_dashboard():
    template = 'county.html'
    
    try: 
        official_query = CountyTurnout.select()
        active_query = EligibleActiveDifferences.select()
        inactive_query = EligibleInactiveDifferences.select()
        
        official_data = [
            {
                "county": row.county,
                "democrat_diff": row.democrat_diff,
                "republican_diff": row.republican_diff,
                "green_diff": row.green_diff,
                "libertarian_diff": row.libertarian_diff,
                "unaffiliated_diff": row.unaffiliated_diff,
                "other_diff": row.other_diff,
                "statewide_diff": row.statewide_diff
            }
            for row in official_query
        ]
        
        active_data = [
            {
                "county": row.county,
                "democrat_diff": row.democrat_diff,
                "republican_diff": row.republican_diff,
                "green_diff": row.green_diff,
                "libertarian_diff": row.libertarian_diff,
                "unaffiliated_diff": row.unaffiliated_diff,
                "other_diff": row.other_diff
            }
            for row in active_query
        ]
        
        inactive_data = [
            {
                "county": row.county,
                "democrat_diff": row.democrat_diff,
                "republican_diff": row.republican_diff,
                "green_diff": row.green_diff if hasattr(row, 'green_diff') else 0,
                "libertarian_diff": row.libertarian_diff,
                "unaffiliated_diff": row.unaffiliated_diff,
                "other_diff": row.other_diff
            }
            for row in inactive_query
        ]
        
        counties = sorted(list(set(row.county for row in official_query)))
        
        return render_template(
            template,
            officialTurnoutData=official_data,
            activeVotersData=active_data,
            inactiveVotersData=inactive_data,
            counties=counties
        )
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return render_template(
            template,
            officialTurnoutData=[],
            activeVotersData=[],
            inactiveVotersData=[],
            counties=[]
        )

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

@app.route("/dumbbell")
def dumbbell_chart():
    return render_template("dumbbell.html")

@app.route("/bubble")
def bubble_chart():
    return render_template("bubble.html")


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