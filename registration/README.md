3/26/25
Tasks: 
- Clean data. We only want the first page of data that shows the total voter registration numbers by county for each month and year. We also have to clean the column names and ensure it reads the second row as rows
- Write code that combines all party columns that are not Democrat, Republican or unaffiliated into one, so that we are left with four columns: Democrat, Republican, unaffiliated and other
- Compare current voter registration numbers in March to similiar years (other years, like 2021 right after an election and before the midterms) to see if voter registration numbers are on track, and if they're not, which parties are suffering
- Visualize these differences using Flourish
- Create a quiz that asks basic location information and shows users where their polling place is or what address to send their mail-in ballot with other resources
- Look into how inactive voter numbers have changed since 2006

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
