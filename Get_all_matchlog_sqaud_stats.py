#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 10:04:41 2025

@author: benharris
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from bs4 import Comment
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



# Generate year strings in the format 'YYYY-YYYY'
years = [f"{year}-{year+1}" for year in range(2024, 2025)]


# Safely extract text with a check for None
def safe_get_text(element):
    if element:
        return element.get_text(strip=True)
    return '0'  

# Function to clean up the stats
def clean_stat(value):
    if isinstance(value, str):
        # Remove commas inside strings and then convert to float
        value = value.replace(",", "")
        try:
            return float(value)  # Try converting to float
        except ValueError:
            return value  # Return the value as is if it's not a valid number (like player names)
    return value

def make_col(prefix, stat):
    # prefix: team or opponent name (string)
    # stat: stat name like 'Shots' or 'Goals'
    # sanitize prefix: strip and collapse whitespace
    p = " ".join(str(prefix).split()).strip()
    return f"{p} {stat}"

def standardize_team_column(df, prefix=""):
    # Find the column name used for team
    possible_cols = ["team", "Team", "squad", "Squad"]
    team_col = None

    for col in df.columns:
        if col in possible_cols:
            team_col = col
            break

    if team_col is None:
        raise ValueError(f"No team column found. Available columns: {df.columns.tolist()}")

    # Add prefix (if any)
    if prefix:
        df = df.add_prefix(prefix + "_")

        # rename prefixed team column back to 'Team'
        df = df.rename(columns={f"{prefix}_" + team_col: "Team"})
    else:
        df = df.rename(columns={team_col: "Team"})

    return df



def clean_stats_df(df, prefix):
    if df is None or df.empty:
        return df
    
    df = df.copy()

    # Keep Date unchanged
    cols = df.columns
    new_cols = []
    for c in cols:
        if c == "Date":
            new_cols.append("Date")
        else:
            new_cols.append(prefix + c)
    df.columns = new_cols

    return df

import re

_METADATA_TOKENS = [
    "team", "start_time", "round", "dayofweek", "venue",
    "result", "goals_for", "goals_against", "opponent", "match_report"
]

def drop_prefixed_metadata(df):
    if df is None:
        return None
    if df.empty:
        return df

    cols_to_drop = []
    for col in df.columns:
        low = col.lower()

        # RULE 1 — Drop ALL columns containing team metadata
        if "team" in low:
            cols_to_drop.append(col)
            continue

        # RULE 2 — Only consider For_/Against_ columns for the remaining metadata
        if low.startswith("for_") or low.startswith("against_"):
            if any(token in low for token in _METADATA_TOKENS):
                cols_to_drop.append(col)

    if cols_to_drop:
        df = df.drop(columns=cols_to_drop, errors="ignore")

    return df

def is_valid_match_row(row):
    # must have a real date
    date_cell = row.find("th", {"data-stat": "date"})
    if not date_cell:
        return False

    date_text = date_cell.get_text(strip=True)

    # reject empty or fake date
    if date_text == "" or date_text == "Date":
        return False

    # reject rows inside comments
    if isinstance(row, Comment):
        return False

    # reject rows without opponent
    if not row.find("td", {"data-stat": "opponent"}):
        return False

    return True





def get_scores_fixtures_stats(year): 
    web = f'https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/schedule/Oxford-United-Scores-and-Fixtures-Championship'
    print(f"Requesting URL: {web}")
    
    # --- Set headers (User-Agent) here ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")  # remove if you want browser to show
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Create driver with headers
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(web)
    
        content = driver.page_source
    
    finally:
        driver.quit()
    
    soup = BeautifulSoup(content, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    
    for_table = soup.find('div', {'id': 'all_matchlogs'}).find('table')
    
    if not for_table:
        print("No table found in 'all_matchlogs'")
        return pd.DataFrame()

    rows = for_table.find('tbody').find_all('tr')
    clean_rows = [r for r in rows if is_valid_match_row(r)]

    
    date = []
    times = []
    comp = []
    day = []
    venue = []
    result = []
    goals_for = []
    goals_against = []
    opponent = []
    xG_for = []
    xG_against = []
    possession = []
    attendance = []
    captain = []
    formation = []
    opposition_formation = []
    referee = []
    
    for row in clean_rows:
        date_element = row.find('th', {'data-stat': 'date'})
        if date_element is None or not date_element.get_text(strip=True):
            continue
        times_element = row.find('td', {'data-stat': 'start_time'})
        comp_element = row.find('td', {'data-stat': 'round'})
        day_element = row.find('td', {'data-stat': 'dayofweek'})
        venue_element = row.find('td', {'data-stat': 'venue'})
        result_element = row.find('td', {'data-stat': 'result'})
        goals_for_element = row.find('td', {'data-stat': 'goals_for'})
        goals_against_element = row.find('td', {'data-stat': 'goals_against'})
        opponent_element = row.find('td', {'data-stat': 'opponent'})
        xG_for_element = row.find('td', {'data-stat': 'xg_for'})
        xG_against_element = row.find('td', {'data-stat': 'xg_against'})
        possession_element = row.find('td', {'data-stat': 'possession'})
        attendance_element = row.find('td', {'data-stat': 'attendance'})
        captain_element = row.find('td', {'data-stat': 'captain'})
        formation_element = row.find('td', {'data-stat': 'formation'})
        opposition_formation_element = row.find('td', {'data-stat': 'opp_formation'})
        referee_element = row.find('td', {'data-stat': 'referee'})
        
        date1 = clean_stat(safe_get_text(date_element))
        times1 = clean_stat(safe_get_text(times_element))
        comp1 = clean_stat(safe_get_text(comp_element))
        day1 = clean_stat(safe_get_text(day_element))
        venue1 = clean_stat(safe_get_text(venue_element))
        result1 = clean_stat(safe_get_text(result_element))
        goals_for1 = clean_stat(safe_get_text(goals_for_element))
        goals_against1 = clean_stat(safe_get_text(goals_against_element))
        opponent1 = clean_stat(safe_get_text(opponent_element))
        xG_for1 = clean_stat(safe_get_text(xG_for_element))
        xG_against1 = clean_stat(safe_get_text(xG_against_element))
        possession1 = clean_stat(safe_get_text(possession_element))
        attendance1 = clean_stat(safe_get_text(attendance_element))
        captain1 = clean_stat(safe_get_text(captain_element))
        formation1 = clean_stat(safe_get_text(formation_element))
        opposition_formation1 = clean_stat(safe_get_text(opposition_formation_element))
        referee1 = clean_stat(safe_get_text(referee_element))
        
        date.append(date1)
        times.append(times1)
        comp.append(comp1)
        day.append(day1)
        venue.append(venue1)
        result.append(result1)
        goals_for.append(goals_for1)
        goals_against.append(goals_against1)
        opponent.append(opponent1)
        xG_for.append(xG_for1)
        xG_against.append(xG_against1)
        possession.append(possession1)
        attendance.append(attendance1)
        captain.append(captain1)
        formation.append(formation1)
        opposition_formation.append(opposition_formation1)
        referee.append(referee1)
    
    if date:
        dict_football = {'Team': 'Oxford United', 'Date': date, 'Time': times,
                         'Competition': comp, 'Day': day,
                         'Venue': venue, 'Result': result, 'Goals For': goals_for,
                         'Goals Against': goals_against, 'Opponent': opponent,
                         'xG For': xG_for, 'xG Against': xG_against,
                         'Possession': possession, 'Attendance': attendance,
                         'Captain': captain, 'Formation': formation,
                         'Opposition Formation': opposition_formation,
                         'Referee': referee}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame()

def parse_fbref_table(table, team_name=None):
    """Parses a FBref table into a pandas DataFrame."""


    rows = table.find("tbody").find_all("tr")
    clean_rows = [r for r in rows if is_valid_match_row(r)]


    extracted = []
    for row in clean_rows:
        date_cell = row.find("th", {"data-stat": "date"})
        if not date_cell or not date_cell.get_text(strip=True):
            continue

        record = {"Date": clean_stat(safe_get_text(date_cell))}

        # Extract all <td data-stat="">
        for td in row.find_all("td"):
            stat = td.get("data-stat")
            value = clean_stat(safe_get_text(td))
            record[stat] = value

        extracted.append(record)

    if not extracted:
        return pd.DataFrame()

    df = pd.DataFrame(extracted)

    # Optional: add a team column
    if team_name:
        df.insert(0, "Team", team_name)

    return df


def get_shooting_stats(year):

    # --- Build URL ---
    web = f"https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/shooting/Oxford-United-Match-Logs-Championship"
    print(f"Requesting URL: {web}")

    # --- User-agent header ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Selenium options ---
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # --- Load page once ---
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(web)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    # --- FIND BOTH TABLES ---
    for_df = None
    against_df = None

    # ----------------------------------------
    #           MATCHLOGS FOR (team)
    # ----------------------------------------
    


    div_for = soup.find("div", id="div_matchlogs_for")
    if div_for:
        table_for = div_for.find("table", id="matchlogs_for")
        if table_for:
            print("✓ Found matchlogs_for table")
            for_df = parse_fbref_table(table_for, team_name="Team")

    # ----------------------------------------
    #          MATCHLOGS AGAINST (opponent)
    # ----------------------------------------

    div_against = soup.find("div", id="div_matchlogs_against")
    if div_against:
        table_against = div_against.find("table", id="matchlogs_against")
        if table_against:
            print("✓ Found matchlogs_against table")
            against_df = parse_fbref_table(table_against, team_name="Opponent")

    
    print(f"Finished extracting shooting stats for year {year}.")
    return for_df, against_df
        
def get_goalkeeping_stats(year):

    # --- Build URL ---
    web = f"https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/keeper/Oxford-United-Match-Logs-Championship"
    print(f"Requesting URL: {web}")

    # --- User-agent header ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Selenium options ---
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # --- Load page once ---
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(web)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    # --- FIND BOTH TABLES ---
    for_df = None
    against_df = None

    # ----------------------------------------
    #           MATCHLOGS FOR (team)
    # ----------------------------------------



    div_for = soup.find("div", id="div_matchlogs_for")
    if div_for:
        table_for = div_for.find("table", id="matchlogs_for")
        if table_for:
            print("✓ Found matchlogs_for table")
            for_df = parse_fbref_table(table_for, team_name="Team")

    # ----------------------------------------
    #          MATCHLOGS AGAINST (opponent)
    # ----------------------------------------

    div_against = soup.find("div", id="div_matchlogs_against")
    if div_against:
        table_against = div_against.find("table", id="matchlogs_against")
        if table_against:
            print("✓ Found matchlogs_against table")
            against_df = parse_fbref_table(table_against, team_name="Opponent")

    
    print(f"Finished extracting keeper stats for year {year}.")
    return for_df, against_df
    

def get_passing_stats(year):

    # --- Build URL ---
    web = f"https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/passing/Oxford-United-Match-Logs-Championship"
    print(f"Requesting URL: {web}")

    # --- User-agent header ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Selenium options ---
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # --- Load page once ---
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(web)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    # --- FIND BOTH TABLES ---
    for_df = None
    against_df = None

    # ----------------------------------------
    #           MATCHLOGS FOR (team)
    # ----------------------------------------



    div_for = soup.find("div", id="div_matchlogs_for")
    if div_for:
        table_for = div_for.find("table", id="matchlogs_for")
        if table_for:
            print("✓ Found matchlogs_for table")
            for_df = parse_fbref_table(table_for, team_name="Team")

    # ----------------------------------------
    #          MATCHLOGS AGAINST (opponent)
    # ----------------------------------------

    div_against = soup.find("div", id="div_matchlogs_against")
    if div_against:
        table_against = div_against.find("table", id="matchlogs_against")
        if table_against:
            print("✓ Found matchlogs_against table")
            against_df = parse_fbref_table(table_against, team_name="Opponent")


    print(f"Finished extracting keeper stats for year {year}.")
    return for_df, against_df


def get_passing_type_stats(year):

    # --- Build URL ---
    web = f"https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/passing_types/Oxford-United-Match-Logs-Championship"
    print(f"Requesting URL: {web}")

    # --- User-agent header ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Selenium options ---
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # --- Load page once ---
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(web)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    # --- FIND BOTH TABLES ---
    for_df = None
    against_df = None

    # ----------------------------------------
    #           MATCHLOGS FOR (team)
    # ----------------------------------------



    div_for = soup.find("div", id="div_matchlogs_for")
    if div_for:
        table_for = div_for.find("table", id="matchlogs_for")
        if table_for:
            print("✓ Found matchlogs_for table")
            for_df = parse_fbref_table(table_for, team_name="Team")

    # ----------------------------------------
    #          MATCHLOGS AGAINST (opponent)
    # ----------------------------------------

    div_against = soup.find("div", id="div_matchlogs_against")
    if div_against:
        table_against = div_against.find("table", id="matchlogs_against")
        if table_against:
            print("✓ Found matchlogs_against table")
            against_df = parse_fbref_table(table_against, team_name="Opponent")
    

    print(f"Finished extracting keeper stats for year {year}.")
    return for_df, against_df


def get_gca_stats(year):

    # --- Build URL ---
    web = f"https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/gca/Oxford-United-Match-Logs-Championship"
    print(f"Requesting URL: {web}")

    # --- User-agent header ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Selenium options ---
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # --- Load page once ---
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(web)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    # --- FIND BOTH TABLES ---
    for_df = None
    against_df = None

    # ----------------------------------------
    #           MATCHLOGS FOR (team)
    # ----------------------------------------



    div_for = soup.find("div", id="div_matchlogs_for")
    if div_for:
        table_for = div_for.find("table", id="matchlogs_for")
        if table_for:
            print("✓ Found matchlogs_for table")
            for_df = parse_fbref_table(table_for, team_name="Team")

    # ----------------------------------------
    #          MATCHLOGS AGAINST (opponent)
    # ----------------------------------------

    div_against = soup.find("div", id="div_matchlogs_against")
    if div_against:
        table_against = div_against.find("table", id="matchlogs_against")
        if table_against:
            print("✓ Found matchlogs_against table")
            against_df = parse_fbref_table(table_against, team_name="Opponent")


    print(f"Finished extracting keeper stats for year {year}.")
    return for_df, against_df


def get_defence_stats(year):

    # --- Build URL ---
    web = f"https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/defense/Oxford-United-Match-Logs-Championship"
    print(f"Requesting URL: {web}")

    # --- User-agent header ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Selenium options ---
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # --- Load page once ---
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(web)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    # --- FIND BOTH TABLES ---
    for_df = None
    against_df = None

    # ----------------------------------------
    #           MATCHLOGS FOR (team)
    # ----------------------------------------



    div_for = soup.find("div", id="div_matchlogs_for")
    if div_for:
        table_for = div_for.find("table", id="matchlogs_for")
        if table_for:
            print("✓ Found matchlogs_for table")
            for_df = parse_fbref_table(table_for, team_name="Team")

    # ----------------------------------------
    #          MATCHLOGS AGAINST (opponent)
    # ----------------------------------------

    div_against = soup.find("div", id="div_matchlogs_against")
    if div_against:
        table_against = div_against.find("table", id="matchlogs_against")
        if table_against:
            print("✓ Found matchlogs_against table")
            against_df = parse_fbref_table(table_against, team_name="Opponent")


    print(f"Finished extracting keeper stats for year {year}.")
    return for_df, against_df


def get_possession_stats(year):

    # --- Build URL ---
    web = f"https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/possession/Oxford-United-Match-Logs-Championship"
    print(f"Requesting URL: {web}")

    # --- User-agent header ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Selenium options ---
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # --- Load page once ---
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(web)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    # --- FIND BOTH TABLES ---
    for_df = None
    against_df = None

    # ----------------------------------------
    #           MATCHLOGS FOR (team)
    # ----------------------------------------



    div_for = soup.find("div", id="div_matchlogs_for")
    if div_for:
        table_for = div_for.find("table", id="matchlogs_for")
        if table_for:
            print("✓ Found matchlogs_for table")
            for_df = parse_fbref_table(table_for, team_name="Team")

    # ----------------------------------------
    #          MATCHLOGS AGAINST (opponent)
    # ----------------------------------------

    div_against = soup.find("div", id="div_matchlogs_against")
    if div_against:
        table_against = div_against.find("table", id="matchlogs_against")
        if table_against:
            print("✓ Found matchlogs_against table")
            against_df = parse_fbref_table(table_against, team_name="Opponent")

    print(f"Finished extracting keeper stats for year {year}.")
    return for_df, against_df


def get_misc_stats(year):

    # --- Build URL ---
    web = f"https://fbref.com/en/squads/604617a2/{year}/matchlogs/c10/misc/Oxford-United-Match-Logs-Championship"
    print(f"Requesting URL: {web}")

    # --- User-agent header ---
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Selenium options ---
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # --- Load page once ---
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(web)
        html = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(html, "lxml")
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        try:
            comment.extract()
        except:
            pass

    # --- FIND BOTH TABLES ---
    for_df = None
    against_df = None

    # ----------------------------------------
    #           MATCHLOGS FOR (team)
    # ----------------------------------------



    div_for = soup.find("div", id="div_matchlogs_for")
    if div_for:
        table_for = div_for.find("table", id="matchlogs_for")
        if table_for:
            print("✓ Found matchlogs_for table")
            for_df = parse_fbref_table(table_for, team_name="Team")

    # ----------------------------------------
    #          MATCHLOGS AGAINST (opponent)
    # ----------------------------------------

    div_against = soup.find("div", id="div_matchlogs_against")
    if div_against:
        table_against = div_against.find("table", id="matchlogs_against")
        if table_against:
            print("✓ Found matchlogs_against table")
            against_df = parse_fbref_table(table_against, team_name="Opponent")


    print(f"Finished extracting keeper stats for year {year}.")
    return for_df, against_df














def merge_matchlogs(base_df, for_df, against_df):
    import sys
    
    cols_to_remove = [
        'Team', 'start_time', 'round', 'dayofweek', 'venue',
        'result', 'goals_for', 'goals_against', 'opponent', 'match_report'
    ]

    print("\n--- BEFORE CLEANUP ---")
    print("Base DF columns:", base_df.columns.tolist())
    if for_df is not None:
        print("FOR DF columns:", for_df.columns.tolist())
    if against_df is not None:
        print("AGAINST DF columns:", against_df.columns.tolist())

    # --- Clean FOR DataFrame ---
    if for_df is not None and not for_df.empty:
        drop_cols_for = [col for col in for_df.columns if col in cols_to_remove]
        print("Dropping from FOR DF:", drop_cols_for)
        for_df = for_df.drop(columns=drop_cols_for, errors='ignore')

        # Add prefix to everything except 'Date'
        rename_for = {col: f"For_{col}" for col in for_df.columns if col != 'Date'}
        print("Renaming FOR DF columns:", rename_for)
        for_df = for_df.rename(rename_for, axis=1)

    # --- Clean AGAINST DataFrame ---
    if against_df is not None and not against_df.empty:
        drop_cols_against = [col for col in against_df.columns if col in cols_to_remove]
        print("Dropping from AGAINST DF:", drop_cols_against)
        against_df = against_df.drop(columns=drop_cols_against, errors='ignore')

        # Add prefix to everything except 'Date'
        rename_against = {col: f"Against_{col}" for col in against_df.columns if col != 'Date'}
        print("Renaming AGAINST DF columns:", rename_against)
        against_df = against_df.rename(rename_against, axis=1)

    # --- Show final columns before merge ---
    print("\n--- BEFORE MERGE ---")
    if for_df is not None:
        print("FOR DF columns:", for_df.columns.tolist())
    if against_df is not None:
        print("AGAINST DF columns:", against_df.columns.tolist())

    # --- Merge FOR ---
    if for_df is not None and not for_df.empty:
        if "Date" not in for_df.columns:
            print("ERROR: 'Date' column missing in FOR DF!")
            sys.exit(1)
        base_df = base_df.merge(for_df, left_on="Date", right_on="Date", how="left")
        print("Merged FOR DF successfully.")

    # --- Merge AGAINST ---
    if against_df is not None and not against_df.empty:
        if "Date" not in against_df.columns:
            print("ERROR: 'Date' column missing in AGAINST DF!")
            sys.exit(1)
        base_df = base_df.merge(against_df, left_on="Date", right_on="Date", how="left")
        print("Merged AGAINST DF successfully.")

    # Remove duplicate columns if any
    base_df = base_df.loc[:, ~base_df.columns.duplicated()]

    print("\n--- AFTER MERGE ---")
    print("Base DF columns:", base_df.columns.tolist())

    return base_df











all_data = []

for year in years:
    print("Processing year:", year)

    standard_stats = get_scores_fixtures_stats(year)

    # Collect all matchlog stats
    for_shooting_df,   against_shooting_df   = get_shooting_stats(year)
    for_keeper_df,     against_keeper_df     = get_goalkeeping_stats(year)
    for_passing_df,    against_passing_df    = get_passing_stats(year)
    for_passing_type_df, against_passing_type_df = get_passing_type_stats(year)
    for_gca_df,        against_gca_df        = get_gca_stats(year)
    for_defence_df,    against_defence_df    = get_defence_stats(year)
    for_possession_df, against_possession_df = get_possession_stats(year)
    for_misc_df,       against_misc_df       = get_misc_stats(year)

    # Base dataframe
    base_df = standard_stats.copy()
    base_df = standardize_team_column(base_df)


    # --- MERGE ALL MATCHLOG CATEGORIES ---
    base_df = merge_matchlogs(base_df, for_shooting_df,       against_shooting_df)
    base_df = merge_matchlogs(base_df, for_keeper_df,         against_keeper_df)
    base_df = merge_matchlogs(base_df, for_passing_df,        against_passing_df)
    base_df = merge_matchlogs(base_df, for_passing_type_df,   against_passing_type_df)
    base_df = merge_matchlogs(base_df, for_gca_df,            against_gca_df)
    base_df = merge_matchlogs(base_df, for_defence_df,        against_defence_df)
    base_df = merge_matchlogs(base_df, for_possession_df,     against_possession_df)
    base_df = merge_matchlogs(base_df, for_misc_df,           against_misc_df)

    base_df = base_df.loc[:, ~base_df.columns.duplicated()]

    # Finalise
    base_df["year"] = year
    base_df.fillna(0, inplace=True)

    all_data.append(base_df)
    time.sleep(5)

# Save final combined output
if all_data:
    df_final = pd.concat(all_data, ignore_index=True)
    df_final.to_csv("all_squad_stats_matchlogs_24-25_Championship.csv", index=False)
    print("CSV created successfully.")
else:
    print("No data available.")



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    