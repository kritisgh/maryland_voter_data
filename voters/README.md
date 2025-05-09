# Who Votes In Maryland? A News App by Rushabh Kamdar, Katharine Wilson, Johnny Yan, and Geoffrey Zhang

To access our web app, please run our app.py in the terminal using "python app.py" and ensuring that you are in the "voter" folder. This should run the app like any other Flask web app. Attempts to upload our app to GitHub Pages unfortunately resulted in errors with our JavaScript code.

________________________
3/26/2025 --
Things we need aggregated:
Of people who voted in the 2024 election, in (blank city), (percentage) were registered Democrats, etc.

3/25/2025 --
Cleaned data with Pandas. Added Geocode and map to Datasette with following code:

geocode-sqlite nominatim agg.db agg
--location="{residential_city}, 'MD'"
--delay=1
--user-agent="newsapps-geo"


3/24/2025 --
See Github Issues. https://github.com/NewsAppsUMD/maryland_voter_data/issues/3


3/12/2025 --
We would like to group voters by ZIP Code/city, age, and political affiliation - and figure out what proportion of voters are associated with a party based on ZIP Code/city and age. We are trying to decide whether to use ZIP Code or city name - if we use city name, we run into issues with people miswriting their city. If we use ZIP Code, we may overgeneralize a person's location (some people's ZIP codes might be for two or more cities.)

Another potential idea we discussed was identifying whether certain names or suffixes vote more Democratic or Republican - which is something we briefly explored using a Datasette we started. We could not find many conclusive observations, however, when looking into this.

Ideas for the final product: we can have a map with pins for different cities. Each city would have its own page showcasing a breakdown of political affiliation overall, and split by age. 
