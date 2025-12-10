# Canberra United FC Tactical Analysis
This project applies data analysis techniques to data taken from the 2024-25 A-League Womens season in order to analyse Canberra United FC's season. I wanted to see specifically how they play and the style they play with, and where they could be doing better within this style. 

## Data & Cleaning
All data was taken from FBREF.com.
In order to clean the data I made sure that any NaN datapoints became 0, and that I could extract any text without it corrupting my data since mostly I was getting numerical data with the occasional text.
It took a while to extract the data as FBREF.com consistently would deny me access to the site, but after I used selenium and some headers so I did not look like a bot I managed to extract what I needed.

The two files that I used to extract the data, 'Get_all_matchlog_squad_stats.py' and 'Get_all_squad_stats.py', are both now geared up to extract data from the Championship and Oxford United, rather than A-League Womens and Canberra United, but it is a quick and easy fix to change the team and league to whatever you want to extract.

## Tools
- Python(using Spyder): selenium, BeautifulSoup, pandas
- SQL

## Models
The two models I used to analyse the data are also both currently rigged up to work for Oxford United, but it is also an easy change to make it work for Canberra United. Essentially the only difference is that I use the data from the A-League Womens and I change the team in focus to Canberra United rather than Oxford United. Also, I added a rivals section for my analysis of Oxford United in order to see more clearly the way that Oxford United played compared to their closest rivals in the league, rather than against the giants at the top of the league who skew the averages. I chose not to do this for my analysis of Canberra United because the A-League Womens is only 12 teams and there is much less of a difference between teams at the top and bottom of the table than compared the the English Championship.

In the model 'club_analysis.py' I used entirely SQL queries to get the data I wanted from the dataset and then python to plot bar charts. In 'matchlog_analysis.py' I utilised more styles of analysis, such as line charts and also correlation between wins and certain statistics. I then plotted more line charts based on the results of the correlation but the code I wrote for these charts are not on the file anymore because I deleted it to change it for a new project on Oxford United.

## Results
Please see the file 'Canberra United F.C. Tactical Analysis - Google Docs.pdf' for my detailed report of Canberra United's tactical analysis.
