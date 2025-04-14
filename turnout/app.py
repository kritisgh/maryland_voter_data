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
        table_name = "eligible_inactive"
        database = db
        primary_key = False

def paginate(data, page=1, per_page=20):
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]

    return {
        'data': paginated_data,
        'total': total,
        'page': page,
        'per_page': per_page,
        'has_prev': page > 1,
        'has_next': end < total,
        'prev_page': page - 1,
        'next_page': page + 1
    }

@app.route("/")
def index():
    template = 'index.html'
    return render_template(template)

def get_official_turnout_csv():
    csv_path = './static/official_by_party_and_county_complete.csv'
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

def get_eligible_inactive_csv():
    csv_path = './static/eligible_inactive.csv'
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list


def get_eligible_active_csv():
    csv_path = './static/eligible_active.csv'
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

@app.route("/official-turnout")
def official_turnout():
    template = 'official_turnout.html'
    page = int(request.args.get('page', 1))
    object_list = get_official_turnout_csv()
    paginated = paginate(object_list, page, per_page=20)
    return render_template(
        template,
        object_list=paginated['data'],
        page=paginated['page'],
        has_prev=paginated['has_prev'],
        has_next=paginated['has_next'],
        prev_page=paginated['prev_page'],
        next_page=paginated['next_page']
    )

@app.route("/eligible-inactive")
def eligible_inactive():
    template = 'eligible_inactive.html'
    page = int(request.args.get('page', 1))
    object_list = get_eligible_inactive_csv()
    paginated = paginate(object_list, page, per_page=20)
    return render_template(
        template,
        object_list=paginated['data'],
        page=paginated['page'],
        has_prev=paginated['has_prev'],
        has_next=paginated['has_next'],
        prev_page=paginated['prev_page'],
        next_page=paginated['next_page']
    )

@app.route("/eligible-active")
def eligible_active():
    template = 'eligible_active.html'
    page = int(request.args.get('page', 1))
    object_list = get_eligible_active_csv()
    paginated = paginate(object_list, page, per_page=20)
    return render_template(
        template,
        object_list=paginated['data'],
        page=paginated['page'],
        has_prev=paginated['has_prev'],
        has_next=paginated['has_next'],
        prev_page=paginated['prev_page'],
        next_page=paginated['next_page']
    )

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)

