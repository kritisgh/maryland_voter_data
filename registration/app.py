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

@app.route("/")
def index():
    template = 'index.html'
    return render_template(template)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
