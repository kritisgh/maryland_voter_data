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
        - Official Maryland Voter Turnout
        - Eligible Active Voter Turnout
        - Eligible Inactive Voter Turnout

Initial plans for each page (subject to change):
- Official Maryland Voter Turnout:
        - present the a paginated version of the full table 
        - hyperlink each county name to a detailed County page:
                - present a map that outlines the county boundaries
                - indicate which party has generally received the most support across the available data (turnout percentage/count)
                - break down data by year: indicate which party won the election that year and how the turnout was distributed across parties
        - have a map of Maryland that is partitioned by county:
                - colorcode by: the color that represents the most supported party or according to turnout percentage using color intensity
                - have hover data that includes: county name, turnout percentage by year, and a link to the detailed county page
