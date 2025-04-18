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

2024-04-18

Features of our News App: 
Introduction to what the data means
Given the timeframe of the data in our app, we know that we are going to discuss the role that the pandemic had in the differences between voter turnout and the turnout methods used
We also plan to discuss any notable differences in behavior by voter party preferences 
Once we get our data visualizations on the pages, we will reference them in the text 
Bullet points summarizing the most interesting findings (written by us after finding trends or using Groq)
Statewide choropleth map that displays changes in turnout over time
If the numbers don’t show a common pattern, we could do a row chart instead 
County-level line charts that display changes in turnout over time (you could filter to certain counties so it won’t be too cluttered) 
Tooltips to hover over and easily see the numbers/navigate the data
Filters/Dropdown bar that provides an option to show breakdown by county or party


Final Project Update: 

This past week, we were about to refine our news app so that it will have three web pages explaining voter turnout information. Not only does the home page of the website have photos and links leading to subpages, but our web pages have detailed information as well. We have webpages for official Maryland turnout, eligible active voters and eligible inactive voters.

We updated our tables by incorporating the DataTables JavaScript library into all three of the detailed pages. The library gave us an easier way to paginate and style the tables. More importantly, it helped us add interactivity to the tables because in the Official Turnout page, users can sort the counties by: Election Day turnout, Early Voting turnout, Vote by Mail turnout, Provisional turnout, number of Eligible Voters, Turnout Percentage, and year in increasing or decreasing order. Since it would not make sense to sort the data by party or county, we created filters for these attributes and for year as well. We created the filter buttons in HTML, but we used AI to write the code to give them functionality since it required JavaScript. We provided the HTML code for it to see the buttons and the Python code for it to understand the structure of the data we were trying to create filters for. On the first prompt, it provided the functional JavaScript code to dynamically load county names and to filter the tables based on the selected conditions. We’re also planning on creating filters for the type of turnout for the Official Turnout page in case users want to compare differences within turnout method between the two years (e.g., early voting turnout in 2020 vs 2024). 

The Eligible Inactive and Eligible Active voter pages have the same filters (year, county, and party), but the tables on these pages can be sorted by party turnout: Democrat, Bread and Roses, Green, Libertarian, Working Class Party, No Labels Maryland, Unaffiliated, or Other. We used the same code from the Official Turnout page to make the filters functional. These pages will be the main focus now because we want to use the chart.js library to create bar graphs for voter turnout by party by county across the two different years (2020 and 2024). The idea is to allow users to select a county and then display the bars for the two years beside each other for each party. If the user has the Statewide option selected, it would aggregate all the county data by party for each year and display those differences. We will color-code the bars and make an easy-to-read legend. 


We also explored creating data visualizations for our news app but realized that they may present some of the data as more confusing. For example, we originally planned to create a table on Datawrapper showing Maryland voter turnout across each county. But after realizing that voter turnout increased slightly in almost every county, we concluded that the visualization would just be repetitive with displaying information from each county. Instead, we realized that it might be better to write up a few bullet points describing the three data tables we have. This will create more simplicity for a news app that is loaded with data tables. We will be drafting the language of these bullet points and incorporating them into our news app this upcoming week. 

Blockers:
- No major blockers, we're just learning more about our data as we keep trying our ideas, so we're adjusting as we learn. 