from flask import Flask
from flask import render_template
from flourish_id import flourish_ids
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
    embed_id = flourish_ids.get(county)
    year_summary = (
        Registration
        .select(
            fn.SUM(Registration.dem).alias('dem'),
            fn.SUM(Registration.rep).alias('rep'),
            fn.SUM(Registration.unaf).alias('unaf'),
            fn.SUM(Registration.other).alias('other')
        ).where((Registration.county == county) & (Registration.year == 2024)).dicts().get())
    historical_records = (Registration.select().where(Registration.county == county).order_by(Registration.year.desc(), Registration.month.desc()))
    counties = Registration.select(Registration.county).distinct().order_by(Registration.county)
    return render_template(
        "county_detail.html",
        county=county,
        flourish_id=embed_id,
        year_summary=year_summary,
        records=historical_records,
        counties=counties
    )

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
