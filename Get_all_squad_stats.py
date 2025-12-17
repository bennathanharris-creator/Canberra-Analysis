#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 15:02:50 2025

@author: benharris
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Generate year strings in the format 'YYYY-YYYY'
years = [f"{year}-{year+1}" for year in range(2024, 2025)]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


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

def get_standard_stats(year):
    # URL for the stats page
    web = f'https://fbref.com/en/comps/196/{year}/stats/{year}-A-League-Women-Stats'
    print(f"Loading URL: {web}")

    # Set up Selenium WebDriver
    driver = webdriver.Chrome()
    
    try:
        # Open the webpage
        driver.get(web)

        # Extract the HTML content
        content = driver.page_source
        
    finally:
        # Close the browser window
        driver.quit()

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(content, 'lxml')
    
    # Locate the correct table within 'all_stats_standard'
    stats_table = soup.find('div', {'id': 'all_stats_squads_standard'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_standard'")
        return pd.DataFrame()

    # Extract data from the table
    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    minutes_played = []
    goals = []
    assists = []
    goals_plus_assists = []
    non_pen_goals = []
    pens_scored = []
    pens_attempted = []
    prog_carries = []
    prog_passes = []
    prog_passes_received = []
    yellows = []
    reds = []
    xG = []
    non_pen_xG = []
    xAG = []
    non_pen_xG_plus_xA = []
    avg_age = []
    avg_possession = []
    
    
    # Extract the data from the html code at 'data-stat' = stat to be extracted
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue  # Skip empty rows
        minutes_played_element = row.find('td', {'data-stat': 'minutes'})
        goals_element = row.find('td', {'data-stat': 'goals'})
        assists_element = row.find('td', {'data-stat': 'assists'})
        goals_plus_assists_element = row.find('td', {'data-stat': 'goals_assists'})
        non_pen_goals_element = row.find('td', {'data-stat': 'goals_pens'})
        pens_made_element = row.find('td', {'data-stat': 'pens_made'})
        pens_attempted_element = row.find('td', {'data-stat': 'pens_att'})
        prog_carries_element = row.find('td', {'data-stat': 'progressive_carries'})
        prog_passes_element = row.find('td', {'data-stat': 'progressive_passes'})
        prog_passes_received_element = row.find('td', {'data-stat': 'progressive_passes_received'})
        yellows_element = row.find('td', {'data-stat': 'cards_yellow'})
        reds_element = row.find('td', {'data-stat': 'cards_red'})
        xG_element = row.find('td', {'data-stat': 'xg'})
        non_pen_xG_element = row.find('td', {'data-stat': 'npxg'})
        xA_element = row.find('td', {'data-stat': 'xg_assist'})
        non_pen_xG_plus_xA_element = row.find('td', {'data-stat': 'npxg_xg_assist'})
        avg_age_element = row.find('td', {'data-stat': 'avg_age'})
        avg_possession_element = row.find('td', {'data-stat': 'possession'})
        
        # Clean the data
        team1 = clean_stat(safe_get_text(team_element))
        minutes = clean_stat(safe_get_text(minutes_played_element))
        G = clean_stat(safe_get_text(goals_element))
        A = clean_stat(safe_get_text(assists_element))
        G_plus_A = clean_stat(safe_get_text(goals_plus_assists_element))
        npG = clean_stat(safe_get_text(non_pen_goals_element))
        pens = clean_stat(safe_get_text(pens_made_element))
        pens_att = clean_stat(safe_get_text(pens_attempted_element))
        progC = clean_stat(safe_get_text(prog_carries_element))
        progP = clean_stat(safe_get_text(prog_passes_element))
        progPR = clean_stat(safe_get_text(prog_passes_received_element))
        yellow_cards = clean_stat(safe_get_text(yellows_element))
        red_cards = clean_stat(safe_get_text(reds_element))
        xg = clean_stat(safe_get_text(xG_element))
        npxg = clean_stat(safe_get_text(non_pen_xG_element))
        xa = clean_stat(safe_get_text(xA_element))
        npxg_plus_xa = clean_stat(safe_get_text(non_pen_xG_plus_xA_element))
        avg_age1 = clean_stat(safe_get_text(avg_age_element))
        avg_possession1 = clean_stat(safe_get_text(avg_possession_element))
        
        team.append(team1)
        minutes_played.append(minutes)
        goals.append(G)
        assists.append(A)
        goals_plus_assists.append(G_plus_A)
        non_pen_goals.append(npG)
        pens_scored.append(pens)
        pens_attempted.append(pens_att)
        prog_carries.append(progC)
        prog_passes.append(progP)
        prog_passes_received.append(progPR)
        yellows.append(yellow_cards)
        reds.append(red_cards)
        xG.append(xg)
        non_pen_xG.append(npxg)
        xAG.append(xa)
        non_pen_xG_plus_xA.append(npxg_plus_xa)
        avg_age.append(avg_age1)
        avg_possession.append(avg_possession1)
        
    # Send to dataframe as long as there is a player's name
    if team:
        dict_football = {'Team': team, 'Minutes': minutes_played, 'Goals': goals,
                         'Assists': assists, 'Goals + Assists': goals_plus_assists,
                         'Non Pen Goals': non_pen_goals, 'Pens Scored': pens_scored,
                         'Pens Attempted': pens_attempted, 'Prog Carries': prog_carries,
                         'Prog Passes': prog_passes, 'Prog Passes Received': prog_passes_received,
                         'Yellows': yellows, 'Reds': reds, 'xG': xG, 'Non Pen xG': non_pen_xG,
                         'xAG': xAG, 'Non Pen xG + xA': non_pen_xG_plus_xA,
                         'Avg Age': avg_age, 'Avg Possession': avg_possession}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame()
    
# Repeat same process for every other table to get all stats 
def get_shooting_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/shooting/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_shooting'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_shooting'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    shots = []
    shots_on_target = []
    npxG_per_shot = []
    G_minus_xG = []
    npG_minus_npxG = []
    SoT_percentage = []
    goals_per_shot = []
    goals_per_SoT = []
    avg_shot_distance = []
    free_kick_shots = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue
        shots_element = row.find('td', {'data-stat': 'shots'})
        shots_on_target_element = row.find('td', {'data-stat': 'shots_on_target'})
        non_pen_xG_per_shot_element = row.find('td', {'data-stat': 'npxg_per_shot'})
        goals_minus_xG_element = row.find('td', {'data-stat': 'xg_net'})
        non_pen_goals_minus_non_pen_xG_element = row.find('td', {'data-stat': 'npxg_net'})
        SoT_percentage_element = row.find('td', {'data-stat': 'shots_on_target_pct'})
        goals_per_shot_element = row.find('td', {'data-stat': 'goals_per_shot'})
        goals_per_SoT_element = row.find('td', {'data-stat': 'goals_per_shot_on_target'})
        avg_shot_distance_element = row.find('td', {'data-stat': 'average_shot_distance'})
        free_kick_shots_element = row.find('td', {'data-stat': 'shots_free_kicks'})

        team1 = clean_stat(safe_get_text(team_element))
        shot = clean_stat(safe_get_text(shots_element))
        SoT = clean_stat(safe_get_text(shots_on_target_element))
        npxg_per_shot = clean_stat(safe_get_text(non_pen_xG_per_shot_element))
        g_minus_xg = clean_stat(safe_get_text(goals_minus_xG_element))
        npg_minus_npxg = clean_stat(safe_get_text(non_pen_goals_minus_non_pen_xG_element))
        SoT_percentage1 = clean_stat(safe_get_text(SoT_percentage_element))
        goals_per_shot1 = clean_stat(safe_get_text(goals_per_shot_element))
        goals_per_SoT1 = clean_stat(safe_get_text(goals_per_SoT_element))
        avg_shot_distance1 = clean_stat(safe_get_text(avg_shot_distance_element))
        free_kick_shots1 = clean_stat(safe_get_text(free_kick_shots_element))
        
        team.append(team1)
        shots.append(shot)
        shots_on_target.append(SoT)
        npxG_per_shot.append(npxg_per_shot)
        G_minus_xG.append(g_minus_xg)
        npG_minus_npxG.append(npg_minus_npxg)
        SoT_percentage.append(SoT_percentage1)
        goals_per_shot.append(goals_per_shot1)
        goals_per_SoT.append(goals_per_SoT1)
        avg_shot_distance.append(avg_shot_distance1)
        free_kick_shots.append(free_kick_shots1)
        
        
    if team:
        dict_football = {'Team': team, 'Shots': shots, 'Shots on Target': shots_on_target,
                         'Non Pen xG per Shot': npxG_per_shot, 'Goals minus xG': G_minus_xG,
                         'Non Pen Goals minus Non Pen xG': npG_minus_npxG,
                         'Shot on Target Percentage': SoT_percentage,
                         'Goals per Shot': goals_per_shot,
                         'Goals per Shot on Target': goals_per_SoT,
                         'Avg Shot Distance': avg_shot_distance,
                         'Free Kick Shots': free_kick_shots}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame()
        
    
def get_passing_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/passing/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_passing'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_passing'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    short_passes_completed = []
    short_passes_attempted = []
    medium_passes_completed = []
    medium_passes_attempted = []
    long_passes_completed =[]
    long_passes_attempted = []
    xA = []
    assists_minus_xAG = []
    key_passes = []
    pass_into_final_third = []
    pass_into_pen_area = []
    cross_into_pen_area = []
    passes_completed = []
    passes_attempted = []
    pass_completion = []
    total_passing_distance = []
    prog_passing_distance = []
    short_pass_completion = []
    medium_pass_completion = []
    long_pass_completion = []
    
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue
        short_passes_completed_element = row.find('td', {'data-stat': 'passes_completed_short'})
        short_passes_attempted_element = row.find('td', {'data-stat': 'passes_short'})
        medium_passes_completed_element = row.find('td', {'data-stat': 'passes_completed_medium'})
        medium_passes_attempted_element = row.find('td', {'data-stat': 'passes_medium'})
        long_passes_completed_element = row.find('td', {'data-stat': 'passes_completed_long'})
        long_passes_attempted_element = row.find('td', {'data-stat': 'passes_long'})
        xA_element = row.find('td', {'data-stat': 'pass_xa'})
        assists_minus_xAG_element = row.find('td', {'data-stat': 'xg_assist_net'})
        key_passes_element = row.find('td', {'data-stat': 'assisted_shots'})
        pass_into_final_third_element = row.find('td', {'data-stat': 'passes_into_final_third'})
        pass_into_pen_area_element = row.find('td', {'data-stat': 'passes_into_penalty_area'})
        cross_into_pen_area_element = row.find('td', {'data-stat': 'crosses_into_penalty_area'})
        passes_completed_element = row.find('td', {'data-stat': 'passes_completed'})
        passes_attempted_element = row.find('td', {'data-stat': 'passes'})
        pass_completion_element = row.find('td', {'data-stat': 'passes_pct'})
        total_passing_distance_element = row.find('td', {'data-stat': 'passes_total_distance'})
        prog_passing_distance_element = row.find('td', {'data-stat': 'passes_progressive_distance'})
        short_pass_completion_element = row.find('td', {'data-stat': 'passes_pct_short'})
        medium_pass_completion_element = row.find('td', {'data-stat': 'passes_pct_medium'})
        long_pass_completion_element = row.find('td', {'data-stat': 'passes_pct_long'})
        
        team1 = clean_stat(safe_get_text(team_element))
        short_passes_completed1 = clean_stat(safe_get_text(short_passes_completed_element))
        short_passes_attempted1 = clean_stat(safe_get_text(short_passes_attempted_element))
        medium_passes_completed1 = clean_stat(safe_get_text(medium_passes_completed_element))
        medium_passes_attempted1 = clean_stat(safe_get_text(medium_passes_attempted_element))
        long_passes_completed1 = clean_stat(safe_get_text(long_passes_completed_element))
        long_passes_attempted1 = clean_stat(safe_get_text(long_passes_attempted_element))
        xA1 = clean_stat(safe_get_text(xA_element))
        assists_minus_xAG1 = clean_stat(safe_get_text(assists_minus_xAG_element))
        key_passes1 = clean_stat(safe_get_text(key_passes_element))
        pass_into_final_third1 = clean_stat(safe_get_text(pass_into_final_third_element))
        pass_into_pen_area1 = clean_stat(safe_get_text(pass_into_pen_area_element))
        cross_into_pen_area1 = clean_stat(safe_get_text(cross_into_pen_area_element))
        passes_completed1 = clean_stat(safe_get_text(passes_completed_element))
        passes_attempted1 = clean_stat(safe_get_text(passes_attempted_element))
        pass_completion1 = clean_stat(safe_get_text(pass_completion_element))
        total_passing_distance1 = clean_stat(safe_get_text(total_passing_distance_element))
        prog_passing_distance1 = clean_stat(safe_get_text(prog_passing_distance_element))
        short_pass_completion1 = clean_stat(safe_get_text(short_pass_completion_element))
        medium_pass_completion1 = clean_stat(safe_get_text(medium_pass_completion_element))
        long_pass_completion1 = clean_stat(safe_get_text(long_pass_completion_element))
        
        team.append(team1)
        short_passes_completed.append(short_passes_completed1)
        short_passes_attempted.append(short_passes_attempted1)
        medium_passes_completed.append(medium_passes_completed1)
        medium_passes_attempted.append(medium_passes_attempted1)
        long_passes_completed.append(long_passes_completed1)
        long_passes_attempted.append(long_passes_attempted1)
        xA.append(xA1)
        assists_minus_xAG.append(assists_minus_xAG1)
        key_passes.append(key_passes1)
        pass_into_final_third.append(pass_into_final_third1)
        pass_into_pen_area.append(pass_into_pen_area1)
        cross_into_pen_area.append(cross_into_pen_area1)
        passes_completed.append(passes_completed1)
        passes_attempted.append(passes_attempted1)
        pass_completion.append(pass_completion1)
        total_passing_distance.append(total_passing_distance1)
        prog_passing_distance.append(prog_passing_distance1)
        short_pass_completion.append(short_pass_completion1)
        medium_pass_completion.append(medium_pass_completion1)
        long_pass_completion.append(long_pass_completion1)
        
    if team:
        dict_football = {'Team': team, 'Short Pass': short_passes_completed, 'Short Pass Attempted': short_passes_attempted,
                         'Medium Pass': medium_passes_completed, 'Medium Pass Attempted': medium_passes_attempted,
                         'Long Pass': long_passes_completed, 'Long Pass Attempted': long_passes_attempted,
                         'xA': xA, 'Assists minus xAG': assists_minus_xAG, 'Key Passes': key_passes,
                         'Pass into final third': pass_into_final_third, 'Pass into Pen Area': pass_into_pen_area,
                         'Cross into Pen Area': cross_into_pen_area,
                         'Passes Completed': passes_completed,
                         'Passes Attempted': passes_attempted,
                         'Pass Completion': pass_completion,
                         'Total Passing Distance': total_passing_distance,
                         'Progressive Passing Distance': prog_passing_distance,
                         'Short Pass Completion': short_pass_completion,
                         'Medium Pass Completion': medium_pass_completion,
                         'Long Pass Completion': long_pass_completion}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 

def get_gca_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/gca/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_gca'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_gca'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    sca = []
    gca = []
    sca_live_pass = []
    sca_dead_pass = []
    sca_take_on = []
    sca_shot = []
    sca_foul_drawn = []
    sca_defensive_action = []
    gca_live_pass = []
    gca_dead_pass = []
    gca_take_on = []
    gca_shot = []
    gca_foul_drawn = []
    gca_defensive_action = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue 
        sca_element = row.find('td', {'data-stat': 'sca'})
        gca_element = row.find('td', {'data-stat': 'gca'})
        sca_live_pass_element = row.find('td', {'data-stat': 'sca_passes_live'})
        sca_dead_pass_element = row.find('td', {'data-stat': 'sca_passes_dead'})
        sca_take_on_element = row.find('td', {'data-stat': 'sca_take_ons'})
        sca_shot_element = row.find('td', {'data-stat': 'sca_shots'})
        sca_foul_drawn_element = row.find('td', {'data-stat': 'sca_fouled'})
        sca_defensive_action_element = row.find('td', {'data-stat': 'sca_defense'})
        gca_live_pass_element = row.find('td', {'data-stat': 'gca_passes_live'})
        gca_dead_pass_element = row.find('td', {'data-stat': 'gca_passes_dead'})
        gca_take_on_element = row.find('td', {'data-stat': 'gca_take_ons'})
        gca_shot_element = row.find('td', {'data-stat': 'gca_shots'})
        gca_foul_drawn_element = row.find('td', {'data-stat': 'gca_fouled'})
        gca_defensive_action_element = row.find('td', {'data-stat': 'gca_defense'})
        
        team1 = clean_stat(safe_get_text(team_element))
        sca1 = clean_stat(safe_get_text(sca_element))
        gca1 = clean_stat(safe_get_text(gca_element))
        sca_live_pass1 = clean_stat(safe_get_text(sca_live_pass_element))
        sca_dead_pass1 = clean_stat(safe_get_text(sca_dead_pass_element))
        sca_take_on1 = clean_stat(safe_get_text(sca_take_on_element))
        sca_shot1 = clean_stat(safe_get_text(sca_shot_element))
        sca_foul_drawn1 = clean_stat(safe_get_text(sca_foul_drawn_element))
        sca_defensive_action1 = clean_stat(safe_get_text(sca_defensive_action_element))
        gca_live_pass1 = clean_stat(safe_get_text(gca_live_pass_element))
        gca_dead_pass1 = clean_stat(safe_get_text(gca_dead_pass_element))
        gca_take_on1 = clean_stat(safe_get_text(gca_take_on_element))
        gca_shot1 = clean_stat(safe_get_text(gca_shot_element))
        gca_foul_drawn1 = clean_stat(safe_get_text(gca_foul_drawn_element))
        gca_defensive_action1 = clean_stat(safe_get_text(gca_defensive_action_element))
                                    
        team.append(team1)
        sca.append(sca1)
        gca.append(gca1)
        sca_live_pass.append(sca_live_pass1)
        sca_dead_pass.append(sca_dead_pass1)
        sca_take_on.append(sca_take_on1)
        sca_shot.append(sca_shot1)
        sca_foul_drawn.append(sca_foul_drawn1)
        sca_defensive_action.append(sca_defensive_action1)
        gca_live_pass.append(gca_live_pass1)
        gca_dead_pass.append(gca_dead_pass1)
        gca_take_on.append(gca_take_on1)
        gca_shot.append(gca_shot1)
        gca_foul_drawn.append(gca_foul_drawn1)
        gca_defensive_action.append(gca_defensive_action1)
        
        
    if team:
        dict_football = {'Team': team, 'Shot Creation Actions': sca,
                         'Goal Creation Actions': gca,
                         'SCA From Live Pass': sca_live_pass,
                         'SCA From Dead Pass': sca_dead_pass,
                         'SCA From Take On': sca_take_on,
                         'SCA From Shot': sca_shot,
                         'SCA From Foul Drawn': sca_foul_drawn,
                         'SCA From Defensive Action': sca_defensive_action,
                         'GCA From Live Pass': gca_live_pass,
                         'GCA From Dead Pass': gca_dead_pass,
                         'GCA From Take On': gca_take_on,
                         'GCA From Shot': gca_shot,
                         'GCA From Foul Drawn': gca_foul_drawn,
                         'GCA From Defensive Action': gca_defensive_action}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 
    
def get_defence_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/defense/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_defense'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_defense'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    tackles = []
    tackles_def_3rd = []
    tackles_won = []
    dribblers_tackled = []
    dribbles_challenged =[]
    blocked_shots = []
    blocked_passes = []
    interceptions = []
    clearances = []
    errors = []
    tackles_mid_3rd = []
    tackles_att_3rd = []
    dribblers_tackled_pct = []
    challenges_lost = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue
        tackles_element = row.find('td', {'data-stat': 'tackles'})
        tackles_def_3rd_element = row.find('td', {'data-stat': 'tackles_def_3rd'})
        tackles_won_element = row.find('td', {'data-stat': 'tackles_won'})
        dribblers_tackled_element = row.find('td', {'data-stat': 'challenge_tackles'})
        dribbles_challenged_element = row.find('td', {'data-stat': 'challenges'})
        blocked_shots_element = row.find('td', {'data-stat': 'blocked_shots'})
        blocked_passes_element = row.find('td', {'data-stat': 'blocked_passes'})
        interceptions_element = row.find('td', {'data-stat': 'interceptions'})
        clearances_element = row.find('td', {'data-stat': 'clearances'})
        errors_element = row.find('td', {'data-stat': 'errors'})
        tackles_mid_3rd_element = row.find('td', {'data-stat': 'tackles_mid_3rd'})
        tackles_att_3rd_element = row.find('td', {'data-stat': 'tackles_att_3rd'})
        dribblers_tackled_pct_element = row.find('td', {'data-stat': 'challenge_tackles_pct'})
        challenges_lost_element = row.find('td', {'data-stat': 'challenges_lost'})
        
        team1 = clean_stat(safe_get_text(team_element))
        tackles1 = clean_stat(safe_get_text(tackles_element))
        tackles_def_3rd1 = clean_stat(safe_get_text(tackles_def_3rd_element))
        tackles_won1 = clean_stat(safe_get_text(tackles_won_element))
        dribblers_tackled1 = clean_stat(safe_get_text(dribblers_tackled_element))
        dribbles_challenged1 = clean_stat(safe_get_text(dribbles_challenged_element))
        blocked_shots1 = clean_stat(safe_get_text(blocked_shots_element))
        blocked_passes1 = clean_stat(safe_get_text(blocked_passes_element))
        interceptions1 = clean_stat(safe_get_text(interceptions_element))
        clearances1 = clean_stat(safe_get_text(clearances_element))
        errors1 = clean_stat(safe_get_text(errors_element))
        tackles_mid_3rd1 = clean_stat(safe_get_text(tackles_mid_3rd_element))
        tackles_att_3rd1 = clean_stat(safe_get_text(tackles_att_3rd_element))
        dribblers_tackled_pct1 = clean_stat(safe_get_text(dribblers_tackled_pct_element))
        challenges_lost1 = clean_stat(safe_get_text(challenges_lost_element))
        
        team.append(team1)
        tackles.append(tackles1)
        tackles_def_3rd.append(tackles_def_3rd1)
        tackles_won.append(tackles_won1)
        dribblers_tackled.append(dribblers_tackled1)
        dribbles_challenged.append(dribbles_challenged1)
        blocked_shots.append(blocked_shots1)
        blocked_passes.append(blocked_passes1)
        interceptions.append(interceptions1)
        clearances.append(clearances1)
        errors.append(errors1)
        tackles_mid_3rd.append(tackles_mid_3rd1)
        tackles_att_3rd.append(tackles_att_3rd1)
        dribblers_tackled_pct.append(dribblers_tackled_pct1)
        challenges_lost.append(challenges_lost1)
        
    if team:
        dict_football = {'Team': team, 'Tackles': tackles, 'Tackles in Def 3rd': tackles_def_3rd, 'Tackles Won': tackles_won,
                         'Dribblers Tackled': dribblers_tackled, 'Dribbles Challenged': dribbles_challenged,
                         'Blocked Shots': blocked_shots, 'Blocked Passes': blocked_passes,
                         'Interceptions': interceptions, 'Clearances': clearances, 'Errors': errors,
                         'Tackles in Mid 3rd': tackles_mid_3rd,
                         'Tackles in Att 3rd': tackles_att_3rd,
                         'Dribblers Tackled Percentage': dribblers_tackled_pct,
                         'Challenges Lost': challenges_lost}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 
    
def get_possession_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/possession/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_possession'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_possession'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    touches_attacking_third = []
    touches_pen = []
    take_ons_attempted = []
    take_ons_won = []
    carries = []
    carries_into_final_third = []
    carries_into_pen = []
    miscontrols = []
    dispossessed = []
    touches_def_pen = []
    touches_def_3rd = []
    touches_mid_3rd = []
    take_on_win_pct = []
    take_on_tackled = []
    take_on_tackled_pct = []
    carries_total_distance = []
    prog_carries_distance = []
    passes_received = []
    prog_passes_received = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue 
        touches_attacking_third_element = row.find('td', {'data-stat': 'touches_att_3rd'})
        touches_pen_element = row.find('td', {'data-stat': 'touches_att_pen_area'})
        take_ons_attempted_element = row.find('td', {'data-stat': 'take_ons'})
        take_ons_won_element = row.find('td', {'data-stat': 'take_ons_won'})
        carries_element = row.find('td', {'data-stat': 'carries'})
        carries_into_final_third_element = row.find('td', {'data-stat': 'carries_into_final_third'})
        carries_into_pen_element = row.find('td', {'data-stat': 'carries_into_penalty_area'})
        miscontrols_element = row.find('td', {'data-stat': 'miscontrols'})
        dispossessed_element = row.find('td', {'data-stat': 'dispossessed'})
        touches_def_pen_element = row.find('td', {'data-stat': 'touches_def_pen_area'})
        touches_def_3rd_element = row.find('td', {'data-stat': 'touches_def_3rd'})
        touches_mid_3rd_element = row.find('td', {'data-stat': 'touches_mid_3rd'})
        take_on_win_pct_element = row.find('td', {'data-stat': 'take_ons_won_pct'})
        take_on_tackled_element = row.find('td', {'data-stat': 'take_ons_tackled'})
        take_on_tackled_pct_element = row.find('td', {'data-stat': 'take_ons_tackled_pct'})
        carries_total_distance_element = row.find('td', {'data-stat': 'carries_distance'})
        prog_carries_distance_element = row.find('td', {'data-stat': 'carries_progressive_distance'})
        passes_received_element = row.find('td', {'data-stat': 'passes_received'})
        prog_passes_received_element = row.find('td', {'data-stat': 'progressive_passes_received'})
        
        team1 = clean_stat(safe_get_text(team_element))
        touches_attacking_third1 = clean_stat(safe_get_text(touches_attacking_third_element))
        touches_pen1 = clean_stat(safe_get_text(touches_pen_element))
        take_ons_attempted1 = clean_stat(safe_get_text(take_ons_attempted_element))
        take_ons_won1 = clean_stat(safe_get_text(take_ons_won_element))
        carries1 = clean_stat(safe_get_text(carries_element))
        carries_into_final_third1 = clean_stat(safe_get_text(carries_into_final_third_element))
        carries_into_pen1 = clean_stat(safe_get_text(carries_into_pen_element))
        miscontrols1 = clean_stat(safe_get_text(miscontrols_element))
        dispossessed1 = clean_stat(safe_get_text(dispossessed_element))
        touches_def_pen1 = clean_stat(safe_get_text(touches_def_pen_element))
        touches_def_3rd1 = clean_stat(safe_get_text(touches_def_3rd_element))
        touches_mid_3rd1 = clean_stat(safe_get_text(touches_mid_3rd_element))
        take_on_win_pct1 = clean_stat(safe_get_text(take_on_win_pct_element))
        take_on_tackled1 = clean_stat(safe_get_text(take_on_tackled_element))
        take_on_tackled_pct1 = clean_stat(safe_get_text(take_on_tackled_pct_element))
        carries_total_distance1 = clean_stat(safe_get_text(carries_total_distance_element))
        prog_carries_distance1 = clean_stat(safe_get_text(prog_carries_distance_element))
        passes_received1 = clean_stat(safe_get_text(passes_received_element))
        prog_passes_received1 = clean_stat(safe_get_text(prog_passes_received_element))
        
        team.append(team1)
        touches_attacking_third.append(touches_attacking_third1)
        touches_pen.append(touches_pen1)
        take_ons_attempted.append(take_ons_attempted1)
        take_ons_won.append(take_ons_won1)
        carries.append(carries1)
        carries_into_final_third.append(carries_into_final_third1)
        carries_into_pen.append(carries_into_pen1)
        miscontrols.append(miscontrols1)
        dispossessed.append(dispossessed1)
        touches_def_pen.append(touches_def_pen1)
        touches_def_3rd.append(touches_def_3rd1)
        touches_mid_3rd.append(touches_mid_3rd1)
        take_on_win_pct.append(take_on_win_pct1)
        take_on_tackled.append(take_on_tackled1)
        take_on_tackled_pct.append(take_on_tackled_pct1)
        carries_total_distance.append(carries_total_distance1)
        prog_carries_distance.append(prog_carries_distance1)
        passes_received.append(passes_received1)
        prog_passes_received.append(prog_passes_received1)
        
    if team:
        dict_football = {'Team': team, 'Touches in Attacking Third': touches_attacking_third, 
                         'Touches in Pen Area': touches_pen, 'Take Ons Attempted': take_ons_attempted,
                         'Take Ons Won': take_ons_won, 'Carries': carries,
                         'Carries into Final Third': carries_into_final_third, 'Carries into Penalty Area': carries_into_pen,
                         'Miscontrols': miscontrols, 'Dispossessed': dispossessed,
                         'Touches in Defensive Pen Area': touches_def_pen,
                         'Touches in Defensive Third': touches_def_3rd,
                         'Touches in Midfield Third': touches_mid_3rd,
                         'Take Ons Won Percentage': take_on_win_pct,
                         'Take Ons Tackled': take_on_tackled,
                         'Take Ons Tackled Percentage': take_on_tackled_pct,
                         'Total Distance Carried': carries_total_distance,
                         'Progressive Carries Distance': prog_carries_distance,
                         'Passes Received': passes_received,
                         'Progressive Passes Received': prog_passes_received}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 
        
        
def get_playingtime_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/playingtime/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_playing_time'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_playing_time'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    ppm = []
    onG = []
    onGA = []
    onxG = []
    onxGA = []
    on_off = []
    on_off_xG = []
    subs = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue
        ppm_element = row.find('td', {'data-stat': 'points_per_game'})
        onG_element = row.find('td', {'data-stat': 'on_goals_for'})
        onGA_element = row.find('td', {'data-stat': 'on_goals_against'})
        onxG_element = row.find('td', {'data-stat': 'on_xg_for'})
        onxGA_element = row.find('td', {'data-stat': 'on_xg_against'})
        on_off_element = row.find('td', {'data-stat': 'plus_minus'})
        on_off_xG_element = row.find('td', {'data-stat': 'xg_plus_minus'})
        subs_element = row.find('td', {'data-stat': 'games_subs'})
        
        team1 = clean_stat(safe_get_text(team_element))
        ppm1 = clean_stat(safe_get_text(ppm_element))
        onG1 = clean_stat(safe_get_text(onG_element))
        onGA1 = clean_stat(safe_get_text(onGA_element))
        onxG1 = clean_stat(safe_get_text(onxG_element))
        onxGA1 = clean_stat(safe_get_text(onxGA_element))
        on_off1 = clean_stat(safe_get_text(on_off_element))
        on_off_xG1 = clean_stat(safe_get_text(on_off_xG_element))
        subs1 = clean_stat(safe_get_text(subs_element))
        
        team.append(team1)
        ppm.append(ppm1)
        onG.append(onG1)
        onGA.append(onGA1)
        onxG.append(onxG1)
        onxGA.append(onxGA1)
        on_off.append(on_off1)
        on_off_xG.append(on_off_xG1)
        subs.append(subs1)
        
    if team:
        dict_football = {'Team': team, 'Points Per Match': ppm, 'Goals whilst on Pitch': onG,
                         'Goals Conceded whilst on Pitch': onGA, 'xG whilst on Pitch': onxG,
                         'xG Conceded whilst on Pitch': onxGA, 'Net Goals On or Off Pitch': on_off,
                         'Net xG On or Off Pitch': on_off_xG,
                         'Substitutes': subs}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 
        
        
def get_misc_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/misc/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_misc'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_misc'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    fouls_comitted = []
    fouls_drawn = []
    offsides = []
    pens_won = []
    pens_conceded = []
    own_goals = []
    recoveries = []
    aerials_won = []
    aerials_lost = []
    aerials_won_pct = []
    second_yellow = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue
        fouls_comitted_element = row.find('td', {'data-stat': 'fouls'})
        fouls_drawn_element = row.find('td', {'data-stat': 'fouled'})
        offsides_element = row.find('td', {'data-stat': 'offsides'})
        pens_won_element = row.find('td', {'data-stat': 'pens_won'})
        pens_conceded_element = row.find('td', {'data-stat': 'pens_conceded'})
        own_goals_element = row.find('td', {'data-stat': 'own_goals'})
        recoveries_element = row.find('td', {'data-stat': 'ball_recoveries'})
        aerials_won_element = row.find('td', {'data-stat': 'aerials_won'})
        aerials_lost_element = row.find('td', {'data-stat': 'aerials_lost'})
        aerials_won_pct_element = row.find('td', {'data-stat': 'aerials_won_pct'})
        second_yellow_element = row.find('td', {'data-stat': 'cards_yellow_red'})
        
        team1 = clean_stat(safe_get_text(team_element))
        fouls_comitted1 = clean_stat(safe_get_text(fouls_comitted_element))
        fouls_drawn1 = clean_stat(safe_get_text(fouls_drawn_element))
        offsides1 = clean_stat(safe_get_text(offsides_element))
        pens_won1 = clean_stat(safe_get_text(pens_won_element))
        pens_conceded1 = clean_stat(safe_get_text(pens_conceded_element))
        own_goals1 = clean_stat(safe_get_text(own_goals_element))
        recoveries1 = clean_stat(safe_get_text(recoveries_element))
        aerials_won1 = clean_stat(safe_get_text(aerials_won_element))
        aerials_lost1 = clean_stat(safe_get_text(aerials_lost_element))
        aerials_won_pct1 = clean_stat(safe_get_text(aerials_won_pct_element))
        second_yellow1 = clean_stat(safe_get_text(second_yellow_element))
        
        team.append(team1)
        fouls_comitted.append(fouls_comitted1)
        fouls_drawn.append(fouls_drawn1)
        offsides.append(offsides1)
        pens_won.append(pens_won1)
        pens_conceded.append(pens_conceded1)
        own_goals.append(own_goals1)
        recoveries.append(recoveries1)
        aerials_won.append(aerials_won1)
        aerials_lost.append(aerials_lost1)
        aerials_won_pct.append(aerials_won_pct1)
        second_yellow.append(second_yellow1)
        
    if team:
        dict_football = {'Team': team, 'Fouls Comitted': fouls_comitted, 'Fouls Drawn': fouls_drawn,
                         'Offsides': offsides, 'Penalties Won': pens_won,
                         'Penalties Conceded': pens_conceded, 'Own Goals': own_goals, 'Recoveries': recoveries,
                         'Aerial Duels Won': aerials_won, 'Aerial Duels Lost': aerials_lost,
                         'Aerial Duels Won Percentage': aerials_won_pct,
                         'Second Yellows': second_yellow}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 


def get_goalkeeping_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/keepers/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_keeper'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_keeper'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    goals_against = []
    shots_on_target_against = []
    saves = []
    clean_sheets = []
    pens_faced = []
    pens_scored_against = []
    pens_saved = []
    pens_missed_against = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue
        goals_against_element = row.find('td', {'data-stat': 'gk_goals_against'})
        shots_on_target_against_element = row.find('td', {'data-stat': 'gk_shots_on_target_against'})
        saves_element = row.find('td', {'data-stat': 'gk_saves'})
        clean_sheets_element = row.find('td', {'data-stat': 'gk_clean_sheets'})
        pens_faced_element = row.find('td', {'data-stat': 'gk_pens_att'})
        pens_scored_against_element = row.find('td', {'data-stat': 'gk_pens_allowed'})
        pens_saved_element = row.find('td', {'data-stat': 'gk_pens_saved'})
        pens_missed_against_element = row.find('td', {'data-stat': 'gk_pens_missed'})

        team1 = clean_stat(safe_get_text(team_element))
        goals_against1 = clean_stat(safe_get_text(goals_against_element))
        shots_on_target_against1 = clean_stat(safe_get_text(shots_on_target_against_element))
        saves1 = clean_stat(safe_get_text(saves_element))
        clean_sheets1 = clean_stat(safe_get_text(clean_sheets_element))
        pens_faced1 = clean_stat(safe_get_text(pens_faced_element))
        pens_scored_against1 = clean_stat(safe_get_text(pens_scored_against_element))
        pens_saved1 = clean_stat(safe_get_text(pens_saved_element))
        pens_missed_against1 = clean_stat(safe_get_text(pens_missed_against_element))

        team.append(team1)
        goals_against.append(goals_against1)
        shots_on_target_against.append(shots_on_target_against1)
        saves.append(saves1)
        clean_sheets.append(clean_sheets1)
        pens_faced.append(pens_faced1)
        pens_scored_against.append(pens_scored_against1)
        pens_saved.append(pens_saved1)
        pens_missed_against.append(pens_missed_against1)
                
    if team:
        dict_football = {'Team': team, 'Goals Against': goals_against, 'SoTA': shots_on_target_against,
                         'Saves': saves, 'Clean Sheets': clean_sheets, 'Penalties Faced': pens_faced,
                         'Penalties Scored Against': pens_scored_against, 'Penalties Saved': pens_saved,
                         'Penalties Missed Against': pens_missed_against}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame() 


def get_advanced_goalkeeping_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/keepersadv/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_keeper_adv'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_keeper_adv'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    free_kick_goals_against = []
    corner_goals_against = []
    own_goals_against = []
    PSxG = []
    PSxG_per_SoT = []
    PSxG_plus_or_minus = []
    launches_completed = []
    launches_attempted = []
    launch_completion_percentage = []
    gk_passes = []
    gk_throws = []
    launch_percentage = []
    gk_avg_pass_length = []
    goal_kicks = []
    goal_kicks_launched_percentage = []
    goal_kick_avg_length = []
    crosses_faced = []
    crosses_stopped = []
    crosses_stopped_percentage = []
    sweeper_actions = []
    sweeper_avg_distance = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue
        free_kick_goals_against_element = row.find('td', {'data-stat': 'gk_free_kick_goals_against'})
        corner_goals_against_element = row.find('td', {'data-stat': 'gk_corner_kick_goals_against'})
        own_goals_against_element = row.find('td', {'data-stat': 'gk_own_goals_against'})
        PSxG_element = row.find('td', {'data-stat': 'gk_psxg'})
        PSxG_per_SoT_element = row.find('td', {'data-stat': 'gk_psnpxg_per_shot_on_target_against'})
        PSxG_plus_or_minus_element = row.find('td', {'data-stat': 'gk_psxg_net'})
        launches_completed_element = row.find('td', {'data-stat': 'gk_passes_completed_launched'})
        launches_attempted_element = row.find('td', {'data-stat': 'gk_passes_launched'})
        launch_completion_percentage_element = row.find('td', {'data-stat': 'gk_passes_pct_launched'})
        gk_passes_element = row.find('td', {'data-stat': 'gk_passes'})
        gk_throws_element = row.find('td', {'data-stat': 'gk_passes_throws'})
        launch_percentage_element = row.find('td', {'data-stat': 'gk_pct_passes_launched'})
        gk_avg_pass_length_element = row.find('td', {'data-stat': 'gk_passes_length_avg'})
        goal_kicks_element = row.find('td', {'data-stat': 'gk_goal_kicks'})
        goal_kicks_launched_percentage_element = row.find('td', {'data-stat': 'gk_pct_goal_kicks_launched'})
        goal_kick_avg_length_element = row.find('td', {'data-stat': 'gk_goal_kick_length_avg'})
        crosses_faced_element = row.find('td', {'data-stat': 'gk_crosses'})
        crosses_stopped_element = row.find('td', {'data-stat': 'gk_crosses_stopped'})
        crosses_stopped_percentage_element = row.find('td', {'data-stat': 'gk_crosses_stopped_pct'})
        sweeper_actions_element = row.find('td', {'data-stat': 'gk_def_actions_outside_pen_area'})
        sweeper_avg_distance_element = row.find('td', {'data-stat': 'gk_avg_distance_def_actions'})

        team1 = clean_stat(safe_get_text(team_element))
        free_kick_goals_against1 = clean_stat(safe_get_text(free_kick_goals_against_element))
        corner_goals_against1 = clean_stat(safe_get_text(corner_goals_against_element))
        own_goals_against1 = clean_stat(safe_get_text(own_goals_against_element))
        PSxG1 = clean_stat(safe_get_text(PSxG_element))
        PSxG_per_SoT1 = clean_stat(safe_get_text(PSxG_per_SoT_element))
        PSxG_plus_or_minus1 = clean_stat(safe_get_text(PSxG_plus_or_minus_element))
        launches_completed1 = clean_stat(safe_get_text(launches_completed_element))
        launches_attempted1 = clean_stat(safe_get_text(launches_attempted_element))
        launch_completion_percentage1 = clean_stat(safe_get_text(launch_completion_percentage_element))
        gk_passes1 = clean_stat(safe_get_text(gk_passes_element))
        gk_throws1 = clean_stat(safe_get_text(gk_throws_element))
        launch_percentage1 = clean_stat(safe_get_text(launch_percentage_element))
        gk_avg_pass_length1 = clean_stat(safe_get_text(gk_avg_pass_length_element))
        goal_kicks1 = clean_stat(safe_get_text(goal_kicks_element))
        goal_kicks_launched_percentage1 = clean_stat(safe_get_text(goal_kicks_launched_percentage_element))
        goal_kick_avg_length1 = clean_stat(safe_get_text(goal_kick_avg_length_element))
        crosses_faced1 = clean_stat(safe_get_text(crosses_faced_element))
        crosses_stopped1 = clean_stat(safe_get_text(crosses_stopped_element))
        crosses_stopped_percentage1 = clean_stat(safe_get_text(crosses_stopped_percentage_element))
        sweeper_actions1 = clean_stat(safe_get_text(sweeper_actions_element))
        sweeper_avg_distance1 = clean_stat(safe_get_text(sweeper_avg_distance_element))
        
        team.append(team1)
        free_kick_goals_against.append(free_kick_goals_against1)
        corner_goals_against.append(corner_goals_against1)
        own_goals_against.append(own_goals_against1)
        PSxG.append(PSxG1)
        PSxG_per_SoT.append(PSxG_per_SoT1)
        PSxG_plus_or_minus.append(PSxG_plus_or_minus1)
        launches_completed.append(launches_completed1)
        launches_attempted.append(launches_attempted1)
        launch_completion_percentage.append(launch_completion_percentage1)
        gk_passes.append(gk_passes1)
        gk_throws.append(gk_throws1)
        launch_percentage.append(launch_percentage1)
        gk_avg_pass_length.append(gk_avg_pass_length1)
        goal_kicks.append(goal_kicks1)
        goal_kicks_launched_percentage.append(goal_kicks_launched_percentage1)
        goal_kick_avg_length.append(goal_kick_avg_length1)
        crosses_faced.append(crosses_faced1)
        crosses_stopped.append(crosses_stopped1)
        crosses_stopped_percentage.append(crosses_stopped_percentage1)
        sweeper_actions.append(sweeper_actions1)
        sweeper_avg_distance.append(sweeper_avg_distance1)
        
    if team:
        dict_football = {'Team': team, 'Free Kick Goals Against': free_kick_goals_against,
                         'Corner Goals Against': corner_goals_against, 
                         'Own Goals Against': own_goals_against, 'PSxG': PSxG,
                         'PSxG per Shot on Target': PSxG_per_SoT,
                         'PSxG +/-': PSxG_plus_or_minus, 'Launches Completed': launches_completed,
                         'Launches Attempted': launches_attempted,
                         'Launch Completion Percentage': launch_completion_percentage,
                         'Goalkeeper Passes': gk_passes,
                         'Goalkeeper Throws': gk_throws,
                         'Launch Percentage': launch_percentage,
                         'Goalkeeper Avg Pass Length': gk_avg_pass_length,
                         'Goal Kicks': goal_kicks,
                         'Goal Kicks Launched': goal_kicks_launched_percentage,
                         'Avg Goal Kick Length': goal_kick_avg_length,
                         'Crosses Faced': crosses_faced,
                         'Crosses Stopped': crosses_stopped,
                         'Crosses Stopped Percentage': crosses_stopped_percentage,
                         'Sweeper Actions': sweeper_actions,
                         'Avg Sweeper Distance': sweeper_avg_distance}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame()


def get_pass_type_stats(year):
    web = f'https://fbref.com/en/comps/196/{year}/passing_types/{year}-A-League-Women-Stats'
    print(f"Requesting URL: {web}")
    
    driver = webdriver.Chrome()
    
    try:
        driver.get(web)
        

        content = driver.page_source
        
    finally:
        driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    
    stats_table = soup.find('div', {'id': 'all_stats_squads_passing_types'}).find('table')
    
    if not stats_table:
        print("No table found in 'all_stats_squads_passing_types'")
        return pd.DataFrame()

    rows = stats_table.find('tbody').find_all('tr')
    
    team = []
    live_ball_passes = []
    dead_ball_passes = []
    free_kick_passes = []
    through_balls = []
    switches = []
    crosses = []
    throw_ins = []
    corners = []
    inswinging_corners = []
    outswinging_corners = []
    straight_corners = []
    passes_offside = []
    passes_blocked = []
    
    for row in rows:
        team_element = row.find('th', {'data-stat': 'team'})
        if team_element is None or not team_element.get_text(strip=True):
            continue
        live_ball_passes_element = row.find('td', {'data-stat': 'passes_live'})
        dead_ball_passes_element = row.find('td', {'data-stat': 'passes_dead'})
        free_kick_passes_element = row.find('td', {'data-stat': 'passes_free_kicks'})
        through_balls_element = row.find('td', {'data-stat': 'through_balls'})
        switches_element = row.find('td', {'data-stat': 'passes_switches'})
        crosses_element = row.find('td', {'data-stat': 'crosses'})
        throw_ins_element = row.find('td', {'data-stat': 'throw_ins'})
        corners_element = row.find('td', {'data-stat': 'corner_kicks'})
        inswinging_corners_element = row.find('td', {'data-stat': 'corner_kicks_in'})
        outswinging_corners_element = row.find('td', {'data-stat': 'corner_kicks_out'})
        straight_corners_element = row.find('td', {'data-stat': 'corner_kicks_straight'})
        passes_offside_element = row.find('td', {'data-stat': 'passes_offsides'})
        passes_blocked_element = row.find('td', {'data-stat': 'passes_blocked'})
        
        team1 = clean_stat(safe_get_text(team_element))
        live_ball_passes1 = clean_stat(safe_get_text(live_ball_passes_element))
        dead_ball_passes1 = clean_stat(safe_get_text(dead_ball_passes_element))
        free_kick_passes1 = clean_stat(safe_get_text(free_kick_passes_element))
        through_balls1 = clean_stat(safe_get_text(through_balls_element))
        switches1 = clean_stat(safe_get_text(switches_element))
        crosses1 = clean_stat(safe_get_text(crosses_element))
        throw_ins1 = clean_stat(safe_get_text(throw_ins_element))
        corners1 = clean_stat(safe_get_text(corners_element))
        inswinging_corners1 = clean_stat(safe_get_text(inswinging_corners_element))
        outswinging_corners1 = clean_stat(safe_get_text(outswinging_corners_element))
        straight_corners1 = clean_stat(safe_get_text(straight_corners_element))
        passes_offside1 = clean_stat(safe_get_text(passes_offside_element))
        passes_blocked1 = clean_stat(safe_get_text(passes_blocked_element))
        
        team.append(team1)
        live_ball_passes.append(live_ball_passes1)
        dead_ball_passes.append(dead_ball_passes1)
        free_kick_passes.append(free_kick_passes1)
        through_balls.append(through_balls1)
        switches.append(switches1)
        crosses.append(crosses1)
        throw_ins.append(throw_ins1)
        corners.append(corners1)
        inswinging_corners.append(inswinging_corners1)
        outswinging_corners.append(outswinging_corners1)
        straight_corners.append(straight_corners1)
        passes_offside.append(passes_offside1)
        passes_blocked.append(passes_blocked1)
        
    if team:
        dict_football = {'Team': team, 'Live Ball Passes': live_ball_passes,
                         'Dead Ball Passes': dead_ball_passes,
                         'Free Kick Passes': free_kick_passes,
                         'Through Balls': through_balls,
                         'Switches': switches, 'Crosses': crosses,
                         'Throw Ins': throw_ins, 'Corners': corners,
                         'Inswinging Corners': inswinging_corners,
                         'Outswinging Corners': outswinging_corners,
                         'Straight Corners': straight_corners,
                         'Passes Offside': passes_offside,
                         'Passes Blocked': passes_blocked}
        df_football = pd.DataFrame(dict_football)
        df_football.fillna(0, inplace=True)
        print(f"Data extracted for {year}")
        return df_football
    else:
        print(f"No data extracted for {year}")
        return pd.DataFrame()
        
    









all_data = []  # List to store combined data for each year

for year in years:
    # Collect data from each function for the current year
    standard_stats = get_standard_stats(year)
    shooting_stats = get_shooting_stats(year)
    passing_stats = get_passing_stats(year)
    gca_stats = get_gca_stats(year)
    defence_stats = get_defence_stats(year)
    possession_stats = get_possession_stats(year)
    playingtime_stats = get_playingtime_stats(year)
    misc_stats = get_misc_stats(year)
    goalkeeping_stats = get_goalkeeping_stats(year)
    advanced_goalkeeping_stats = get_advanced_goalkeeping_stats(year)
    pass_type_stats = get_pass_type_stats(year)
    

    
    # Sort and drop duplicates in the main 'standard_stats' DataFrame
    base_df = standard_stats
    # Merge other datasets after deduplication
    for df in [shooting_stats, passing_stats, gca_stats, defence_stats, 
               possession_stats, playingtime_stats, misc_stats,
               goalkeeping_stats, advanced_goalkeeping_stats,
               pass_type_stats]:
        base_df = base_df.merge(df, on='Team', how='left')  # Merge without introducing new duplicates
    
    # Fill NaN values with zeros
    base_df.fillna(0, inplace=True)
    base_df['year'] = year



        
    # Add the year's combined DataFrame to the list
    all_data.append(base_df)
    
    # Delay to avoid rate limiting
    time.sleep(5)


# After collecting and merging data for all years
if all_data:
    # Concatenate all yearly DataFrames into one
    df_final_combined = pd.concat(all_data, ignore_index=True)
    
    # Sort the DataFrame by 'Player' and 'Minutes' (descending order)
    df_final_sorted = df_final_combined.sort_values(by=['Team', 'Minutes'], ascending=[True, False])
    
    # Keep only the last row for each player (based on most recent/maximum 'Minutes')
    df_final_sorted = df_final_sorted.drop_duplicates(subset='Team', keep='last')
    
    # Reset index after removing duplicates
    df_final_sorted.reset_index(drop=True, inplace=True)
    
    # Save the final combined DataFrame to a CSV
    df_final_sorted.to_csv('all_squad_stats_24-25_A-League-Women.csv', index=False)
    print("CSV file created successfully")
else:
    print("No data available to save.")

    
    
    
    
    
    
    
        
        
        
        
        
        