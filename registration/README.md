4/18/25:
We focused on getting our visualizations and non-data information completed this week. This includes:
<li>DB: Writing homepage summary of application as well as county summaries</li>
<li>April and Olivia: Creating chlorpleth maps for state-level and county-level registration numbers</li>
<li>Anthony: creating HTML/CSS code for the home page (to start)</li>

4/11/25: 
- All our data is in CSVs and has been cleaned. We have monthly voter registration CSVs, yearly totals by county and inactive voter totals by year
- We started developing the HTML site and have thought about the design
- We've made four data visualizations showing 2022 voter registration per 100,000 residents by county, changes in inactive voter registration over time, Democrat voter registration in the last year + 2 months, and Democrat/Republican registration rates over time. We have all the iframe embed codes but haven't put them into the HTML yet because we're still figuring out the design/layout

4/4/25: 
Tasks assigned via issues 

We turns the pdfs data into csvs data. This is so for now we can now manipulate data and start wroking on our project.

The task are the folling:

Voter quiz a la NYT dialect story: https://www.nytimes.com/interactive/2014/upshot/dialect-quiz-map.html

April Tasks:


Review qualifications

Generate questions

If qualified: enter address for voter info

If not qualified: end of quiz

Anthony Task:

Write code that combines all party columns that are not Democrat, Republican or unaffiliated into one, so that we are left with four columns: Democrat, Republican, unaffiliated and other.

Calculate percent changes, last complete month (Feb/March) for midterm election years 2022 vs current 2025 State level County level
Olivia tasks:
- create data visualizations in Flourish from the new CSVs 

3/26/25
Tasks: 
- Clean data. We only want the first page of data that shows the total voter registration numbers by county for each month and year. We also have to clean the column names and ensure it reads the second row as rows
- Write code that combines all party columns that are not Democrat, Republican or unaffiliated into one, so that we are left with four columns: Democrat, Republican, unaffiliated and other
- Compare current voter registration numbers in March to similiar years (other years, like 2021 right after an election and before the midterms) to see if voter registration numbers are on track, and if they're not, which parties are suffering
- Visualize these differences using Flourish
- Create a quiz that asks basic location information and shows users where their polling place is or what address to send their mail-in ballot with other resources
- Look into how inactive voter numbers have changed since 2006

  Olivia Task:

Create Flourish visualizationsby party every mid-term election cycle Democrat Republican Unaffiliated Other By county - line graphs Allegany, Anne Arundel, Baltimore, Calvert, Caroline Carroll, Cecil, Charles, Dorchester, Frederick Garrett, Harford, Howard, Kent, Montgomery Prince George's, Queen Anne's, St. Mary's, Somerset, Talbot Washington, Wicomico, Worcester, Baltimore City.

Dabeluchukwu Task:


Analyze the historical change in the number of inactive voters from 2006 to present. Highlight which counties and parties have seen the largest increases or decreases in inactive voter counts.

Checklist:

 Extract inactive voter data by year/month

 Create line graphs by county and party






3/12/25

- We will find the total number of registered voters by county and party every midterm election since 2006,
  - Our party categories will be Democrat, Republican, unafiliated and other (other totals will include Green, Populist, etc in addition to the actual "other" column).
- We can present this data on a state-wide level so people can see county-by-county registration levels, and more detailed county analyses with additional information about change in registration, party breakdown, type and number of removals, and number of inactive voters.
- We'll need to convert these PDFs into data we can analyze (CSVs). We don't need OCR because the PDFs aren't images/scans.
- Our data is currently four tables all together in a PDF. We want to change this into tables with counties as the rows and years as the columns with each cell containing the total number of registered voters in the area. We can also create tables broken down by party or specific county tables. 
- Some things we're going to look at are how the number of unaffiliated voters have changed over time, the frequency of new party registration fluctuations, and overall trends in voter registration across different areas of the state.
- We will have a section where users can input their address and see their nearest polling place and details about how to vote in person or early via mail (including where to send their ballot). 

Notes:
Look at registration numbers by county. 

Thinking about the total numbers for registration every fours years.

We have statewide elections in off years, every 2 years. The patterns other states see we may not see here.

The state parties remain the same, but the new parties always come and go.


4/11/25
The inactive_month.py code is basically the same as the code that produces voter_registration_summary csv except this time it focuses on year,month,county,inactive. It produces inactive_voter_summarry.csv

inactive_month.py produces monthly_inactive_total.csv and it produces the total amount of inactive voters each month in a csv format.

Then there is plot_inactive.py which creates inactive_voter_trend.png which reads "monthly_inactive_totals.csv" to create the visuals. This was done with help from Chatgpt.

Some of the numbers are inaccuate and I will fix tommorow
