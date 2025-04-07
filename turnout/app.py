import csv
from flask import Flask
from flask import render_template
from peewee import *
app = Flask(__name__)

db = SqliteDatabase('turnout.db')

class OfficialTurnout(Model):
    county = CharField()
    election_day = IntegerField()
    early_voting = IntegerField()
    vote_by_mail = IntegerField()
    provisional = IntegerField()
    eligible_voters = IntegerField()
    turnout_percent = DoubleField()
    party = CharField()
    year = IntegerField()

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
    return render_template(template, object_list=object_list)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)
