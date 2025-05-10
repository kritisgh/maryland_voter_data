from flask import Flask, render_template
from info import flourish_ids
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

def percent_change(new, old):
    try:
        return round(((new - old) / old) * 100, 1)
    except ZeroDivisionError:
        return 0

@app.route("/")
def index():
    counties = Registration.select(Registration.county).distinct().order_by(Registration.county)
    return render_template("index.html", counties=counties)

@app.route('/county/<slug>')
def county_detail(slug):
    county = slug
    embed_id = flourish_ids.get(county)
    image_path = f"images/{county}.png"
    

    year_summary = (
        Registration
        .select(
            fn.SUM(Registration.dem).alias('dem'),
            fn.SUM(Registration.rep).alias('rep'),
            fn.SUM(Registration.unaf).alias('unaf'),
            fn.SUM(Registration.other).alias('other')
        )
        .where((Registration.county == county) & (Registration.year == 2024))
        .dicts()
        .get()
    )

    year_2020 = (
        Registration
        .select(
            fn.SUM(Registration.dem).alias('dem'),
            fn.SUM(Registration.rep).alias('rep'),
            fn.SUM(Registration.unaf).alias('unaf'),
            fn.SUM(Registration.other).alias('other')
        )
        .where((Registration.county == county) & (Registration.year == 2020))
        .dicts()
        .get()
    )

    change = {
        "dem": percent_change(year_summary["dem"], year_2020["dem"]),
        "rep": percent_change(year_summary["rep"], year_2020["rep"]),
        "unaf": percent_change(year_summary["unaf"], year_2020["unaf"]),
        "other": percent_change(year_summary["other"], year_2020["other"]),
    }

    historical_records = (
        Registration
        .select()
        .where(Registration.county == county)
        .order_by(Registration.year.desc(), Registration.month.desc())
    )

    state_2020 = Registration.select(
        fn.SUM(Registration.dem).alias('dem'),
        fn.SUM(Registration.rep).alias('rep'),
        fn.SUM(Registration.unaf).alias('unaf'),
        fn.SUM(Registration.other).alias('other')
    ).where(Registration.year == 2020).dicts().get()

    state_2024 = Registration.select(
        fn.SUM(Registration.dem).alias('dem'),
        fn.SUM(Registration.rep).alias('rep'),
        fn.SUM(Registration.unaf).alias('unaf'),
        fn.SUM(Registration.other).alias('other')
    ).where(Registration.year == 2024).dicts().get()

    # Total all categories
    def total(v):
        return sum(v.values())

    county_total_2020 = total(year_2020)
    county_total_2024 = total(year_summary)
    state_total_2020 = total(state_2020)
    state_total_2024 = total(state_2024)

    county_change = percent_change(county_total_2024, county_total_2020)
    state_change = percent_change(state_total_2024, state_total_2020)

    counties = Registration.select(Registration.county).distinct().order_by(Registration.county)

    return render_template(
        "county_detail.html",
        county=county,
        flourish_id=embed_id,
        image_path=image_path,
        year_summary=year_summary,
        year_2020=year_2020,
        change=change,
        county_change=county_change,
        state_change=state_change,
        records=historical_records,
        counties=counties
    )

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)