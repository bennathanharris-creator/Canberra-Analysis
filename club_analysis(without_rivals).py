#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 09:41:00 2025

@author: benharris
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np

df = pd.read_csv('all_squad_stats_24-25(A-League-Womens).csv')

# Load in SQL
conn = sqlite3.connect(':memory:')
df.to_sql('league_stats', conn, index=False, if_exists='replace')



# ============================================================================
# GOALS QUERY
# ============================================================================

goals_query = """
SELECT
    (SELECT AVG(Goals) FROM league_stats) AS league_avg_goals,
    (SELECT Goals FROM league_stats WHERE Team = 'Canberra Utd') AS club_goals,
    (SELECT Team FROM league_stats ORDER BY Goals DESC LIMIT 1) AS top_team,
    (SELECT Goals FROM league_stats ORDER BY Goals DESC LIMIT 1) AS top_team_goals;
"""

season_goals = pd.read_sql_query(goals_query, conn)

league_avg = float(season_goals.loc[0, "league_avg_goals"])
club_gls = float(season_goals.loc[0, "club_goals"])
top_tm = season_goals.loc[0, "top_team"]
top_goals = float(season_goals.loc[0, "top_team_goals"])


teams = ["League Average", "Canberra Utd", top_tm]
goals = [league_avg, club_gls, top_goals]

plt.figure(figsize=(8, 5))
bars = plt.bar(teams, goals, color=["lightgrey", "green", "gold"], edgecolor="black")

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, f"{height:.1f}",
             ha="center", va="bottom", fontsize=10, fontweight="bold")

plt.title("Goals", fontsize=14, fontweight="bold")
plt.ylabel("Total Goals", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


# ============================================================================
# PENS QUERY
# ============================================================================

pens_query = """ 
SELECT 
    (SELECT AVG("Non Pen Goals") FROM league_stats) AS league_avg_non_pen_goals,
    (SELECT AVG("Pens Scored") FROM league_stats) AS league_avg_pens_scored,
    (SELECT AVG("Pens Attempted") FROM league_stats) AS league_avg_pens_attempted,

    (SELECT "Non Pen Goals" FROM league_stats WHERE Team = 'Canberra Utd') AS club_non_pen_goals,
    (SELECT "Pens Scored" FROM league_stats WHERE Team = 'Canberra Utd') AS club_pens_scored,
    (SELECT "Pens Attempted" FROM league_stats WHERE Team = 'Canberra Utd') AS club_pens_attempted,
    
    (SELECT Team FROM league_stats ORDER BY "Non Pen Goals" DESC LIMIT 1) AS top_team_1,
    (SELECT Team FROM league_stats ORDER BY "Pens Scored" DESC LIMIT 1) AS top_team_2,
    (SELECT Team FROM league_stats ORDER BY "Pens Attempted" DESC LIMIT 1) AS top_team_3,
    
    (SELECT "Non Pen Goals" FROM league_stats ORDER BY "Non Pen Goals" DESC LIMIT 1) AS top_team_non_pen_goals,
    (SELECT "Pens Scored" FROM league_stats ORDER BY "Pens Scored" DESC LIMIT 1) AS top_team_pens_scored,
    (SELECT "Pens Attempted" FROM league_stats ORDER BY "Pens Attempted" DESC LIMIT 1) AS top_team_pens_attempted;
"""

# Run query
season_pens = pd.read_sql_query(pens_query, conn)

# Extract results
league_avg_npg = float(season_pens.loc[0, "league_avg_non_pen_goals"])
league_avg_ps = float(season_pens.loc[0, "league_avg_pens_scored"])
league_avg_pa = float(season_pens.loc[0, "league_avg_pens_attempted"])

club_npg = float(season_pens.loc[0, "club_non_pen_goals"])
club_ps = float(season_pens.loc[0, "club_pens_scored"])
club_pa = float(season_pens.loc[0, "club_pens_attempted"])

top_team_npg = season_pens.loc[0, "top_team_1"]
top_team_ps = season_pens.loc[0, "top_team_2"]
top_team_pa = season_pens.loc[0, "top_team_3"]

top_npg = float(season_pens.loc[0, "top_team_non_pen_goals"])
top_ps = float(season_pens.loc[0, "top_team_pens_scored"])
top_pa = float(season_pens.loc[0, "top_team_pens_attempted"])

# Prepare data for plotting
categories = ['Non-Pen Goals', 'Pens Scored', 'Pens Attempted']
league_avg = [league_avg_npg, league_avg_ps, league_avg_pa]
club = [club_npg, club_ps, club_pa]
top_team = [top_npg, top_ps, top_pa]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_npg}, {top_team_ps}, {top_team_pa})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Penalties')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# PROGRESSIVE QUERY
# ============================================================================

prog_query = """ 
SELECT
    (SELECT AVG("Prog Carries") FROM league_stats) AS league_avg_prog_carries,
    (SELECT AVG("Prog Passes") FROM league_stats) AS league_avg_prog_passes,

    
    (SELECT "Prog Carries" FROM league_stats WHERE Team = 'Canberra Utd') AS club_prog_carries,
    (SELECT "Prog Passes" FROM league_stats WHERE Team = 'Canberra Utd') AS club_prog_passes,
    
    (SELECT Team FROM league_stats ORDER BY "Prog Carries" DESC LIMIT 1) AS top_team_1,
    (SELECT Team FROM league_stats ORDER BY "Prog Passes" DESC LIMIT 1) AS top_team_2,
    
    (SELECT "Prog Carries" FROM league_stats ORDER BY "Prog Carries" DESC LIMIT 1) AS top_team_prog_carries,
    (SELECT "Prog Passes" FROM league_stats ORDER BY "Prog Passes" DESC LIMIT 1) AS top_team_prog_passes;
"""

prog = pd.read_sql(prog_query, conn)

# Extract results
league_avg_prog_c = float(prog.loc[0, "league_avg_prog_carries"])
league_avg_prog_p = float(prog.loc[0, "league_avg_prog_passes"])


club_prog_c = float(prog.loc[0, "club_prog_carries"])
club_prog_p = float(prog.loc[0, "club_prog_passes"])

top_team_prog_c = prog.loc[0, "top_team_1"]
top_team_prog_p = prog.loc[0, "top_team_2"]

top_prog_c = float(prog.loc[0, "top_team_prog_carries"])
top_prog_p = float(prog.loc[0, "top_team_prog_passes"])

# Prepare data for plotting
categories = ['Prog Carries', 'Prog Passes']
league_avg = [league_avg_prog_c, league_avg_prog_p]
club = [club_prog_c, club_prog_p]
top_team = [top_prog_c, top_prog_p]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_prog_c}, {top_team_prog_p})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Progression')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# ============================================================================
# DISCIPLINARY QUERY
# ============================================================================

disciplinary_query= """ 
SELECT
    (SELECT AVG("Yellows") FROM league_stats) AS league_avg_yellows,
    (SELECT AVG("Reds") FROM league_stats) AS league_avg_reds,

    
    (SELECT "Yellows" FROM league_stats WHERE Team = 'Canberra Utd') AS club_yellows,
    (SELECT "Reds" FROM league_stats WHERE Team = 'Canberra Utd') AS club_reds,
    
    (SELECT Team FROM league_stats ORDER BY "Yellows" DESC LIMIT 1) AS top_team_1,
    (SELECT Team FROM league_stats ORDER BY "Reds" DESC LIMIT 1) AS top_team_2,
    
    (SELECT "Yellows" FROM league_stats ORDER BY "Yellows" DESC LIMIT 1) AS top_team_yellows,
    (SELECT "Reds" FROM league_stats ORDER BY "Reds" DESC LIMIT 1) AS top_team_reds;
"""

disciplinary = pd.read_sql_query(disciplinary_query, conn)

# Extract results
league_avg_yellows = float(disciplinary.loc[0, "league_avg_yellows"])
league_avg_reds = float(disciplinary.loc[0, "league_avg_reds"])


club_yellows = float(disciplinary.loc[0, "club_yellows"])
club_reds = float(disciplinary.loc[0, "club_reds"])

top_team_yellows = disciplinary.loc[0, "top_team_1"]
top_team_reds = disciplinary.loc[0, "top_team_2"]

top_yellows = float(disciplinary.loc[0, "top_team_yellows"])
top_reds = float(disciplinary.loc[0, "top_team_reds"])

# Prepare data for plotting
categories = ['yellows', 'Reds']
league_avg = [league_avg_yellows, league_avg_reds]
club = [club_yellows, club_reds]
top_team = [top_yellows, top_reds]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_yellows}, {top_team_reds})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Disciplinary')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# xG QUERY
# ============================================================================

xG_query = """ 
SELECT
    (SELECT AVG("xG") FROM league_stats) AS league_avg1,
    (SELECT AVG("Non Pen xG") FROM league_stats) AS league_avg2,
    (SELECT AVG("xAG") FROM league_stats) AS league_avg3,
    (SELECT AVG("Goals minus xG") FROM league_stats) AS league_avg4,
    (SELECT AVG("Non Pen Goals minus Non Pen xG") FROM league_stats) AS league_avg5,

    
    (SELECT "xG" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Non Pen xG" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "xAG" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Goals minus xG" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,
    (SELECT "Non Pen Goals minus Non Pen xG" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,

    (SELECT Team FROM league_stats ORDER BY "xG" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Non Pen xG" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "xAG" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Goals minus xG" DESC LIMIT 1) AS top_team4,
    (SELECT Team FROM league_stats ORDER BY "Non Pen Goals minus Non Pen xG" DESC LIMIT 1) AS top_team5,

    (SELECT "xG" FROM league_stats ORDER BY "xG" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Non Pen xG" FROM league_stats ORDER BY "Non Pen xG" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "xAG" FROM league_stats ORDER BY "xAG" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Goals minus xG" FROM league_stats ORDER BY "Goals minus xG" DESC LIMIT 1) AS top_team_stat4,
    (SELECT "Non Pen Goals minus Non Pen xG" FROM league_stats ORDER BY "Non Pen Goals minus Non Pen xG" DESC LIMIT 1) AS top_team_stat5;
"""

xG = pd.read_sql_query(xG_query, conn)

# Extract results
league_avg_xg = float(xG.loc[0, "league_avg1"])
league_avg_npxg = float(xG.loc[0, "league_avg2"])
league_avg_xag = float(xG.loc[0, "league_avg3"])
league_avg_gmxg = float(xG.loc[0, "league_avg4"])
league_avg_npgmnpxg = float(xG.loc[0, "league_avg5"])


club_xg = float(xG.loc[0, "club1"])
club_npxg = float(xG.loc[0, "club2"])
club_xag = float(xG.loc[0, "club3"])
club_gmxg = float(xG.loc[0, "club4"])
club_npgmnpxg = float(xG.loc[0, "club5"])

top_team_xg = xG.loc[0, "top_team1"]
top_team_npxg = xG.loc[0, "top_team2"]
top_team_xag = xG.loc[0, "top_team3"]
top_team_gmxg = xG.loc[0, "top_team4"]
top_team_npgmnpxg = xG.loc[0, "top_team5"]

top_xg = float(xG.loc[0, "top_team_stat1"])
top_npxg = float(xG.loc[0, "top_team_stat2"])
top_xag = float(xG.loc[0, "top_team_stat3"])
top_gmxg = float(xG.loc[0, "top_team_stat4"])
top_npgmnpxg = float(xG.loc[0, "top_team_stat5"])


# Prepare data for plotting
categories = ['xG', 'Non Pen xG', 'xAG', 'Goals minus xG', 'Non Pen Goals minus Non Pen xG']
league_avg = [league_avg_xg, league_avg_npxg, league_avg_xag, league_avg_gmxg, league_avg_npgmnpxg]
club = [club_xg, club_npxg, club_xag, club_gmxg, club_npgmnpxg]
top_team = [top_xg, top_npxg, top_xag, top_gmxg, top_npgmnpxg]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_xg}, {top_team_npxg}, {top_team_xag}, {top_team_gmxg}, {top_team_npgmnpxg})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('xG')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# SHOTS QUERY
# ============================================================================

shots_query = """ 
SELECT
    (SELECT AVG("Shots") FROM league_stats) AS league_avg1,
    (SELECT AVG("Shots on Target") FROM league_stats) AS league_avg2,
    (SELECT AVG("Shot on Target Percentage") FROM league_stats) AS league_avg3,
    (SELECT AVG("Avg Shot Distance") FROM league_stats) AS league_avg4,
    
    
    (SELECT "Shots" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Shots on Target" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Shot on Target Percentage" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Avg Shot Distance" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,

    (SELECT Team FROM league_stats ORDER BY "Shots" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Shots on Target" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Shot on Target Percentage" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Avg Shot Distance" DESC LIMIT 1) AS top_team4,

    (SELECT "Shots" FROM league_stats ORDER BY "Shots" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Shots on Target" FROM league_stats ORDER BY "Shots on Target" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Shot on Target Percentage" FROM league_stats ORDER BY "Shot on Target Percentage" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Avg Shot Distance" FROM league_stats ORDER BY "Avg Shot Distance" DESC LIMIT 1) AS top_team_stat4;
"""

shots = pd.read_sql_query(shots_query, conn)

# Extract results
league_avg_s = float(shots.loc[0, "league_avg1"])
league_avg_sot = float(shots.loc[0, "league_avg2"])
league_avg_sotp = float(shots.loc[0, "league_avg3"])
league_avg_asd = float(shots.loc[0, "league_avg4"])


club_s = float(shots.loc[0, "club1"])
club_sot = float(shots.loc[0, "club2"])
club_sotp = float(shots.loc[0, "club3"])
club_asd = float(shots.loc[0, "club4"])

top_team_s = shots.loc[0, "top_team1"]
top_team_sot = shots.loc[0, "top_team2"]
top_team_sotp = shots.loc[0, "top_team3"]
top_team_asd = shots.loc[0, "top_team4"]

top_s = float(shots.loc[0, "top_team_stat1"])
top_sot = float(shots.loc[0, "top_team_stat2"])
top_sotp = float(shots.loc[0, "top_team_stat3"])
top_asd = float(shots.loc[0, "top_team_stat4"])


# Prepare data for plotting
categories = ['Shots', 'Shots on Target', 'Shot on Target Percentage', 'Avg Shot Distance']
league_avg = [league_avg_s, league_avg_sot, league_avg_sotp, league_avg_asd]
club = [club_s, club_sot, club_sotp, club_asd]
top_team = [top_s, top_sot, top_sotp, top_asd]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_s}, {top_team_sot}, {top_team_sotp}, {top_team_asd})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Shots')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# GOALS PER SHOT QUERY
# ============================================================================

goals_per_shot_query = """ 
SELECT
    (SELECT AVG("Goals per Shot") FROM league_stats) AS league_avg1,
    (SELECT AVG("Goals per Shot on Target") FROM league_stats) AS league_avg2,

    
    (SELECT "Goals per Shot" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Goals per Shot on Target" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,

    (SELECT Team FROM league_stats ORDER BY "Goals per Shot" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Goals per Shot on Target" DESC LIMIT 1) AS top_team2,

    (SELECT "Goals per Shot" FROM league_stats ORDER BY "Goals per Shot" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Goals per Shot on Target" FROM league_stats ORDER BY "Goals per Shot on Target" DESC LIMIT 1) AS top_team_stat2;
"""

goals_per_shot = pd.read_sql_query(goals_per_shot_query, conn)

# Extract results
league_avg_gps = float(goals_per_shot.loc[0, "league_avg1"])
league_avg_gpsot = float(goals_per_shot.loc[0, "league_avg2"])


club_gps = float(goals_per_shot.loc[0, "club1"])
club_gpsot = float(goals_per_shot.loc[0, "club2"])

top_team_gps = goals_per_shot.loc[0, "top_team1"]
top_team_gpsot = goals_per_shot.loc[0, "top_team2"]

top_gps = float(goals_per_shot.loc[0, "top_team_stat1"])
top_gpsot = float(goals_per_shot.loc[0, "top_team_stat2"])

# Prepare data for plotting
categories = ['Goals per Shot', 'Goals per Shot on Target']
league_avg = [league_avg_gps, league_avg_gpsot]
club = [club_gps, club_gpsot]
top_team = [top_gps, top_gpsot]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_gps}, {top_team_gpsot})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Goals per Shot')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# PASS QUERY
# ============================================================================

pass_query = """ 
SELECT
    (SELECT AVG("Short Pass") FROM league_stats) AS league_avg1,
    (SELECT AVG("Medium Pass") FROM league_stats) AS league_avg3,
    (SELECT AVG("Long Pass") FROM league_stats) AS league_avg5,
    
    
    (SELECT "Short Pass" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Medium Pass" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Long Pass" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,

    (SELECT Team FROM league_stats ORDER BY "Short Pass" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Medium Pass" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Long Pass" DESC LIMIT 1) AS top_team5,

    (SELECT "Short Pass" FROM league_stats ORDER BY "Short Pass" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Medium Pass" FROM league_stats ORDER BY "Medium Pass" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Long Pass" FROM league_stats ORDER BY "Long Pass" DESC LIMIT 1) AS top_team_stat5;
"""

pass_ = pd.read_sql_query(pass_query, conn)

# Extract results
league_avg_sp = float(pass_.loc[0, "league_avg1"])
league_avg_mp = float(pass_.loc[0, "league_avg3"])
league_avg_lp = float(pass_.loc[0, "league_avg5"])


club_sp = float(pass_.loc[0, "club1"])
club_mp = float(pass_.loc[0, "club3"])
club_lp = float(pass_.loc[0, "club5"])

top_team_sp = pass_.loc[0, "top_team1"]
top_team_mp = pass_.loc[0, "top_team3"]
top_team_lp = pass_.loc[0, "top_team5"]

top_sp = float(pass_.loc[0, "top_team_stat1"])
top_mp = float(pass_.loc[0, "top_team_stat3"])
top_lp = float(pass_.loc[0, "top_team_stat5"])

# Prepare data for plotting
categories = ['Short Pass', 'Medium Pass', 'Long Pass']
league_avg = [league_avg_sp, league_avg_mp, league_avg_lp]
club = [club_sp, club_mp, club_lp]
top_team = [top_sp, top_mp, top_lp]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_sp}, {top_team_mp}, {top_team_lp})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Passing')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# xA QUERY
# ============================================================================

xA_query = """ 
SELECT
    (SELECT AVG("xA") FROM league_stats) AS league_avg1,
    (SELECT AVG("Assists minus xAG") FROM league_stats) AS league_avg2,
    
    
    (SELECT "xA" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Assists minus xAG" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,

    (SELECT Team FROM league_stats ORDER BY "xA" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Assists minus xAG" DESC LIMIT 1) AS top_team2,

    (SELECT "xA" FROM league_stats ORDER BY "xA" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Assists minus xAG" FROM league_stats ORDER BY "Assists minus xAG" DESC LIMIT 1) AS top_team_stat2;
"""

xA = pd.read_sql_query(xA_query, conn)

# Extract results
league_avg_xa = float(xA.loc[0, "league_avg1"])
league_avg_amxag = float(xA.loc[0, "league_avg2"])


club_xa = float(xA.loc[0, "club1"])
club_amxag = float(xA.loc[0, "club2"])

top_team_xa = xA.loc[0, "top_team1"]
top_team_amxag = xA.loc[0, "top_team2"]

top_xa = float(xA.loc[0, "top_team_stat1"])
top_amxag = float(xA.loc[0, "top_team_stat2"])

# Prepare data for plotting
categories = ['xA', 'Assists minus xAG']
league_avg = [league_avg_xa, league_avg_amxag]
club = [club_xa, club_amxag]
top_team = [top_xa, top_amxag]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_xa}, {top_team_amxag})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('xA')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# ATTACKING PASS QUERY
# ============================================================================

attacking_pass_query = """
SELECT
    (SELECT AVG("Key Passes") FROM league_stats) AS league_avg1,
    (SELECT AVG("Pass into final third") FROM league_stats) AS league_avg2,
    (SELECT AVG("Pass into Pen Area") FROM league_stats) AS league_avg3,
    (SELECT AVG("Cross into Pen Area") FROM league_stats) AS league_avg4,
    
    
    (SELECT "Key Passes" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Pass into final third" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Pass into Pen Area" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Cross into Pen Area" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,

    (SELECT Team FROM league_stats ORDER BY "Key Passes" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Pass into final third" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Pass into Pen Area" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Cross into Pen Area" DESC LIMIT 1) AS top_team4,

    (SELECT "Key Passes" FROM league_stats ORDER BY "Key Passes" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Pass into final third" FROM league_stats ORDER BY "Pass into final third" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Pass into Pen Area" FROM league_stats ORDER BY "Pass into Pen Area" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Cross into Pen Area" FROM league_stats ORDER BY "Cross into Pen Area" DESC LIMIT 1) AS top_team_stat4;
"""

attacking_pass = pd.read_sql_query(attacking_pass_query, conn)

# Extract results
league_avg_kp = float(attacking_pass.loc[0, "league_avg1"])
league_avg_pft = float(attacking_pass.loc[0, "league_avg2"])
league_avg_ppa = float(attacking_pass.loc[0, "league_avg3"])
league_avg_cpa = float(attacking_pass.loc[0, "league_avg4"])


club_kp = float(attacking_pass.loc[0, "club1"])
club_pft = float(attacking_pass.loc[0, "club2"])
club_ppa = float(attacking_pass.loc[0, "club3"])
club_cpa = float(attacking_pass.loc[0, "club4"])

top_team_kp = attacking_pass.loc[0, "top_team1"]
top_team_pft = attacking_pass.loc[0, "top_team2"]
top_team_ppa = attacking_pass.loc[0, "top_team3"]
top_team_cpa = attacking_pass.loc[0, "top_team4"]

top_kp = float(attacking_pass.loc[0, "top_team_stat1"])
top_pft = float(attacking_pass.loc[0, "top_team_stat2"])
top_ppa = float(attacking_pass.loc[0, "top_team_stat3"])
top_cpa = float(attacking_pass.loc[0, "top_team_stat4"])

# Prepare data for plotting
categories = ['Key Passes', 'Pass into final third', 'Pass into Pen Area', 'Cross into Pen Area']
league_avg = [league_avg_kp, league_avg_pft, league_avg_ppa, league_avg_cpa]
club = [club_kp, club_pft, club_ppa, club_cpa]
top_team = [top_kp, top_pft, top_ppa, top_cpa]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_kp}, {top_team_pft}, {top_team_ppa}, {top_team_cpa})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Attacking Passes')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# ============================================================================
# PASS COMPLETION QUERY
# ============================================================================

pass_completion_query = """ 
SELECT
    (SELECT AVG("Pass Completion") FROM league_stats) AS league_avg1,
    (SELECT AVG("Short Pass Completion") FROM league_stats) AS league_avg2,
    (SELECT AVG("Medium Pass Completion") FROM league_stats) AS league_avg3,
    (SELECT AVG("Long Pass Completion") FROM league_stats) AS league_avg4,
    
    
    (SELECT "Pass Completion" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Short Pass Completion" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Medium Pass Completion" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Long Pass Completion" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,

    (SELECT Team FROM league_stats ORDER BY "Pass Completion" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Short Pass Completion" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Medium Pass Completion" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Long Pass Completion" DESC LIMIT 1) AS top_team4,

    (SELECT "Pass Completion" FROM league_stats ORDER BY "Pass Completion" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Short Pass Completion" FROM league_stats ORDER BY "Short Pass Completion" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Medium Pass Completion" FROM league_stats ORDER BY "Medium Pass Completion" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Long Pass Completion" FROM league_stats ORDER BY "Long Pass Completion" DESC LIMIT 1) AS top_team_stat4;
"""

pass_completion =pd.read_sql_query(pass_completion_query, conn)

# Extract results
league_avg_pc = float(pass_completion.loc[0, "league_avg1"])
league_avg_spc = float(pass_completion.loc[0, "league_avg2"])
league_avg_mpc = float(pass_completion.loc[0, "league_avg3"])
league_avg_lpc = float(pass_completion.loc[0, "league_avg4"])


club_pc = float(pass_completion.loc[0, "club1"])
club_spc = float(pass_completion.loc[0, "club2"])
club_mpc = float(pass_completion.loc[0, "club3"])
club_lpc = float(pass_completion.loc[0, "club4"])

top_team_pc = pass_completion.loc[0, "top_team1"]
top_team_spc = pass_completion.loc[0, "top_team2"]
top_team_mpc = pass_completion.loc[0, "top_team3"]
top_team_lpc = pass_completion.loc[0, "top_team4"]

top_pc = float(pass_completion.loc[0, "top_team_stat1"])
top_spc = float(pass_completion.loc[0, "top_team_stat2"])
top_mpc = float(pass_completion.loc[0, "top_team_stat3"])
top_lpc = float(pass_completion.loc[0, "top_team_stat4"])

# Prepare data for plotting
categories = ['Pass Completion', 'Short Pass Completion', 'Medium Pass Completion', 'Long Pass Completion']
league_avg = [league_avg_pc, league_avg_spc, league_avg_mpc, league_avg_lpc]
club = [club_pc, club_spc, club_mpc, club_lpc]
top_team = [top_pc, top_spc, top_mpc, top_lpc]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_pc}, {top_team_spc}, {top_team_mpc}, {top_team_lpc})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Pass Completion')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# SHOT CREATION QUERY
# ============================================================================

shot_creation_query = """ 
SELECT
    (SELECT AVG("SCA From Live Pass") FROM league_stats) AS league_avg1,
    (SELECT AVG("SCA From Dead Pass") FROM league_stats) AS league_avg2,
    (SELECT AVG("SCA From Take On") FROM league_stats) AS league_avg3,
    (SELECT AVG("SCA From Shot") FROM league_stats) AS league_avg4,
    (SELECT AVG("SCA From Foul Drawn") FROM league_stats) AS league_avg5,
    (SELECT AVG("SCA From Defensive Action") FROM league_stats) AS league_avg6,
    

    (SELECT "SCA From Live Pass" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "SCA From Dead Pass" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "SCA From Take On" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "SCA From Shot" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,
    (SELECT "SCA From Foul Drawn" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,
    (SELECT "SCA From Defensive Action" FROM league_stats WHERE Team = 'Canberra Utd') AS club6,

    (SELECT Team FROM league_stats ORDER BY "SCA From Live Pass" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "SCA From Dead Pass" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "SCA From Take On" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "SCA From Shot" DESC LIMIT 1) AS top_team4,
    (SELECT Team FROM league_stats ORDER BY "SCA From Foul Drawn" DESC LIMIT 1) AS top_team5,
    (SELECT Team FROM league_stats ORDER BY "SCA From Defensive Action" DESC LIMIT 1) AS top_team6,

    (SELECT "SCA From Live Pass" FROM league_stats ORDER BY "SCA From Live Pass" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "SCA From Dead Pass" FROM league_stats ORDER BY "SCA From Dead Pass" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "SCA From Take On" FROM league_stats ORDER BY "SCA From Take On" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "SCA From Shot" FROM league_stats ORDER BY "SCA From Shot" DESC LIMIT 1) AS top_team_stat4,
    (SELECT "SCA From Foul Drawn" FROM league_stats ORDER BY "SCA From Foul Drawn" DESC LIMIT 1) AS top_team_stat5,
    (SELECT "SCA From Defensive Action" FROM league_stats ORDER BY "SCA From Defensive Action" DESC LIMIT 1) AS top_team_stat6;
"""

shot_creation = pd.read_sql_query(shot_creation_query, conn)

# Extract results
league_avg_scalp = float(shot_creation.loc[0, "league_avg1"])
league_avg_scadp = float(shot_creation.loc[0, "league_avg2"])
league_avg_scato = float(shot_creation.loc[0, "league_avg3"])
league_avg_scas = float(shot_creation.loc[0, "league_avg4"])
league_avg_scafd = float(shot_creation.loc[0, "league_avg5"])
league_avg_scada = float(shot_creation.loc[0, "league_avg6"])


club_scalp = float(shot_creation.loc[0, "club1"])
club_scadp = float(shot_creation.loc[0, "club2"])
club_scato = float(shot_creation.loc[0, "club3"])
club_scas = float(shot_creation.loc[0, "club4"])
club_scafd = float(shot_creation.loc[0, "club5"])
club_scada = float(shot_creation.loc[0, "club6"])

top_team_scalp = shot_creation.loc[0, "top_team1"]
top_team_scadp = shot_creation.loc[0, "top_team2"]
top_team_scato = shot_creation.loc[0, "top_team3"]
top_team_scas = shot_creation.loc[0, "top_team4"]
top_team_scafd = shot_creation.loc[0, "top_team5"]
top_team_scada = shot_creation.loc[0, "top_team6"]

top_scalp = float(shot_creation.loc[0, "top_team_stat1"])
top_scadp = float(shot_creation.loc[0, "top_team_stat2"])
top_scato = float(shot_creation.loc[0, "top_team_stat3"])
top_scas = float(shot_creation.loc[0, "top_team_stat4"])
top_scafd = float(shot_creation.loc[0, "top_team_stat5"])
top_scada = float(shot_creation.loc[0, "top_team_stat6"])

# Prepare data for plotting
categories = ['SCA Live Pass', 'SCA Dead Pass', 'SCA Take On', 'SCA Shot', 'SCA Foul Drawn', 'SCA Defensive Action']
league_avg = [league_avg_scalp, league_avg_scadp, league_avg_scato, league_avg_scas, league_avg_scafd, league_avg_scada]
club = [club_scalp, club_scadp, club_scato, club_scas, club_scafd, club_scada]
top_team = [top_scalp, top_scadp, top_scato, top_scas, top_scafd, top_scada]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_scalp}, {top_team_scadp}, {top_team_scato}, {top_team_scas}, {top_team_scafd}, {top_team_scada})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Shot Creation')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# GOAL CREATION QUERY
# ============================================================================

goal_creation_query = """ 
SELECT
    (SELECT AVG("GCA From Live Pass") FROM league_stats) AS league_avg1,
    (SELECT AVG("GCA From Dead Pass") FROM league_stats) AS league_avg2,
    (SELECT AVG("GCA From Take On") FROM league_stats) AS league_avg3,
    (SELECT AVG("GCA From Shot") FROM league_stats) AS league_avg4,
    (SELECT AVG("GCA From Foul Drawn") FROM league_stats) AS league_avg5,
    (SELECT AVG("GCA From Defensive Action") FROM league_stats) AS league_avg6,

    
    (SELECT "GCA From Live Pass" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "GCA From Dead Pass" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "GCA From Take On" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "GCA From Shot" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,
    (SELECT "GCA From Foul Drawn" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,
    (SELECT "GCA From Defensive Action" FROM league_stats WHERE Team = 'Canberra Utd') AS club6,

    (SELECT Team FROM league_stats ORDER BY "GCA From Live Pass" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "GCA From Dead Pass" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "GCA From Take On" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "GCA From Shot" DESC LIMIT 1) AS top_team4,
    (SELECT Team FROM league_stats ORDER BY "GCA From Foul Drawn" DESC LIMIT 1) AS top_team5,
    (SELECT Team FROM league_stats ORDER BY "GCA From Defensive Action" DESC LIMIT 1) AS top_team6,

    (SELECT "GCA From Live Pass" FROM league_stats ORDER BY "GCA From Live Pass" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "GCA From Dead Pass" FROM league_stats ORDER BY "GCA From Dead Pass" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "GCA From Take On" FROM league_stats ORDER BY "GCA From Take On" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "GCA From Shot" FROM league_stats ORDER BY "GCA From Shot" DESC LIMIT 1) AS top_team_stat4,
    (SELECT "GCA From Foul Drawn" FROM league_stats ORDER BY "GCA From Foul Drawn" DESC LIMIT 1) AS top_team_stat5,
    (SELECT "GCA From Defensive Action" FROM league_stats ORDER BY "GCA From Defensive Action" DESC LIMIT 1) AS top_team_stat6;
"""

goal_creation = pd.read_sql_query(goal_creation_query, conn)

# Extract results
league_avg_gcalp = float(goal_creation.loc[0, "league_avg1"])
league_avg_gcadp = float(goal_creation.loc[0, "league_avg2"])
league_avg_gcato = float(goal_creation.loc[0, "league_avg3"])
league_avg_gcas = float(goal_creation.loc[0, "league_avg4"])
league_avg_gcafd = float(goal_creation.loc[0, "league_avg5"])
league_avg_gcada = float(goal_creation.loc[0, "league_avg6"])


club_gcalp = float(goal_creation.loc[0, "club1"])
club_gcadp = float(goal_creation.loc[0, "club2"])
club_gcato = float(goal_creation.loc[0, "club3"])
club_gcas = float(goal_creation.loc[0, "club4"])
club_gcafd = float(goal_creation.loc[0, "club5"])
club_gcada = float(goal_creation.loc[0, "club6"])

top_team_gcalp = goal_creation.loc[0, "top_team1"]
top_team_gcadp = goal_creation.loc[0, "top_team2"]
top_team_gcato = goal_creation.loc[0, "top_team3"]
top_team_gcas = goal_creation.loc[0, "top_team4"]
top_team_gcafd = goal_creation.loc[0, "top_team5"]
top_team_gcada = goal_creation.loc[0, "top_team6"]

top_gcalp = float(goal_creation.loc[0, "top_team_stat1"])
top_gcadp = float(goal_creation.loc[0, "top_team_stat2"])
top_gcato = float(goal_creation.loc[0, "top_team_stat3"])
top_gcas = float(goal_creation.loc[0, "top_team_stat4"])
top_gcafd = float(goal_creation.loc[0, "top_team_stat5"])
top_gcada = float(goal_creation.loc[0, "top_team_stat6"])

# Prepare data for plotting
categories = ['GCA Live Pass', 'GCA Dead Pass', 'GCA Take On', 'GCA Shot', 'GCA Foul Drawn', 'GCA Defensive Action']
league_avg = [league_avg_gcalp, league_avg_gcadp, league_avg_gcato, league_avg_gcas, league_avg_gcafd, league_avg_gcada]
club = [club_gcalp, club_gcadp, club_gcato, club_gcas, club_gcafd, club_gcada]
top_team = [top_gcalp, top_gcadp, top_gcato, top_gcas, top_gcafd, top_gcada]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_gcalp}, {top_team_gcadp}, {top_team_gcato}, {top_team_gcas}, {top_team_gcafd}, {top_team_gcada})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Goal Creation')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# TACKLES QUERY
# ============================================================================

tackles_query = """
SELECT
    (SELECT AVG("Tackles") FROM league_stats) AS league_avg1,
    (SELECT AVG("Tackles Won") FROM league_stats) AS league_avg2,
    (SELECT AVG("Tackles in Def 3rd") FROM league_stats) AS league_avg3,
    (SELECT AVG("Tackles in Mid 3rd") FROM league_stats) AS league_avg4,
    (SELECT AVG("Tackles in Att 3rd") FROM league_stats) AS league_avg5,
    
    
    (SELECT "Tackles" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Tackles Won" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Tackles in Def 3rd" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Tackles in Mid 3rd" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,
    (SELECT "Tackles in Att 3rd" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,

    (SELECT Team FROM league_stats ORDER BY "Tackles" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Tackles Won" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Tackles in Def 3rd" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Tackles in Mid 3rd" DESC LIMIT 1) AS top_team4,
    (SELECT Team FROM league_stats ORDER BY "Tackles in Att 3rd" DESC LIMIT 1) AS top_team5,

    (SELECT "Tackles" FROM league_stats ORDER BY "Tackles" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Tackles Won" FROM league_stats ORDER BY "Tackles Won" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Tackles in Def 3rd" FROM league_stats ORDER BY "Tackles in Def 3rd" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Tackles in Mid 3rd" FROM league_stats ORDER BY "Tackles in Mid 3rd" DESC LIMIT 1) AS top_team_stat4,
    (SELECT "Tackles in Att 3rd" FROM league_stats ORDER BY "Tackles in Att 3rd" DESC LIMIT 1) AS top_team_stat5;
"""

tackles = pd.read_sql_query(tackles_query, conn)

# Extract results
league_avg_t = float(tackles.loc[0, "league_avg1"])
league_avg_tw = float(tackles.loc[0, "league_avg2"])
league_avg_td3 = float(tackles.loc[0, "league_avg3"])
league_avg_tm3 = float(tackles.loc[0, "league_avg4"])
league_avg_ta3 = float(tackles.loc[0, "league_avg5"])


club_t = float(tackles.loc[0, "club1"])
club_tw = float(tackles.loc[0, "club2"])
club_td3 = float(tackles.loc[0, "club3"])
club_tm3 = float(tackles.loc[0, "club4"])
club_ta3 = float(tackles.loc[0, "club5"])

top_team_t = tackles.loc[0, "top_team1"]
top_team_tw = tackles.loc[0, "top_team2"]
top_team_td3 = tackles.loc[0, "top_team3"]
top_team_tm3 = tackles.loc[0, "top_team4"]
top_team_ta3 = tackles.loc[0, "top_team5"]

top_t = float(tackles.loc[0, "top_team_stat1"])
top_tw = float(tackles.loc[0, "top_team_stat2"])
top_td3 = float(tackles.loc[0, "top_team_stat3"])
top_tm3 = float(tackles.loc[0, "top_team_stat4"])
top_ta3 = float(tackles.loc[0, "top_team_stat5"])


# Prepare data for plotting
categories = ['Tackles', 'Tackles Won', 'Tackles Def 3rd', 'Tackles Mid 3rd', 'Tackles Att 3rd']
league_avg = [league_avg_t, league_avg_tw, league_avg_td3, league_avg_tm3, league_avg_ta3]
club = [club_t, club_tw, club_td3, club_tm3, club_ta3]
top_team = [top_t, top_tw, top_td3, top_tm3, top_ta3]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_t}, {top_team_tw}, {top_team_td3}, {top_team_tm3}, {top_team_ta3})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Tackles')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# DEFENSIVE QUERY
# ============================================================================

defensive_query = """ 
SELECT
    (SELECT AVG("Dribblers Tackled") FROM league_stats) AS league_avg1,
    (SELECT AVG("Dribblers Tackled Percentage") FROM league_stats) AS league_avg2,
    (SELECT AVG("Blocked Shots") FROM league_stats) AS league_avg3,
    (SELECT AVG("Blocked Passes") FROM league_stats) AS league_avg4,
    (SELECT AVG("Interceptions") FROM league_stats) AS league_avg5,
    (SELECT AVG("Clearances") FROM league_stats) AS league_avg6,
    (SELECT AVG("Recoveries") FROM league_stats) AS league_avg7,
    
    
    (SELECT "Dribblers Tackled" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Dribblers Tackled Percentage" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Blocked Shots" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Blocked Passes" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,
    (SELECT "Interceptions" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,
    (SELECT "Clearances" FROM league_stats WHERE Team = 'Canberra Utd') AS club6,
    (SELECT "Recoveries" FROM league_stats WHERE Team = 'Canberra Utd') AS club7,

    (SELECT Team FROM league_stats ORDER BY "Dribblers Tackled" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Dribblers Tackled Percentage" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Blocked Shots" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Blocked Passes" DESC LIMIT 1) AS top_team4,
    (SELECT Team FROM league_stats ORDER BY "Interceptions" DESC LIMIT 1) AS top_team5,
    (SELECT Team FROM league_stats ORDER BY "Clearances" DESC LIMIT 1) AS top_team6,
    (SELECT Team FROM league_stats ORDER BY "Recoveries" DESC LIMIT 1) AS top_team7,

    (SELECT "Dribblers Tackled" FROM league_stats ORDER BY "Dribblers Tackled" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Dribblers Tackled Percentage" FROM league_stats ORDER BY "Dribblers Tackled Percentage" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Blocked Shots" FROM league_stats ORDER BY "Blocked Shots" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Blocked Passes" FROM league_stats ORDER BY "Blocked Passes" DESC LIMIT 1) AS top_team_stat4,
    (SELECT "Interceptions" FROM league_stats ORDER BY "Interceptions" DESC LIMIT 1) AS top_team_stat5,
    (SELECT "Clearances" FROM league_stats ORDER BY "Clearances" DESC LIMIT 1) AS top_team_stat6,
    (SELECT "Recoveries" FROM league_stats ORDER BY "Recoveries" DESC LIMIT 1) AS top_team_stat7;
"""

defensive = pd.read_sql_query(defensive_query, conn)

# Extract results
league_avg_dt = float(defensive.loc[0, "league_avg1"])
league_avg_dtp = float(defensive.loc[0, "league_avg2"])
league_avg_bs = float(defensive.loc[0, "league_avg3"])
league_avg_bp = float(defensive.loc[0, "league_avg4"])
league_avg_i = float(defensive.loc[0, "league_avg5"])
league_avg_c = float(defensive.loc[0, "league_avg6"])
league_avg_r = float(defensive.loc[0, "league_avg7"])


club_dt = float(defensive.loc[0, "club1"])
club_dtp = float(defensive.loc[0, "club2"])
club_bs = float(defensive.loc[0, "club3"])
club_bp = float(defensive.loc[0, "club4"])
club_i = float(defensive.loc[0, "club5"])
club_c = float(defensive.loc[0, "club6"])
club_r = float(defensive.loc[0, "club7"])

top_team_dt = defensive.loc[0, "top_team1"]
top_team_dtp = defensive.loc[0, "top_team2"]
top_team_bs = defensive.loc[0, "top_team3"]
top_team_bp = defensive.loc[0, "top_team4"]
top_team_i = defensive.loc[0, "top_team5"]
top_team_c = defensive.loc[0, "top_team6"]
top_team_r = defensive.loc[0, "top_team7"]

top_dt = float(defensive.loc[0, "top_team_stat1"])
top_dtp = float(defensive.loc[0, "top_team_stat2"])
top_bs = float(defensive.loc[0, "top_team_stat3"])
top_bp = float(defensive.loc[0, "top_team_stat4"])
top_i = float(defensive.loc[0, "top_team_stat5"])
top_c = float(defensive.loc[0, "top_team_stat6"])
top_r = float(defensive.loc[0, "top_team_stat7"])

# Prepare data for plotting
categories = ['Dribblers Tackled', 'Dribblers Tackled %', 'Blocked Shots', 'Blocked Pass', 'Interceptions', 'Clearances', 'Recoveries']
league_avg = [league_avg_dt, league_avg_dtp, league_avg_bs, league_avg_bp, league_avg_i, league_avg_c, league_avg_r]
club = [club_dt, club_dtp, club_bs, club_bp, club_i, club_c, club_r]
top_team = [top_dt, top_dtp, top_bs, top_bp, top_i, top_c, top_r]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(13, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_dt}, {top_team_dtp}, {top_team_bs}, {top_team_bp}, {top_team_i}, {top_team_c}, {top_team_r})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Defensive')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# TOUCHES QUERY
# ============================================================================

touches_query = """
SELECT
    (SELECT AVG("Touches in Defensive Pen Area") FROM league_stats) AS league_avg1,
    (SELECT AVG("Touches in Defensive Third") FROM league_stats) AS league_avg2,
    (SELECT AVG("Touches in Midfield Third") FROM league_stats) AS league_avg3,
    (SELECT AVG("Touches in Attacking Third") FROM league_stats) AS league_avg4,
    (SELECT AVG("Touches in Pen Area") FROM league_stats) AS league_avg5,
    
    
    (SELECT "Touches in Defensive Pen Area" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Touches in Defensive Third" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Touches in Midfield Third" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Touches in Attacking Third" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,
    (SELECT "Touches in Pen Area" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,

    (SELECT Team FROM league_stats ORDER BY "Touches in Defensive Pen Area" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Touches in Defensive Third" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Touches in Midfield Third" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Touches in Attacking Third" DESC LIMIT 1) AS top_team4,
    (SELECT Team FROM league_stats ORDER BY "Touches in Pen Area" DESC LIMIT 1) AS top_team5,

    (SELECT "Touches in Defensive Pen Area" FROM league_stats ORDER BY "Touches in Defensive Pen Area" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Touches in Defensive Third" FROM league_stats ORDER BY "Touches in Defensive Third" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Touches in Midfield Third" FROM league_stats ORDER BY "Touches in Midfield Third" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Touches in Attacking Third" FROM league_stats ORDER BY "Touches in Attacking Third" DESC LIMIT 1) AS top_team_stat4,
    (SELECT "Touches in Pen Area" FROM league_stats ORDER BY "Touches in Pen Area" DESC LIMIT 1) AS top_team_stat5;
"""

touches = pd.read_sql_query(touches_query, conn)

# Extract results
league_avg_todpa = float(touches.loc[0, "league_avg1"])
league_avg_tod3 = float(touches.loc[0, "league_avg2"])
league_avg_tom3 = float(touches.loc[0, "league_avg3"])
league_avg_toa3 = float(touches.loc[0, "league_avg4"])
league_avg_toapa = float(touches.loc[0, "league_avg5"])


club_todpa = float(touches.loc[0, "club1"])
club_tod3 = float(touches.loc[0, "club2"])
club_tom3 = float(touches.loc[0, "club3"])
club_toa3 = float(touches.loc[0, "club4"])
club_toapa = float(touches.loc[0, "club5"])

top_team_todpa = touches.loc[0, "top_team1"]
top_team_tod3 = touches.loc[0, "top_team2"]
top_team_tom3 = touches.loc[0, "top_team3"]
top_team_toa3 = touches.loc[0, "top_team4"]
top_team_toapa = touches.loc[0, "top_team5"]

top_todpa = float(touches.loc[0, "top_team_stat1"])
top_tod3 = float(touches.loc[0, "top_team_stat2"])
top_tom3 = float(touches.loc[0, "top_team_stat3"])
top_toa3 = float(touches.loc[0, "top_team_stat4"])
top_toapa = float(touches.loc[0, "top_team_stat5"])


# Prepare data for plotting
categories = ['Touches Def Pen', 'Touches Def 3rd', 'Touches Mid 3rd', 'Touches Att 3rd', 'Touches Pen Area']
league_avg = [league_avg_todpa, league_avg_tod3, league_avg_tom3, league_avg_toa3, league_avg_toapa]
club = [club_todpa, club_tod3, club_tom3, club_toa3, club_toapa]
top_team = [top_todpa, top_tod3, top_tom3, top_toa3, top_toapa]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_todpa}, {top_team_tod3}, {top_team_tom3}, {top_team_toa3}, {top_team_toapa})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Touches')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# TAKE ONS QUERY
# ============================================================================

take_ons_query = """
SELECT
    (SELECT AVG("Take Ons Attempted") FROM league_stats) AS league_avg1,
    (SELECT AVG("Take Ons Won") FROM league_stats) AS league_avg2,
    (SELECT AVG("Take Ons Won Percentage") FROM league_stats) AS league_avg3,
    (SELECT AVG("Take Ons Tackled") FROM league_stats) AS league_avg4,
    (SELECT AVG("Take Ons Tackled Percentage") FROM league_stats) AS league_avg5,
    
    
    (SELECT "Take Ons Attempted" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Take Ons Won" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Take Ons Won Percentage" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Take Ons Tackled" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,
    (SELECT "Take Ons Tackled Percentage" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,

    (SELECT Team FROM league_stats ORDER BY "Take Ons Attempted" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Take Ons Won" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Take Ons Won Percentage" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Take Ons Tackled" DESC LIMIT 1) AS top_team4,
    (SELECT Team FROM league_stats ORDER BY "Take Ons Tackled Percentage" DESC LIMIT 1) AS top_team5,

    (SELECT "Take Ons Attempted" FROM league_stats ORDER BY "Take Ons Attempted" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Take Ons Won" FROM league_stats ORDER BY "Take Ons Won" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Take Ons Won Percentage" FROM league_stats ORDER BY "Take Ons Won Percentage" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Take Ons Tackled" FROM league_stats ORDER BY "Take Ons Tackled" DESC LIMIT 1) AS top_team_stat4,
    (SELECT "Take Ons Tackled Percentage" FROM league_stats ORDER BY "Take Ons Tackled Percentage" DESC LIMIT 1) AS top_team_stat5;
"""

take_ons = pd.read_sql_query(take_ons_query, conn)

# Extract results
league_avg_toa = float(take_ons.loc[0, "league_avg1"])
league_avg_tow = float(take_ons.loc[0, "league_avg2"])
league_avg_towp = float(take_ons.loc[0, "league_avg3"])
league_avg_tot = float(take_ons.loc[0, "league_avg4"])
league_avg_totp = float(take_ons.loc[0, "league_avg5"])


club_toa = float(take_ons.loc[0, "club1"])
club_tow = float(take_ons.loc[0, "club2"])
club_towp = float(take_ons.loc[0, "club3"])
club_tot = float(take_ons.loc[0, "club4"])
club_totp = float(take_ons.loc[0, "club5"])

top_team_toa = take_ons.loc[0, "top_team1"]
top_team_tow = take_ons.loc[0, "top_team2"]
top_team_towp = take_ons.loc[0, "top_team3"]
top_team_tot = take_ons.loc[0, "top_team4"]
top_team_totp = take_ons.loc[0, "top_team5"]

top_toa = float(take_ons.loc[0, "top_team_stat1"])
top_tow = float(take_ons.loc[0, "top_team_stat2"])
top_towp = float(take_ons.loc[0, "top_team_stat3"])
top_tot = float(take_ons.loc[0, "top_team_stat4"])
top_totp = float(take_ons.loc[0, "top_team_stat5"])


# Prepare data for plotting
categories = ['Take Ons Attempted', 'Take Ons Won', 'Take Ons Won %', 'Take Ons Tackled', 'Take Ons Tackled %']
league_avg = [league_avg_toa, league_avg_tow, league_avg_towp, league_avg_tot, league_avg_totp]
club = [club_toa, club_tow, club_towp, club_tot, club_totp]
top_team = [top_toa, top_tow, top_towp, top_tot, top_totp]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_toa}, {top_team_tow}, {top_team_towp}, {top_team_tot}, {top_team_totp})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Take Ons')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# CARRIES QUERY
# ============================================================================

carries_query = """ 
SELECT
    (SELECT AVG("Carries into Final Third") FROM league_stats) AS league_avg1,
    (SELECT AVG("Carries into Penalty Area") FROM league_stats) AS league_avg2,

    
    (SELECT "Carries into Final Third" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Carries into Penalty Area" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,

    (SELECT Team FROM league_stats ORDER BY "Carries into Final Third" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Carries into Penalty Area" DESC LIMIT 1) AS top_team2,

    (SELECT "Carries into Final Third" FROM league_stats ORDER BY "Carries into Final Third" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Carries into Penalty Area" FROM league_stats ORDER BY "Carries into Penalty Area" DESC LIMIT 1) AS top_team_stat2;
"""

carries = pd.read_sql_query(carries_query, conn)

# Extract results
league_avg_cift = float(carries.loc[0, "league_avg1"])
league_avg_cipa = float(carries.loc[0, "league_avg2"])


club_cift = float(carries.loc[0, "club1"])
club_cipa = float(carries.loc[0, "club2"])

top_team_cift = carries.loc[0, "top_team1"]
top_team_cipa = carries.loc[0, "top_team2"]

top_cift = float(carries.loc[0, "top_team_stat1"])
top_cipa = float(carries.loc[0, "top_team_stat2"])


# Prepare data for plotting
categories = ['Carries Final 3rd', 'Carries Pen Area']
league_avg = [league_avg_cift, league_avg_cipa]
club = [club_cift, club_cipa]
top_team = [top_cift, top_cipa]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_cift}, {top_team_cipa})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Carries')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# MISTAKES QUERY
# ============================================================================

mistakes_query = """ 
SELECT
    (SELECT AVG("Miscontrols") FROM league_stats) AS league_avg1,
    (SELECT AVG("Dispossessed") FROM league_stats) AS league_avg2,
    (SELECT AVG("Errors") FROM league_stats) AS league_avg3,


    (SELECT "Miscontrols" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Dispossessed" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Errors" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,

    (SELECT Team FROM league_stats ORDER BY "Miscontrols" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Dispossessed" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Errors" DESC LIMIT 1) AS top_team3,

    (SELECT "Miscontrols" FROM league_stats ORDER BY "Miscontrols" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Dispossessed" FROM league_stats ORDER BY "Dispossessed" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Errors" FROM league_stats ORDER BY "Errors" DESC LIMIT 1) AS top_team_stat3;
"""

mistakes = pd.read_sql_query(mistakes_query, conn)

# Extract results
league_avg_m = float(mistakes.loc[0, "league_avg1"])
league_avg_d = float(mistakes.loc[0, "league_avg2"])
league_avg_e = float(mistakes.loc[0, "league_avg3"])


club_m = float(mistakes.loc[0, "club1"])
club_d = float(mistakes.loc[0, "club2"])
club_e = float(mistakes.loc[0, "club3"])

top_team_m = mistakes.loc[0, "top_team1"]
top_team_d = mistakes.loc[0, "top_team2"]
top_team_e = mistakes.loc[0, "top_team3"]

top_m = float(mistakes.loc[0, "top_team_stat1"])
top_d = float(mistakes.loc[0, "top_team_stat2"])
top_e = float(mistakes.loc[0, "top_team_stat3"])


# Prepare data for plotting
categories = ['Miscontrols', 'Dispossessed', 'Errors']
league_avg = [league_avg_m, league_avg_d, league_avg_e]
club = [club_m, club_d, club_e]
top_team = [top_m, top_d, top_e]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_m}, {top_team_d}, {top_team_e})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Mistakes')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# FOULS QUERY
# ============================================================================

fouls_query = """ 
SELECT
    (SELECT AVG("Fouls Comitted") FROM league_stats) AS league_avg1,
    (SELECT AVG("Fouls Drawn") FROM league_stats) AS league_avg2,
    (SELECT AVG("Offsides") FROM league_stats) AS league_avg3,

    
    (SELECT "Fouls Comitted" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Fouls Drawn" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Offsides" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,

    (SELECT Team FROM league_stats ORDER BY "Fouls Comitted" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Fouls Drawn" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Offsides" DESC LIMIT 1) AS top_team3,

    (SELECT "Fouls Comitted" FROM league_stats ORDER BY "Fouls Comitted" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Fouls Drawn" FROM league_stats ORDER BY "Fouls Drawn" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Offsides" FROM league_stats ORDER BY "Offsides" DESC LIMIT 1) AS top_team_stat3;
"""

fouls = pd.read_sql_query(fouls_query, conn)

# Extract results
league_avg_fc = float(fouls.loc[0, "league_avg1"])
league_avg_fd = float(fouls.loc[0, "league_avg2"])
league_avg_o = float(fouls.loc[0, "league_avg3"])


club_fc = float(fouls.loc[0, "club1"])
club_fd = float(fouls.loc[0, "club2"])
club_o = float(fouls.loc[0, "club3"])

top_team_fc = fouls.loc[0, "top_team1"]
top_team_fd = fouls.loc[0, "top_team2"]
top_team_o = fouls.loc[0, "top_team3"]

top_fc = float(fouls.loc[0, "top_team_stat1"])
top_fd = float(fouls.loc[0, "top_team_stat2"])
top_o = float(fouls.loc[0, "top_team_stat3"])


# Prepare data for plotting
categories = ['Fouls Comitted', 'Fouls Drawn', 'Offsides']
league_avg = [league_avg_fc, league_avg_fd, league_avg_o]
club = [club_fc, club_fd, club_o]
top_team = [top_fc, top_fd, top_o]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_fc}, {top_team_fd}, {top_team_o})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Fouls')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# MISC QUERY
# ============================================================================

misc_query = """ 
SELECT
    (SELECT AVG("Penalties Won") FROM league_stats) AS league_avg1,
    (SELECT AVG("Penalties Conceded") FROM league_stats) AS league_avg2,
    (SELECT AVG("Own Goals") FROM league_stats) AS league_avg3,
    (SELECT AVG("Second yellows") FROM league_stats) AS league_avg4,
    

    (SELECT "Penalties Won" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Penalties Conceded" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Own Goals" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Second yellows" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,

    (SELECT Team FROM league_stats ORDER BY "Penalties Won" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Penalties Conceded" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Own Goals" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Second yellows" DESC LIMIT 1) AS top_team4,

    (SELECT "Penalties Won" FROM league_stats ORDER BY "Penalties Won" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Penalties Conceded" FROM league_stats ORDER BY "Penalties Conceded" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Own Goals" FROM league_stats ORDER BY "Own Goals" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Second yellows" FROM league_stats ORDER BY "Second yellows" DESC LIMIT 1) AS top_team_stat4;
"""

misc = pd.read_sql_query(misc_query, conn)

# Extract results
league_avg_penw = float(misc.loc[0, "league_avg1"])
league_avg_penc = float(misc.loc[0, "league_avg2"])
league_avg_og = float(misc.loc[0, "league_avg3"])
league_avg_sy = float(misc.loc[0, "league_avg4"])


club_penw = float(misc.loc[0, "club1"])
club_penc = float(misc.loc[0, "club2"])
club_og = float(misc.loc[0, "club3"])
club_sy = float(misc.loc[0, "club4"])

top_team_penw = misc.loc[0, "top_team1"]
top_team_penc = misc.loc[0, "top_team2"]
top_team_og = misc.loc[0, "top_team3"]
top_team_sy = misc.loc[0, "top_team4"]

top_penw = float(misc.loc[0, "top_team_stat1"])
top_penc = float(misc.loc[0, "top_team_stat2"])
top_og = float(misc.loc[0, "top_team_stat3"])
top_sy = float(misc.loc[0, "top_team_stat4"])


# Prepare data for plotting
categories = ['Pens Won', 'Pens Conceded', 'Own Goals', 'Second yellows']
league_avg = [league_avg_penw, league_avg_penc, league_avg_og, league_avg_sy]
club = [club_penw, club_penc, club_og, club_sy]
top_team = [top_penw, top_penc, top_og, top_sy]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_penw}, {top_team_penc}, {top_team_og}, {top_team_sy})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Misc')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# AERIAL QUERY
# ============================================================================

aerial_query = """ 
SELECT
    (SELECT AVG("Aerial Duels Won") FROM league_stats) AS league_avg2,
    (SELECT AVG("Aerial Duels Lost") FROM league_stats) AS league_avg3,
    (SELECT AVG("Aerial Duels Won Percentage") FROM league_stats) AS league_avg4,


    (SELECT "Aerial Duels Won" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Aerial Duels Lost" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Aerial Duels Won Percentage" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,

    (SELECT Team FROM league_stats ORDER BY "Aerial Duels Won" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Aerial Duels Lost" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Aerial Duels Won Percentage" DESC LIMIT 1) AS top_team4,

    (SELECT "Aerial Duels Won" FROM league_stats ORDER BY "Aerial Duels Won" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Aerial Duels Lost" FROM league_stats ORDER BY "Aerial Duels Lost" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Aerial Duels Won Percentage" FROM league_stats ORDER BY "Aerial Duels Won Percentage" DESC LIMIT 1) AS top_team_stat4;
"""

aerial = pd.read_sql_query(aerial_query, conn)

# Extract results
league_avg_adw = float(aerial.loc[0, "league_avg2"])
league_avg_adl = float(aerial.loc[0, "league_avg3"])
league_avg_adwp = float(aerial.loc[0, "league_avg4"])


club_adw = float(aerial.loc[0, "club2"])
club_adl = float(aerial.loc[0, "club3"])
club_adwp = float(aerial.loc[0, "club4"])

top_team_adw = aerial.loc[0, "top_team2"]
top_team_adl = aerial.loc[0, "top_team3"]
top_team_adwp = aerial.loc[0, "top_team4"]

top_adw = float(aerial.loc[0, "top_team_stat2"])
top_adl = float(aerial.loc[0, "top_team_stat3"])
top_adwp = float(aerial.loc[0, "top_team_stat4"])


# Prepare data for plotting
categories = ['Aerial Duels Won', 'Aerial Duels Lost', 'Aerial Duels Won %']
league_avg = [league_avg_adw, league_avg_adl, league_avg_adwp]
club = [club_adw, club_adl, club_adwp]
top_team = [top_adw, top_adl, top_adwp]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_adw}, {top_team_adl}, {top_team_adwp})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Aerial')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# GOALKEEPING QUERY
# ============================================================================

goalkeeping_query = """ 
SELECT
    (SELECT AVG("Goals Against") FROM league_stats) AS league_avg1,
    (SELECT AVG("SoTA") FROM league_stats) AS league_avg2,
    (SELECT AVG("Saves") FROM league_stats) AS league_avg3,
    (SELECT AVG("Clean Sheets") FROM league_stats) AS league_avg4,


    (SELECT "Goals Against" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "SoTA" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Saves" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Clean Sheets" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,

    (SELECT Team FROM league_stats ORDER BY "Goals Against" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "SoTA" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Saves" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Clean Sheets" DESC LIMIT 1) AS top_team4,

    (SELECT "Goals Against" FROM league_stats ORDER BY "Goals Against" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "SoTA" FROM league_stats ORDER BY "SoTA" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Saves" FROM league_stats ORDER BY "Saves" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Clean Sheets" FROM league_stats ORDER BY "Clean Sheets" DESC LIMIT 1) AS top_team_stat4;
"""

goalkeeping = pd.read_sql_query(goalkeeping_query, conn)

# Extract results
league_avg_ga = float(goalkeeping.loc[0, "league_avg1"])
league_avg_sota = float(goalkeeping.loc[0, "league_avg2"])
league_avg_save = float(goalkeeping.loc[0, "league_avg3"])
league_avg_cs = float(goalkeeping.loc[0, "league_avg4"])


club_ga = float(goalkeeping.loc[0, "club1"])
club_sota = float(goalkeeping.loc[0, "club2"])
club_save = float(goalkeeping.loc[0, "club3"])
club_cs = float(goalkeeping.loc[0, "club4"])

top_team_ga = goalkeeping.loc[0, "top_team1"]
top_team_sota = goalkeeping.loc[0, "top_team2"]
top_team_save = goalkeeping.loc[0, "top_team3"]
top_team_cs = goalkeeping.loc[0, "top_team4"]

top_ga = float(goalkeeping.loc[0, "top_team_stat1"])
top_sota = float(goalkeeping.loc[0, "top_team_stat2"])
top_save = float(goalkeeping.loc[0, "top_team_stat3"])
top_cs = float(goalkeeping.loc[0, "top_team_stat4"])


# Prepare data for plotting
categories = ['Goals Against', 'SoTA', 'Saves', 'Clean Sheets']
league_avg = [league_avg_ga, league_avg_sota, league_avg_save, league_avg_cs]
club = [club_ga, club_sota, club_save, club_cs]
top_team = [top_ga, top_sota, top_save, top_cs]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_ga}, {top_team_sota}, {top_team_save}, {top_team_cs})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Goalkeeping')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()



# ============================================================================
# GOALKEEPING PENS QUERY
# ============================================================================

goalkeeping_pens_query = """ 
SELECT
    (SELECT AVG("Penalties Faced") FROM league_stats) AS league_avg1,
    (SELECT AVG("Penalties Scored Against") FROM league_stats) AS league_avg2,
    (SELECT AVG("Penalties Saved") FROM league_stats) AS league_avg3,
    (SELECT AVG("Penalties Missed Against") FROM league_stats) AS league_avg4,


    (SELECT "Penalties Faced" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Penalties Scored Against" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Penalties Saved" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Penalties Missed Against" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,

    (SELECT Team FROM league_stats ORDER BY "Penalties Faced" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Penalties Scored Against" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Penalties Saved" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Penalties Missed Against" DESC LIMIT 1) AS top_team4,

    (SELECT "Penalties Faced" FROM league_stats ORDER BY "Penalties Faced" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Penalties Scored Against" FROM league_stats ORDER BY "Penalties Scored Against" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Penalties Saved" FROM league_stats ORDER BY "Penalties Saved" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Penalties Missed Against" FROM league_stats ORDER BY "Penalties Missed Against" DESC LIMIT 1) AS top_team_stat4;
"""

goalkeeping_pens = pd.read_sql_query(goalkeeping_pens_query, conn)

# Extract results
league_avg_pf = float(goalkeeping_pens.loc[0, "league_avg1"])
league_avg_psa = float(goalkeeping_pens.loc[0, "league_avg2"])
league_avg_psave = float(goalkeeping_pens.loc[0, "league_avg3"])
league_avg_pma = float(goalkeeping_pens.loc[0, "league_avg4"])


club_pf = float(goalkeeping_pens.loc[0, "club1"])
club_psa = float(goalkeeping_pens.loc[0, "club2"])
club_psave = float(goalkeeping_pens.loc[0, "club3"])
club_pma = float(goalkeeping_pens.loc[0, "club4"])

top_team_pf = goalkeeping_pens.loc[0, "top_team1"]
top_team_psa = goalkeeping_pens.loc[0, "top_team2"]
top_team_psave = goalkeeping_pens.loc[0, "top_team3"]
top_team_pma = goalkeeping_pens.loc[0, "top_team4"]

top_pf = float(goalkeeping_pens.loc[0, "top_team_stat1"])
top_psa = float(goalkeeping_pens.loc[0, "top_team_stat2"])
top_psave = float(goalkeeping_pens.loc[0, "top_team_stat3"])
top_pma = float(goalkeeping_pens.loc[0, "top_team_stat4"])


# Prepare data for plotting
categories = ['Penalties Faced', 'Penalties Scored Against', 'Penalties Saved', 'Penalties Missed Against']
league_avg = [league_avg_pf, league_avg_psa, league_avg_psave, league_avg_pma]
club = [club_pf, club_psa, club_psave, club_pma]
top_team = [top_pf, top_psa, top_psave, top_pma]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_pf}, {top_team_psa}, {top_team_psave}, {top_team_pma})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Goalkeeping Pens')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# GOALS AGAINST QUERY
# ============================================================================

goals_against_query = """ 
SELECT
    (SELECT AVG("Free Kick Goals Against") FROM league_stats) AS league_avg1,
    (SELECT AVG("Corner Goals Against") FROM league_stats) AS league_avg2,
    (SELECT AVG("Own Goals Against") FROM league_stats) AS league_avg3,

    
    (SELECT "Free Kick Goals Against" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Corner Goals Against" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Own Goals Against" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,

    (SELECT Team FROM league_stats ORDER BY "Free Kick Goals Against" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Corner Goals Against" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Own Goals Against" DESC LIMIT 1) AS top_team3,

    (SELECT "Free Kick Goals Against" FROM league_stats ORDER BY "Free Kick Goals Against" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Corner Goals Against" FROM league_stats ORDER BY "Corner Goals Against" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Own Goals Against" FROM league_stats ORDER BY "Own Goals Against" DESC LIMIT 1) AS top_team_stat3;
"""

goals_against = pd.read_sql_query(goals_against_query, conn)

# Extract results
league_avg_fkga = float(goals_against.loc[0, "league_avg1"])
league_avg_cga = float(goals_against.loc[0, "league_avg2"])
league_avg_oga = float(goals_against.loc[0, "league_avg3"])


club_fkga = float(goals_against.loc[0, "club1"])
club_cga = float(goals_against.loc[0, "club2"])
club_oga = float(goals_against.loc[0, "club3"])

top_team_fkga = goals_against.loc[0, "top_team1"]
top_team_cga = goals_against.loc[0, "top_team2"]
top_team_oga = goals_against.loc[0, "top_team3"]

top_fkga = float(goals_against.loc[0, "top_team_stat1"])
top_cga = float(goals_against.loc[0, "top_team_stat2"])
top_oga = float(goals_against.loc[0, "top_team_stat3"])


# Prepare data for plotting
categories = ['Free Kick Goals Against', 'Corner Goals Against', 'Own Goals Against']
league_avg = [league_avg_fkga, league_avg_cga, league_avg_oga]
club = [club_fkga, club_cga, club_oga]
top_team = [top_fkga, top_cga, top_oga]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_fkga}, {top_team_cga}, {top_team_oga})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Goals Against')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()



# ============================================================================
# PSxG QUERY
# ============================================================================

PSxG_query = """ 
SELECT
    (SELECT AVG("PSxG") FROM league_stats) AS league_avg1,
    (SELECT AVG("PSxG per Shot on Target") FROM league_stats) AS league_avg2,
    (SELECT AVG("PSxG +/-") FROM league_stats) AS league_avg3,
    
    
    (SELECT "PSxG" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "PSxG per Shot on Target" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "PSxG +/-" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,

    (SELECT Team FROM league_stats ORDER BY "PSxG" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "PSxG per Shot on Target" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "PSxG +/-" DESC LIMIT 1) AS top_team3,

    (SELECT "PSxG" FROM league_stats ORDER BY "PSxG" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "PSxG per Shot on Target" FROM league_stats ORDER BY "PSxG per Shot on Target" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "PSxG +/-" FROM league_stats ORDER BY "PSxG +/-" DESC LIMIT 1) AS top_team_stat3;
"""

PSxG = pd.read_sql_query(PSxG_query, conn)

# Extract results
league_avg_psxg = float(PSxG.loc[0, "league_avg1"])
league_avg_psxgpsot = float(PSxG.loc[0, "league_avg2"])
league_avg_psxgpom = float(PSxG.loc[0, "league_avg3"])


club_psxg = float(PSxG.loc[0, "club1"])
club_psxgpsot = float(PSxG.loc[0, "club2"])
club_psxgpom = float(PSxG.loc[0, "club3"])

top_team_psxg = PSxG.loc[0, "top_team1"]
top_team_psxgpsot = PSxG.loc[0, "top_team2"]
top_team_psxgpom = PSxG.loc[0, "top_team3"]

top_psxg = float(PSxG.loc[0, "top_team_stat1"])
top_psxgpsot = float(PSxG.loc[0, "top_team_stat2"])
top_psxgpom = float(PSxG.loc[0, "top_team_stat3"])


# Prepare data for plotting
categories = ['PSxG', 'PSxG per Shot on Target', 'PSxG +/-']
league_avg = [league_avg_psxg, league_avg_psxgpsot, league_avg_psxgpom]
club = [club_psxg, club_psxgpsot, club_psxgpom]
top_team = [top_psxg, top_psxgpsot, top_psxgpom]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_psxg}, {top_team_psxgpsot}, {top_team_psxgpom})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('PSxG')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()



# ============================================================================
# LAUNCHES QUERY
# ============================================================================

launches_query = """ 
SELECT
    (SELECT AVG("Launches Completed") FROM league_stats) AS league_avg1,
    (SELECT AVG("Launches Attempted") FROM league_stats) AS league_avg2,
    (SELECT AVG("Launch Completion Percentage") FROM league_stats) AS league_avg3,
    
    
    (SELECT "Launches Completed" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Launches Attempted" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Launch Completion Percentage" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,

    (SELECT Team FROM league_stats ORDER BY "Launches Completed" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Launches Attempted" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Launch Completion Percentage" DESC LIMIT 1) AS top_team3,

    (SELECT "Launches Completed" FROM league_stats ORDER BY "Launches Completed" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Launches Attempted" FROM league_stats ORDER BY "Launches Attempted" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Launch Completion Percentage" FROM league_stats ORDER BY "Launch Completion Percentage" DESC LIMIT 1) AS top_team_stat3;
"""

launches = pd.read_sql_query(launches_query, conn)

# Extract results
league_avg_l = float(launches.loc[0, "league_avg1"])
league_avg_la = float(launches.loc[0, "league_avg2"])
league_avg_lcp = float(launches.loc[0, "league_avg3"])


club_l = float(launches.loc[0, "club1"])
club_la = float(launches.loc[0, "club2"])
club_lcp = float(launches.loc[0, "club3"])

top_team_l = launches.loc[0, "top_team1"]
top_team_la = launches.loc[0, "top_team2"]
top_team_lcp = launches.loc[0, "top_team3"]

top_l = float(launches.loc[0, "top_team_stat1"])
top_la = float(launches.loc[0, "top_team_stat2"])
top_lcp = float(launches.loc[0, "top_team_stat3"])


# Prepare data for plotting
categories = ['Launches Completed', 'Launches Attempted', 'Launch Completion Percentage']
league_avg = [league_avg_l, league_avg_la, league_avg_lcp]
club = [club_l, club_la, club_lcp]
top_team = [top_l, top_la, top_lcp]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_l}, {top_team_la}, {top_team_lcp})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Launches')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# GOALKEEPING PASS QUERY
# ============================================================================

goalkeeping_pass_query = """ 
SELECT
    (SELECT AVG("Goalkeeper Passes") FROM league_stats) AS league_avg1,
    (SELECT AVG("Goalkeeper Throws") FROM league_stats) AS league_avg2,
    (SELECT AVG("Launch Percentage") FROM league_stats) AS league_avg3,
    (SELECT AVG("Goalkeeper Avg Pass Length") FROM league_stats) AS league_avg4,
    

    (SELECT "Goalkeeper Passes" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Goalkeeper Throws" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Launch Percentage" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Goalkeeper Avg Pass Length" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,

    (SELECT Team FROM league_stats ORDER BY "Goalkeeper Passes" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Goalkeeper Throws" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Launch Percentage" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Goalkeeper Avg Pass Length" DESC LIMIT 1) AS top_team4,

    (SELECT "Goalkeeper Passes" FROM league_stats ORDER BY "Goalkeeper Passes" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Goalkeeper Throws" FROM league_stats ORDER BY "Goalkeeper Throws" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Launch Percentage" FROM league_stats ORDER BY "Launch Percentage" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Goalkeeper Avg Pass Length" FROM league_stats ORDER BY "Goalkeeper Avg Pass Length" DESC LIMIT 1) AS top_team_stat4;
"""

goalkeeping_pass = pd.read_sql_query(goalkeeping_pass_query, conn)

# Extract results
league_avg_gp = float(goalkeeping_pass.loc[0, "league_avg1"])
league_avg_gt = float(goalkeeping_pass.loc[0, "league_avg2"])
league_avg_lap = float(goalkeeping_pass.loc[0, "league_avg3"])
league_avg_gapl = float(goalkeeping_pass.loc[0, "league_avg4"])


club_gp = float(goalkeeping_pass.loc[0, "club1"])
club_gt = float(goalkeeping_pass.loc[0, "club2"])
club_lap = float(goalkeeping_pass.loc[0, "club3"])
club_gapl = float(goalkeeping_pass.loc[0, "club4"])

top_team_gp = goalkeeping_pass.loc[0, "top_team1"]
top_team_gt = goalkeeping_pass.loc[0, "top_team2"]
top_team_lap = goalkeeping_pass.loc[0, "top_team3"]
top_team_gapl = goalkeeping_pass.loc[0, "top_team4"]

top_gp = float(goalkeeping_pass.loc[0, "top_team_stat1"])
top_gt = float(goalkeeping_pass.loc[0, "top_team_stat2"])
top_lap = float(goalkeeping_pass.loc[0, "top_team_stat3"])
top_gapl = float(goalkeeping_pass.loc[0, "top_team_stat4"])


# Prepare data for plotting
categories = ['Goalkeeper Passes', 'Goalkeeper Throws', 'Launch Percentage', 'Goalkeeper Avg Pass Length']
league_avg = [league_avg_gp, league_avg_gt, league_avg_lap, league_avg_gapl]
club = [club_gp, club_gt, club_lap, club_gapl]
top_team = [top_gp, top_gt, top_lap, top_gapl]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_gp}, {top_team_gt}, {top_team_lap}, {top_team_gapl})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Goalkeeping Pass')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# GOAL KICKS QUERY
# ============================================================================

goal_kicks_query = """ 
SELECT
    (SELECT AVG("Goal Kicks") FROM league_stats) AS league_avg1,
    (SELECT AVG("Goal Kicks Launched") FROM league_stats) AS league_avg2,
    (SELECT AVG("Avg Goal Kick Length") FROM league_stats) AS league_avg3,
    
    
    (SELECT "Goal Kicks" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Goal Kicks Launched" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Avg Goal Kick Length" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,

    (SELECT Team FROM league_stats ORDER BY "Goal Kicks" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Goal Kicks Launched" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Avg Goal Kick Length" DESC LIMIT 1) AS top_team3,

    (SELECT "Goal Kicks" FROM league_stats ORDER BY "Goal Kicks" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Goal Kicks Launched" FROM league_stats ORDER BY "Goal Kicks Launched" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Avg Goal Kick Length" FROM league_stats ORDER BY "Avg Goal Kick Length" DESC LIMIT 1) AS top_team_stat3;
"""

goal_kicks = pd.read_sql_query(goal_kicks_query, conn)

# Extract results
league_avg_gk = float(goal_kicks.loc[0, "league_avg1"])
league_avg_gkl = float(goal_kicks.loc[0, "league_avg2"])
league_avg_agkl = float(goal_kicks.loc[0, "league_avg3"])


club_gk = float(goal_kicks.loc[0, "club1"])
club_gkl = float(goal_kicks.loc[0, "club2"])
club_agkl = float(goal_kicks.loc[0, "club3"])

top_team_gk = goal_kicks.loc[0, "top_team1"]
top_team_gkl = goal_kicks.loc[0, "top_team2"]
top_team_agkl = goal_kicks.loc[0, "top_team3"]

top_gk = float(goal_kicks.loc[0, "top_team_stat1"])
top_gkl = float(goal_kicks.loc[0, "top_team_stat2"])
top_agkl = float(goal_kicks.loc[0, "top_team_stat3"])


# Prepare data for plotting
categories = ['Goal Kicks', 'Goal Kicks Launched', 'Avg Goal Kick Length']
league_avg = [league_avg_gk, league_avg_gkl, league_avg_agkl]
club = [club_gk, club_gkl, club_agkl]
top_team = [top_gk, top_gkl, top_agkl]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_gk}, {top_team_gkl}, {top_team_agkl})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Goal Kicks')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()



# ============================================================================
# GOALKEEPER CROSSES QUERY
# ============================================================================

goalkeeper_crosses_query = """ 
SELECT
    (SELECT AVG("Crosses Faced") FROM league_stats) AS league_avg1,
    (SELECT AVG("Crosses Stopped") FROM league_stats) AS league_avg2,
    (SELECT AVG("Crosses Stopped Percentage") FROM league_stats) AS league_avg3,
    
    
    (SELECT "Crosses Faced" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Crosses Stopped" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Crosses Stopped Percentage" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,

    (SELECT Team FROM league_stats ORDER BY "Crosses Faced" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Crosses Stopped" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Crosses Stopped Percentage" DESC LIMIT 1) AS top_team3,

    (SELECT "Crosses Faced" FROM league_stats ORDER BY "Crosses Faced" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Crosses Stopped" FROM league_stats ORDER BY "Crosses Stopped" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Crosses Stopped Percentage" FROM league_stats ORDER BY "Crosses Stopped Percentage" DESC LIMIT 1) AS top_team_stat3;
"""

goalkeeper_crosses = pd.read_sql_query(goalkeeper_crosses_query, conn)

# Extract results
league_avg_cf = float(goalkeeper_crosses.loc[0, "league_avg1"])
league_avg_crs = float(goalkeeper_crosses.loc[0, "league_avg2"])
league_avg_csp = float(goalkeeper_crosses.loc[0, "league_avg3"])


club_cf = float(goalkeeper_crosses.loc[0, "club1"])
club_crs = float(goalkeeper_crosses.loc[0, "club2"])
club_csp = float(goalkeeper_crosses.loc[0, "club3"])

top_team_cf = goalkeeper_crosses.loc[0, "top_team1"]
top_team_crs = goalkeeper_crosses.loc[0, "top_team2"]
top_team_csp = goalkeeper_crosses.loc[0, "top_team3"]

top_cf = float(goalkeeper_crosses.loc[0, "top_team_stat1"])
top_crs = float(goalkeeper_crosses.loc[0, "top_team_stat2"])
top_csp = float(goalkeeper_crosses.loc[0, "top_team_stat3"])


# Prepare data for plotting
categories = ['Crosses Faced', 'Crosses Stopped', 'Crosses Stopped Percentage']
league_avg = [league_avg_cf, league_avg_crs, league_avg_csp]
club = [club_cf, club_crs, club_csp]
top_team = [top_cf, top_crs, top_csp]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_cf}, {top_team_crs}, {top_team_csp})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Goalkeeper Crosses')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# SWEEPER QUERY
# ============================================================================

sweeper_query = """ 
SELECT
    (SELECT AVG("Sweeper Actions") FROM league_stats) AS league_avg1,
    (SELECT AVG("Avg Sweeper Distance") FROM league_stats) AS league_avg2,
    
    
    (SELECT "Sweeper Actions" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Avg Sweeper Distance" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,

    (SELECT Team FROM league_stats ORDER BY "Sweeper Actions" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Avg Sweeper Distance" DESC LIMIT 1) AS top_team2,

    (SELECT "Sweeper Actions" FROM league_stats ORDER BY "Sweeper Actions" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Avg Sweeper Distance" FROM league_stats ORDER BY "Avg Sweeper Distance" DESC LIMIT 1) AS top_team_stat2;
"""

sweeper = pd.read_sql_query(sweeper_query, conn)

# Extract results
league_avg_sa = float(sweeper.loc[0, "league_avg1"])
league_avg_aswd = float(sweeper.loc[0, "league_avg2"])


club_sa = float(sweeper.loc[0, "club1"])
club_aswd = float(sweeper.loc[0, "club2"])

top_team_sa = sweeper.loc[0, "top_team1"]
top_team_aswd = sweeper.loc[0, "top_team2"]

top_sa = float(sweeper.loc[0, "top_team_stat1"])
top_aswd = float(sweeper.loc[0, "top_team_stat2"])


# Prepare data for plotting
categories = ['Sweeper Actions', 'Avg Sweeper Distance']
league_avg = [league_avg_sa, league_avg_aswd]
club = [club_sa, club_aswd]
top_team = [top_sa, top_aswd]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_sa}, {top_team_aswd})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Sweeper')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# PASS TYPES 1 QUERY
# ============================================================================

pass_types_1_query = """ 
SELECT
    (SELECT AVG("Live Ball Passes") FROM league_stats) AS league_avg1,
    (SELECT AVG("Dead Ball Passes") FROM league_stats) AS league_avg2,
    (SELECT AVG("Crosses") FROM league_stats) AS league_avg6,
    (SELECT AVG("Throw Ins") FROM league_stats) AS league_avg7,
    

    (SELECT "Live Ball Passes" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Dead Ball Passes" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Crosses" FROM league_stats WHERE Team = 'Canberra Utd') AS club6,
    (SELECT "Throw Ins" FROM league_stats WHERE Team = 'Canberra Utd') AS club7,

    (SELECT Team FROM league_stats ORDER BY "Live Ball Passes" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Dead Ball Passes" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Crosses" DESC LIMIT 1) AS top_team6,
    (SELECT Team FROM league_stats ORDER BY "Throw Ins" DESC LIMIT 1) AS top_team7,

    (SELECT "Live Ball Passes" FROM league_stats ORDER BY "Live Ball Passes" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Dead Ball Passes" FROM league_stats ORDER BY "Dead Ball Passes" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Crosses" FROM league_stats ORDER BY "Crosses" DESC LIMIT 1) AS top_team_stat6,
    (SELECT "Throw Ins" FROM league_stats ORDER BY "Throw Ins" DESC LIMIT 1) AS top_team_stat7;
"""

pass_types = pd.read_sql_query(pass_types_1_query, conn)

# Extract results
league_avg_lbp = float(pass_types.loc[0, "league_avg1"])
league_avg_dbp = float(pass_types.loc[0, "league_avg2"])
league_avg_cross = float(pass_types.loc[0, "league_avg6"])
league_avg_ti = float(pass_types.loc[0, "league_avg7"])


club_lbp = float(pass_types.loc[0, "club1"])
club_dbp = float(pass_types.loc[0, "club2"])
club_cross = float(pass_types.loc[0, "club6"])
club_ti = float(pass_types.loc[0, "club7"])

top_team_lbp = pass_types.loc[0, "top_team1"]
top_team_dbp = pass_types.loc[0, "top_team2"]
top_team_cross = pass_types.loc[0, "top_team6"]
top_team_ti = pass_types.loc[0, "top_team7"]

top_lbp = float(pass_types.loc[0, "top_team_stat1"])
top_dbp = float(pass_types.loc[0, "top_team_stat2"])
top_cross = float(pass_types.loc[0, "top_team_stat6"])
top_ti = float(pass_types.loc[0, "top_team_stat7"])

# Prepare data for plotting
categories = ['Live Ball Passes', 'Dead Ball Passes', 'Crosses', 'Throw Ins']
league_avg = [league_avg_lbp, league_avg_dbp, league_avg_cross, league_avg_ti]
club = [club_lbp, club_dbp, club_cross, club_ti]
top_team = [top_lbp, top_dbp, top_cross, top_ti]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_lbp}, {top_team_dbp}, {top_team_cross}, {top_team_ti})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Pass Types 1')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()



# ============================================================================
# PASS TYPES 2 QUERY
# ============================================================================

pass_types_2_query = """ 
SELECT
    (SELECT AVG("Free Kick Passes") FROM league_stats) AS league_avg3,
    (SELECT AVG("Through Balls") FROM league_stats) AS league_avg4,
    (SELECT AVG("Switches") FROM league_stats) AS league_avg5,
    (SELECT AVG("Corners") FROM league_stats) AS league_avg8,
    

    (SELECT "Free Kick Passes" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,
    (SELECT "Through Balls" FROM league_stats WHERE Team = 'Canberra Utd') AS club4,
    (SELECT "Switches" FROM league_stats WHERE Team = 'Canberra Utd') AS club5,
    (SELECT "Corners" FROM league_stats WHERE Team = 'Canberra Utd') AS club8,

    (SELECT Team FROM league_stats ORDER BY "Free Kick Passes" DESC LIMIT 1) AS top_team3,
    (SELECT Team FROM league_stats ORDER BY "Through Balls" DESC LIMIT 1) AS top_team4,
    (SELECT Team FROM league_stats ORDER BY "Switches" DESC LIMIT 1) AS top_team5,
    (SELECT Team FROM league_stats ORDER BY "Corners" DESC LIMIT 1) AS top_team8,

    (SELECT "Free Kick Passes" FROM league_stats ORDER BY "Free Kick Passes" DESC LIMIT 1) AS top_team_stat3,
    (SELECT "Through Balls" FROM league_stats ORDER BY "Through Balls" DESC LIMIT 1) AS top_team_stat4,
    (SELECT "Switches" FROM league_stats ORDER BY "Switches" DESC LIMIT 1) AS top_team_stat5,
    (SELECT "Corners" FROM league_stats ORDER BY "Crosses" DESC LIMIT 1) AS top_team_stat8;
"""

pass_types_2 = pd.read_sql_query(pass_types_2_query, conn)

# Extract results
league_avg_fkp = float(pass_types_2.loc[0, "league_avg3"])
league_avg_tb = float(pass_types_2.loc[0, "league_avg4"])
league_avg_switch = float(pass_types_2.loc[0, "league_avg5"])
league_avg_corn = float(pass_types_2.loc[0, "league_avg8"])


club_fkp = float(pass_types_2.loc[0, "club3"])
club_tb = float(pass_types_2.loc[0, "club4"])
club_switch = float(pass_types_2.loc[0, "club5"])
club_corn = float(pass_types_2.loc[0, "club8"])

top_team_fkp = pass_types_2.loc[0, "top_team3"]
top_team_tb = pass_types_2.loc[0, "top_team4"]
top_team_switch = pass_types_2.loc[0, "top_team5"]
top_team_corn = pass_types_2.loc[0, "top_team8"]

top_fkp = float(pass_types_2.loc[0, "top_team_stat3"])
top_tb = float(pass_types_2.loc[0, "top_team_stat4"])
top_switch = float(pass_types_2.loc[0, "top_team_stat5"])
top_corn = float(pass_types_2.loc[0, "top_team_stat8"])

# Prepare data for plotting
categories = ['Free Kick Passes', 'Through Balls', 'Switches', 'Corners']
league_avg = [league_avg_fkp, league_avg_tb, league_avg_switch, league_avg_corn]
club = [club_fkp, club_tb, club_switch, club_corn]
top_team = [top_fkp, top_tb, top_switch, top_corn]

# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_fkp}, {top_team_tb}, {top_team_switch}, {top_team_corn})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Pass Types 2')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# CORNERS QUERY
# ============================================================================

corners_query = """ 
SELECT
    (SELECT AVG("Inswinging Corners") FROM league_stats) AS league_avg1,
    (SELECT AVG("Outswinging Corners") FROM league_stats) AS league_avg2,
    (SELECT AVG("Straight Corners") FROM league_stats) AS league_avg3,
    
    
    (SELECT "Inswinging Corners" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Outswinging Corners" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,
    (SELECT "Straight Corners" FROM league_stats WHERE Team = 'Canberra Utd') AS club3,

    (SELECT Team FROM league_stats ORDER BY "Inswinging Corners" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Outswinging Corners" DESC LIMIT 1) AS top_team2,
    (SELECT Team FROM league_stats ORDER BY "Straight Corners" DESC LIMIT 1) AS top_team3,

    (SELECT "Inswinging Corners" FROM league_stats ORDER BY "Inswinging Corners" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Outswinging Corners" FROM league_stats ORDER BY "Outswinging Corners" DESC LIMIT 1) AS top_team_stat2,
    (SELECT "Straight Corners" FROM league_stats ORDER BY "Straight Corners" DESC LIMIT 1) AS top_team_stat3;
"""

corners = pd.read_sql_query(corners_query, conn)

# Extract results
league_avg_ic = float(corners.loc[0, "league_avg1"])
league_avg_oc = float(corners.loc[0, "league_avg2"])
league_avg_sc = float(corners.loc[0, "league_avg3"])


club_ic = float(corners.loc[0, "club1"])
club_oc = float(corners.loc[0, "club2"])
club_sc = float(corners.loc[0, "club3"])

top_team_ic = corners.loc[0, "top_team1"]
top_team_oc = corners.loc[0, "top_team2"]
top_team_sc = corners.loc[0, "top_team3"]

top_ic = float(corners.loc[0, "top_team_stat1"])
top_oc = float(corners.loc[0, "top_team_stat2"])
top_sc = float(corners.loc[0, "top_team_stat3"])


# Prepare data for plotting
categories = ['Inswinging Corners', 'Outswinging Corners', 'Straight Corners']
league_avg = [league_avg_ic, league_avg_oc, league_avg_sc]
club = [club_ic, club_oc, club_sc]
top_team = [top_ic, top_oc, top_sc]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_ic}, {top_team_oc}, {top_team_sc})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Corners')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


# ============================================================================
# PASS MISTAKES QUERY
# ============================================================================

pass_mistakes_query = """ 
SELECT
    (SELECT AVG("Passes Offside") FROM league_stats) AS league_avg1,
    (SELECT AVG("Passes Blocked") FROM league_stats) AS league_avg2,
    
    
    (SELECT "Passes Offside" FROM league_stats WHERE Team = 'Canberra Utd') AS club1,
    (SELECT "Passes Blocked" FROM league_stats WHERE Team = 'Canberra Utd') AS club2,

    (SELECT Team FROM league_stats ORDER BY "Passes Offside" DESC LIMIT 1) AS top_team1,
    (SELECT Team FROM league_stats ORDER BY "Passes Blocked" DESC LIMIT 1) AS top_team2,

    (SELECT "Passes Offside" FROM league_stats ORDER BY "Passes Offside" DESC LIMIT 1) AS top_team_stat1,
    (SELECT "Passes Blocked" FROM league_stats ORDER BY "Passes Blocked" DESC LIMIT 1) AS top_team_stat2;
"""

pass_mistakes = pd.read_sql_query(pass_mistakes_query, conn)

# Extract results
league_avg_po = float(pass_mistakes.loc[0, "league_avg1"])
league_avg_pb = float(pass_mistakes.loc[0, "league_avg2"])


club_po = float(pass_mistakes.loc[0, "club1"])
club_pb = float(pass_mistakes.loc[0, "club2"])

top_team_po = pass_mistakes.loc[0, "top_team1"]
top_team_pb = pass_mistakes.loc[0, "top_team2"]

top_po = float(pass_mistakes.loc[0, "top_team_stat1"])
top_pb = float(pass_mistakes.loc[0, "top_team_stat2"])


# Prepare data for plotting
categories = ['Passes Offside', 'Passes Blocked']
league_avg = [league_avg_po, league_avg_pb]
club = [club_po, club_pb]
top_team = [top_po, top_pb]


# X-axis positions
x = np.arange(len(categories))
width = 0.2  # width of the bars

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - 1.5*width, league_avg, width, label='League Avg', color='lightgrey')
bars3 = ax.bar(x + 0.5*width, club, width, label='Canberra Utd', color='green')
bars4 = ax.bar(x + 1.5*width, top_team, width, 
               label=f'Top Teams ({top_team_po}, {top_team_pb})', color='gold')

# Labels and title
ax.set_xlabel('Stat Category')
ax.set_ylabel('Count')
ax.set_title('Pass Mistakes')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Add value labels
for bars in [bars1, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()




