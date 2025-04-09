from flask import Flask
from flask import render_template
from peewee import *
app = Flask(__name__)

db = SqliteDatabase('registration.db')

class Registration(Model):
    year = IntegerField()
    month = IntegerField()
    county = CharField()
    dem = IntegerField()
    rep = IntegerField()
    unaf = IntegerField()
    other = IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('year', 'month', 'county')

@app.route("/")
def index():
    counties = Registration.select(Registration.county).distinct().order_by(Registration.county)
    return render_template("index.html", counties=counties)

@app.route('/county/<slug>')
def county_detail(slug):
    county = slug
    records = Registration.select().where(Registration.county == county)
    total_dem = Registration.select(fn.SUM(Registration.dem)).where(Registration.county == county).scalar()
    total_rep = Registration.select(fn.SUM(Registration.rep)).where(Registration.county == county).scalar()
    total_unaf = Registration.select(fn.SUM(Registration.unaf)).where(Registration.county == county).scalar()
    total_other = Registration.select(fn.SUM(Registration.other)).where(Registration.county == county).scalar()

    return render_template(
        "county_detail.html",
        county=county,
        records=records,
        records_count=records.count(),
        total_dem=total_dem,
        total_rep=total_rep,
        total_unaf=total_unaf,
        total_other=total_other
    )

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
