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
- Introduction to what the data means
   - Given the timeframe of the data in our app, we know that we are going to discuss the role that the pandemic had in the differences between voter turnout and the turnout methods used
   - We also plan to discuss any notable differences in behavior by voter party preferences 
   - Once we get our data visualizations on the pages, we will reference them in the text 
- Bullet points summarizing the most interesting findings (written by us after finding trends or using Groq)
- Statewide choropleth map that displays changes in turnout over time
   - If the numbers don’t show a common pattern, we could do a row chart instead 
- County-level bar graphs (or line charts) that display changes in turnout over time (you could filter to certain counties so it won’t be too cluttered) 
   - Tooltips to hover over and easily see the numbers/navigate the data
- Interactive (sortable/filterable) data tables for each view of turnout data (described below)
   - Filters/Dropdown bar that provides an option to show breakdown by county or party

Final Project Update: 

This past week, we were about to refine our news app so that it will have three web pages explaining voter turnout information. Not only does the home page of the website have photos and links leading to subpages, but our web pages have detailed information as well. We have webpages for official Maryland turnout, eligible active voters and eligible inactive voters.

We updated our tables by incorporating the DataTables JavaScript library into all three of the detailed pages. The library gave us an easier way to paginate and style the tables. More importantly, it helped us add interactivity to the tables because in the Official Turnout page, users can sort the counties by: Election Day turnout, Early Voting turnout, Vote by Mail turnout, Provisional turnout, number of Eligible Voters, Turnout Percentage, and year in increasing or decreasing order. Since it would not make sense to sort the data by party or county, we created filters for these attributes and for year as well. We created the filter buttons in HTML, but we used AI to write the code to give them functionality since it required JavaScript. We provided the HTML code for it to see the buttons and the Python code for it to understand the structure of the data we were trying to create filters for. On the first prompt, it provided the functional JavaScript code to dynamically load county names and to filter the tables based on the selected conditions. We’re also planning on creating filters for the type of turnout for the Official Turnout page in case users want to compare differences within turnout method between the two years (e.g., early voting turnout in 2020 vs 2024). 

The Eligible Inactive and Eligible Active voter pages have the same filters (year, county, and party), but the tables on these pages can be sorted by party turnout: Democrat, Bread and Roses, Green, Libertarian, Working Class Party, No Labels Maryland, Unaffiliated, or Other. We used the same code from the Official Turnout page to make the filters functional. These pages will be the main focus now because we want to use the chart.js library to create bar graphs for voter turnout by party by county across the two different years (2020 and 2024). The idea is to allow users to select a county and then display the bars for the two years beside each other for each party. If the user has the Statewide option selected, it would aggregate all the county data by party for each year and display those differences. We will color-code the bars and make an easy-to-read legend. 


We also explored creating data visualizations for our news app but realized that they may present some of the data as more confusing. For example, we originally planned to create a table on Datawrapper showing Maryland voter turnout across each county. But after realizing that voter turnout increased slightly in almost every county, we concluded that the visualization would just be repetitive with displaying information from each county. Instead, we realized that it might be better to write up a few bullet points describing the three data tables we have. This will create more simplicity for a news app that is loaded with data tables. We will be drafting the language of these bullet points and incorporating them into our news app this upcoming week. 

Blockers:
- No major blockers, we're just learning more about our data as we keep trying our ideas, so we're adjusting as we learn. 


**2024-04-25**

We want users to explore turnout (and lack of turnout) in their county and compare it to statewide turnout and/or turnout from another county of their choice. 

In the Eligible Active and Inactive pages (changing page names):
- The users will be able to initially see statewide turnout differences in a vertical bar graph made with chart.js
   - The bars will represent the difference in voter turnout between 2020 and 2024 
- Users will also be able to see and interact with a data table that displays the same data in a tabular format 
   - The columns are the parties, and there is a column for the county name
   - The rows are the calculated difference in voter turnout between 2020 and 2024 
   - Users can sort the data by turnout difference for a given party in increasing or decreasing order
   - When statewide data is selected in the dropdown, users can see the difference in turnout for all counties 
- The table and graph update in sync (selecting one county in one dropdown updates the table to show the same data)
- They will also see text explaining interesting findings and then use an LLM to connect some of the subsets of data to those findings 
- We will have a feature/section that explains what an eligible voter is 
- We can also explain how to become an active voter in the inactive voter page

In the Official Turnout page (changing page name):
- We are going to restructure the parties similar to how we did for the other datatables (add Working Class Party, No Labels Maryland, and Bread and Roses  to the “other” numbers because they are parties with very low numbers)
- Have a county selector and present the data based on turnout percent change by party in decreasing order 
   - For example, if a user selects Allgeny, they would see a vertical bar chart with differences in turnout percentage and percent change for each voting method
- We would present (in text) the party with the highest percent change in turnout for that county, the voting method with the highest percent increase between the two years, and the least used voting method (or most decreased percentage)

We will present full data tables in the “statewide” filter selection to add to the flexibility in case users want to explore neighboring counties or other counties of interest

If we had to describe the use of our app in a sentence or two, we would say that it allows users to explore statewide trends and shifts in voter turnout between 2020 and 2024 (presedential elections). We encourage users to closely examine their county to identify shifts in party alliance and turnout activity between the presedential elections. 

- Closest page to being completely functional: Eligible Inactive Voters
   - We are going to focus on finishing this page first, then we are going to translate the same logic to the other pages for similar functionality
- We added the chart.js charts 
- We changed the layout to present the vertical bar chart before the synced datatable 
- We grouped the data for Working Class Party, No Labels Maryland, and Bread and Roses into the “other” column because the differences were too insignificant and unnoticeable independently 
- Instead of having two rows (one for each year), we calculated the differences and displayed them instead 
- We are going to work on adding dynamic titles to the data to give relevant context  

- We still have to add the findings in the structure described above for each county 
- It will be dynamic to change with each county, but the data will change following a common structure 
   - Similar to one of the news apps we critiqued 

Blockers:
   - None, we have a clearer plan for this week 


**2024-05-02**

This week, we focused on improving the design and accessibility of our website. First, we changed the design of our website so that it would match the CNS stylebook. This included incorporating blue and yellow colors to the website and updating our headers and text to make it more readable. We also changed the home page of our website so that it is cleaner and more accessible. 

Something that we are hoping to improve for next week is to add more news-worthy headlines/page titles to each of the subpages. Additionally, we are hoping to write more texts of information summarizing our interesting findings so that our viewers will be more intrigued by the news app and have some takeaway, instead of just staring at a bunch of different numbers. 

As for navigation, we have a “Menu” sidebar that leads back to the home pages and subpages of our website. The website only has three subpages for the batches of data that we have, so it should be easy to navigate. Although we will not allow users to search through the website, it would be interesting for us to have a search bar for our dataset, something we can discuss in class. The datasets of each of our subpages allow users to filter the information by county or year, which makes the information more accessible. 

We also went through a vibe coding process to create a sample page that has all of our data views/pages within one county-specific page. The page also has the ability to compare data across counties side by side with our visualizations. It starts on an overview page with Total Turnout Change (2020 → 2024), Democrat Turnout Change, Republican Turnout Change, and Unaffiliated Turnout Change in percentages with a positive or negative symbol to represent an increase or decrease in turnout. It also displays the bar chart for Turnout Change By Party (2020 → 2024). The page for each county has three tabs: Official Turnout, Active Voters, and Inactive Voters. Under the bar chart, there is a table with the percent change in voter turnout for each party. If users want to compare counties, they would select the Enable Comparision button and select a county from the dropdown menu. When users are comparing counties, the bar charts only display data for three parties due to space limitations with side by side comparisions: Democrat, Republican, and Unaffiliated. We could switch the comarison to use horizontal bar charts with a common scale so that we can display the changes for all parties effectively. This page feels more like a news app and more smooth as a web application overall. It still follows the color scheme and guides set by April and Kriti and it can be edited further. If the county page is where we decide to go with our project, we will focus on incorporating the findings, interesting information, and some form of guidelines for using the application as text on those pages for context. We could have this be the landing page of our application and have it present statewide data and findings on load. 
