Ideas We Have: 
1) Reporting on the number of inactive voters across counties, and whether the number of inactive voters has increased or decreased over different years. Has anything encouraged/discouraged voter turnout? What is the engagement of eligible voters? 
- We could have a newsapp that let's users put filters in exploring data on voter counties/turnout. The newsapp could also feature a chloropleth map that darkens counties with higher voter turnout. 
2) Exploring voter turnout among parties during different elections. 
3) "How Maryland voters prefer to cast their votes" Looking into how different Maryland voters will cast their votes, whether its by mail or in person. Does this differ by counties or does this differ over the years? 


First Steps: 
1) Convert all of our Excel files to CSV files 
- Datasets we need: Official by Party and County, InActive Voters, Eligible Active Voters by County 
2. Putting these datasette to see how we can view the intersection of these databases. 
3) Narrowing the scope of our story and finding the questions we want to answer. 

Other Thoughts: 
We are leaning towards investigating inactive voters across different counties. Our main first step would just be to use the percent change formula across different counties' inactive voters. 


 2024-04-04

 Completed:
 - We have converted all necessary files into csv files in the turnout_data directory
 - We cleaned the files and added columns for party identification (official turnout dataset) and year (all datasets)
 - We merged the datasets by view/topic and created the three full dataset files (official_by_party_and_county_compelete, eligible_active, and eligible_inactive)
 - All three of the complete datasets have been imported as tables into Datasette in the turnout database (turnout.db)
 - Using the First News App tutorial, we created a starting webpage for turnout data. So far, it displays the full official turnout data as a table.

To be done:
- Modify the index (home) page to resemble the IKE Labs home page, where each turnout category is a link to a detailed page for that view:
    - Official Maryland Voter Turnout (Marco)
    - Eligible Active Voter Turnout (Reem and Natalie)
    - Eligible Inactive Voter Turnout (Kriti)

Initial plans for each page (subject to change):
- Official Maryland Voter Turnout:
    - present a paginated version of the full table 
    - hyperlink each county name to a detailed County page:
         - present a map that outlines the county boundaries
         - indicate which party has generally received the most support across the available data (turnout percentage/count)
         - break down data by year: indicate which party won the election that year and how the turnout was distributed across parties
         - present eligible and ineligble voter activity data (tables and links to those pages)
    - have a map of Maryland that is partitioned by county:
         - colorcode by: the color that represents the most supported party or according to turnout percentage using color intensity
         - have hover data that includes: county name, turnout percentage by year, and a link to the detailed county page

- Eligible Active Voter Turnout
    - present a paginated version of the full table 
    - have a choropleth map where the intensity represents the percentage of eligible active voter participation/turnout
        - have hover data that includes the other attributes from the data: county name and the count of eligible active voter turnout by year
    - display bar charts that also visualize and represent eligible voter turnout by party, and we can add filters by year
    - we could layer the bar charts with a trend line that shows any patterns
    - we could try to make line charts for voter activity by county, but we would first see if the data is not too overcrowded/hard to interact with
    - link any county names to the detailed County page described above

- Eligible Inctive Voter Turnout
    - present a paginated version of the full table 
    - if we calculate percent change in voter inactivity, we could use that do create the choropleth map and use it to decide color intensity by county
    - present similar bar charts and line graphs as eligible active voter section

- if it's a better idea, we could consider having one page for both Eligible Active/Inactive Voter Activity and present the data side by side for comparision or as a separate view within the same page

- no current blockers

2024-04-11
Completed:
- we created peewee models for all three files which means we currently have a model for Official Voter Turnout, Eligible Active Voter Turnout, and Eligible Inctive Voter Turnout
- we created the html files for each page/view of the Maryland voter turnout data
- created the home page with links to each detailed view and a navigation menu
- paginated all current tables 
- added basic table filtering by attribute for eligible inactive voter view

To be done:
Now that we have our basic layout and all of our data as structured and connected site, we will use this week to incorporate our data processing and visualization ideas.
- clean up our directory (Marco) -  we have too many folders and files to keep track of and not all of them are necessary, so a clean up will help us stay organized
- geocode counties to then add the choropleth maps (Natalie)
- explore potential uses for Datawrapper or Flourish (Natalie)
- add line graphs to eligible inactive voters page to show trends for counties by year (Kriti)
- add filters to the offical turnout page (different from eligible voters) [Marco]
- calculate and add the percent change column for official voter turnout (Marco)
- adjust pagination if necessary (Reem)
- add filters and graphs to eligible active voter page (Reem)

Blockers:
- some of our updates are still waiting to be pushed so we will have to be careful when trying to push them to avoid damage to other files
