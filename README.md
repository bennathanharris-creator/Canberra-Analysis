# Canberra United FC Tactical Analysis
This project applies data analysis techniques to data taken from the 2024-25 A-League Womens season in order to analyse Canberra United FC's season. I wanted to see specifically how they play and the style they play with, and where they could be doing better within this style. 

## Data & Cleaning
All data was taken from FBREF.com.
In order to clean the data I made sure that any NaN datapoints became 0, and that I could extract any text without it corrupting my data since mostly I was getting numerical data with the occasional text.
It took a while to extract the data as FBREF.com consistently would deny me access to the site, but after I used selenium and some headers so I did not look like a bot I managed to extract what I needed.

## Tools
- Python(using Spyder): selenium, BeautifulSoup, pandas
- SQL

