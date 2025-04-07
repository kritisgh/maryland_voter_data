import csv
from flask import Flask
from flask import render_template
from peewee import *
app = Flask(__name__)

db = SqliteDatabase('turnout.db')

class OfficialTurnout(Model):
    county = CharField(column_name=' County')
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

def get_csv():
    csv_path = './static/official_by_party_and_county_complete.csv'
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

@app.route("/")
def index():
    template = 'index.html'
    object_list = get_csv()
    allegany_turnout = OfficialTurnout.select().where(OfficialTurnout.county=='Allegany')
    for turnout in allegany_turnout:
        print(turnout.provisional)
    return render_template(template, object_list=object_list)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)
