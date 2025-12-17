#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 19:13:45 2025

@author: benharris
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
import plotly.express as px


df = pd.read_csv('all_squad_stats_matchlogs_24-25(A-League-Womens).csv')

# Load in SQL
conn = sqlite3.connect(':memory:')
df.to_sql('league_stats_matchlogs', conn, index=False, if_exists='replace')


# ============================================================================
# GOALS VS xG FOR QUERY
# ============================================================================
goals_vs_xg_for_query = """
SELECT
    Team,
    Date,
    Result,
    "Goals For",
    "Goals Against",
    Opponent,
    "xG For",
    "xG Against"
FROM league_stats_matchlogs
ORDER BY Date
"""

goals_vs_xg_for = pd.read_sql_query(goals_vs_xg_for_query, conn)

# Convert Date
goals_vs_xg_for["Date"] = pd.to_datetime(goals_vs_xg_for["Date"])

# ---- STATIC MATPLOTLIB PLOT ---- #
plt.figure(figsize=(14, 6))

# Plot xG For
plt.plot(goals_vs_xg_for["Date"], goals_vs_xg_for["Goals For"], marker='o', label="Goals For")


# Plot xG Against
plt.plot(goals_vs_xg_for["Date"], goals_vs_xg_for["xG For"], marker='o', label="xG For")


# Annotate Result + Opponent
for i, row in goals_vs_xg_for.iterrows():
    plt.annotate(
        f"{row['Result']} vs {row['Opponent']}",
        (row["Date"], row["Goals For"]),
        textcoords="offset points",
        xytext=(0, 8),
        ha='center',
        fontsize=8
    )

plt.title("Goals For vs xG For Across the Season")
plt.xlabel("Date")
plt.ylabel("Goals/xG")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()

# ============================================================================
# GOALS VS xG AGAINST QUERY
# ============================================================================
goals_vs_xg_against_query = """
SELECT
    Team,
    Date,
    Result,
    "Goals For",
    "Goals Against",
    Opponent,
    "xG For",
    "xG Against"
FROM league_stats_matchlogs
ORDER BY Date
"""

goals_vs_xg_against = pd.read_sql_query(goals_vs_xg_against_query, conn)

# Convert Date
goals_vs_xg_against["Date"] = pd.to_datetime(goals_vs_xg_against["Date"])

# ---- STATIC MATPLOTLIB PLOT ---- #
plt.figure(figsize=(14, 6))

# Plot xG For
plt.plot(goals_vs_xg_against["Date"], goals_vs_xg_against["Goals Against"], marker='o', label="Goals Against")

# Plot xG Against
plt.plot(goals_vs_xg_against["Date"], goals_vs_xg_against["xG Against"], marker='o', label="xG Against")

# Annotate Result + Opponent
for i, row in goals_vs_xg_against.iterrows():
    plt.annotate(
        f"{row['Result']} vs {row['Opponent']}",
        (row["Date"], row["Goals Against"]),
        textcoords="offset points",
        xytext=(0, 8),
        ha='center',
        fontsize=8
    )

plt.title("Goals Against vs xG Against Across the Season")
plt.xlabel("Date")
plt.ylabel("Goals/xG")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()

# ============================================================================
# GOALS AND xG QUERY
# ============================================================================
query = """
SELECT
    Opponent,
    SUM("Goals For") AS total_goals_for,
    SUM("xG For") AS total_xg_for,
    SUM("Goals Against") AS total_goals_against,
    SUM("xG Against") AS total_xg_against,

    SUM(CASE WHEN Result LIKE 'W%' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN Result LIKE 'D%' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN Result LIKE 'L%' THEN 1 ELSE 0 END) AS losses

FROM league_stats_matchlogs
GROUP BY Opponent
ORDER BY Opponent;
"""
df_summary = pd.read_sql_query(query, conn)

opponents = df_summary['Opponent']
x = np.arange(len(opponents))
width = 0.2

fig, ax = plt.subplots(figsize=(12, 6))

bars_gf = ax.bar(x - 1.5*width, df_summary['total_goals_for'], width, label='Goals For', color='green')
bars_xgf = ax.bar(x - 0.5*width, df_summary['total_xg_for'], width, label='xG For', color='yellow')
bars_ga = ax.bar(x + 0.5*width, df_summary['total_goals_against'], width, label='Goals Against')
bars_xga = ax.bar(x + 1.5*width, df_summary['total_xg_against'], width, label='xG Against')

# Add number annotations on top of each bar
def annotate_bars(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3),  # offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

for bars in [bars_gf, bars_xgf, bars_ga, bars_xga]:
    annotate_bars(bars)

ax.set_xlabel('Opponent')
ax.set_ylabel('Totals')
ax.set_title('Goals & xG For/Against by Opponent')
ax.set_xticks(x)
ax.set_xticklabels(opponents, rotation=45, ha='right')

ax.legend()
plt.tight_layout()
plt.show()









# Results plot
result_df = pd.read_sql_query(query, conn)

# Plot grouped bar chart
opponents = result_df['Opponent']
width = 0.25
x = range(len(opponents))

plt.figure(figsize=(10,6))
plt.bar([i - width for i in x], result_df['wins'], width=width, label='Wins', color='green')
plt.bar(x, result_df['draws'], width=width, label='Draws', color='orange')
plt.bar([i + width for i in x], result_df['losses'], width=width, label='Losses', color='red')

# Add number annotations
for i in x:
    plt.text(i - width, result_df['wins'][i] + 0.05, result_df['wins'][i], ha='center', va='bottom')
    plt.text(i, result_df['draws'][i] + 0.05, result_df['draws'][i], ha='center', va='bottom')
    plt.text(i + width, result_df['losses'][i] + 0.05, result_df['losses'][i], ha='center', va='bottom')

plt.xticks(x, opponents, rotation=45, ha='right')
plt.ylabel('Number of Matches')
plt.title('Wins, Draws, and Losses vs Each Opponent')
plt.legend()
plt.tight_layout()
plt.show()












# ============================================================================
# ROLLING AVERAGE GOALS AND xG PLOTS
# ============================================================================
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Encode results
df['Result_num'] = df['Result'].map({'W':3, 'D':1, 'L':0})

# Rolling window
window = 3
rolling_goals = ['Goals For','Goals Against']

# Only apply rolling to numeric columns
df_rolling = df[rolling_goals].rolling(window, min_periods=1).mean()

# Reattach Date column
df_rolling['Date'] = df['Date'].values

# --- Plot ---
plt.figure(figsize=(12,6))

for col in rolling_goals:
    plt.plot(df_rolling['Date'], df_rolling[col],
             marker='o', label=f'{col} (rolling avg)')


plt.xticks(rotation=45)
plt.ylabel('Goals')
plt.title(f'Rolling Average ({window}-match) Goal Trends')
plt.legend()
plt.tight_layout()
plt.show()

rolling_xG = ['xG For','xG Against']

# Only apply rolling to numeric columns
df_rolling = df[rolling_xG].rolling(window, min_periods=1).mean()

# Reattach Date column
df_rolling['Date'] = df['Date'].values

# --- Plot ---
plt.figure(figsize=(12,6))

for col in rolling_xG:
    plt.plot(df_rolling['Date'], df_rolling[col],
             marker='o', label=f'{col} (rolling avg)')


plt.xticks(rotation=45)
plt.ylabel('Goals')
plt.title(f'Rolling Average ({window}-match) xG Trends')
plt.legend()
plt.tight_layout()
plt.show()







# ============================================================================
# WIN AND LOSS CORRELATION
# ============================================================================

# Encode result numerically for correlation
# Win = 1, Draw = 0, Loss = -1
df['Result_num'] = df['Result'].map({'W': 1, 'D': 0, 'L': -1})

# Keep only numeric columns to avoid errors
numeric_df = df.select_dtypes(include=['float64', 'int64'])

# Compute correlations
corrs = numeric_df.corrwith(df['Result_num']).sort_values(ascending=False)

# Top 20 stats most positively correlated with *winning*
top20_win = corrs.head(20)

# Top 20 stats most negatively correlated with *winning* (i.e., losing)
top20_loss = corrs.tail(30)

print("\n===== TOP 20 STATS CORRELATED WITH WINS =====\n")
print(top20_win)

print("\n===== TOP 20 STATS CORRELATED WITH LOSSES =====\n")
print(top20_loss)









# ============================================================================
# GOALKEEPING KICKS FOR QUERY
# ============================================================================
goalkeeping_kicks_for_query = """
SELECT
    Team,
    Date,
    Result,
    For_gk_passes_launched,
    For_gk_pct_goal_kicks_launched,
    For_gk_goal_kicks,
    For_gk_passes_completed_launched,
    For_gk_goal_kick_length_avg
FROM league_stats_matchlogs
ORDER BY Date
"""

goalkeeping_kicks_for = pd.read_sql_query(goalkeeping_kicks_for_query, conn)

# Convert Date
goalkeeping_kicks_for["Date"] = pd.to_datetime(goalkeeping_kicks_for["Date"])

# ---- STATIC MATPLOTLIB PLOT ---- #
plt.figure(figsize=(14, 6))

plt.plot(goalkeeping_kicks_for["Date"], goalkeeping_kicks_for["For_gk_passes_launched"], marker='o', label="GK Passes Launched")

plt.plot(goalkeeping_kicks_for["Date"], goalkeeping_kicks_for["For_gk_pct_goal_kicks_launched"], marker='o', label="GK Kicks Launched %")

plt.plot(goalkeeping_kicks_for["Date"], goalkeeping_kicks_for["For_gk_goal_kicks"], marker='o', label="GK Kicks")

plt.plot(goalkeeping_kicks_for["Date"], goalkeeping_kicks_for["For_gk_passes_completed_launched"], marker='o', label="GK Launches Completed")

plt.plot(goalkeeping_kicks_for["Date"], goalkeeping_kicks_for["For_gk_goal_kick_length_avg"], marker='o', label="GK Kick Avg Length")

# Annotate Result + Opponent
metrics = [
    "For_gk_passes_launched",
    "For_gk_pct_goal_kicks_launched",
    "For_gk_goal_kick_length_avg"
]

for metric in metrics:
    for _, row in goalkeeping_kicks_for.iterrows():
        plt.annotate(
            row["Result"],
            (row["Date"], row[metric]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=10,
            alpha=0.6
        )

plt.title("GK Passes")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()



# ============================================================================
# GOALKEEPING QUERY
# ============================================================================
goalkeeping_query = """
SELECT
    Team,
    Date,
    Result,
    For_gk_psxg_net,
    For_gk_clean_sheets
FROM league_stats_matchlogs
ORDER BY Date
"""

goalkeeping = pd.read_sql_query(goalkeeping_query, conn)

# Convert Date
goalkeeping["Date"] = pd.to_datetime(goalkeeping["Date"])

# ---- STATIC MATPLOTLIB PLOT ---- #
plt.figure(figsize=(14, 6))

plt.plot(goalkeeping["Date"], goalkeeping["For_gk_psxg_net"], marker='o', label="Net PSxG")

plt.plot(goalkeeping["Date"], goalkeeping["For_gk_clean_sheets"], marker='o', label="Clean Sheets")


# Annotate Result + Opponent
metrics = [
    "For_gk_psxg_net",
    "For_gk_clean_sheets"
]

for metric in metrics:
    for _, row in goalkeeping.iterrows():
        plt.annotate(
            row["Result"],
            (row["Date"], row[metric]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=10,
            alpha=0.6
        )

plt.title("Goalkeeping")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()


# ============================================================================
# SAVE % QUERY
# ============================================================================
save_pct_query = """
SELECT
    Team,
    Date,
    Result,
    For_gk_save_pct
FROM league_stats_matchlogs
ORDER BY Date
"""

save_pct = pd.read_sql_query(save_pct_query, conn)

# Convert Date
save_pct["Date"] = pd.to_datetime(save_pct["Date"])

# ---- STATIC MATPLOTLIB PLOT ---- #
plt.figure(figsize=(14, 6))

plt.plot(save_pct["Date"], save_pct["For_gk_save_pct"], marker='o', label="Save %")



# Annotate Result + Opponent
metrics = [
    "For_gk_save_pct"
]

for metric in metrics:
    for _, row in save_pct.iterrows():
        plt.annotate(
            row["Result"],
            (row["Date"], row[metric]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=10,
            alpha=0.6
        )

plt.title("Save %")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()



# ============================================================================
# TACKLES AGAINST QUERY
# ============================================================================
tackles_against_query = """
SELECT
    Team,
    Date,
    Result,
    Against_tackles_won_y,
    Against_tackles,
    Against_tackles_def_3rd,
    Against_tackles_interceptions
FROM league_stats_matchlogs
ORDER BY Date
"""

tackles_against = pd.read_sql_query(tackles_against_query, conn)

# Convert Date
tackles_against["Date"] = pd.to_datetime(tackles_against["Date"])

# ---- STATIC MATPLOTLIB PLOT ---- #
plt.figure(figsize=(14, 6))

plt.plot(tackles_against["Date"], tackles_against["Against_tackles_won_y"], marker='o', label="Tackles Against Won")

plt.plot(tackles_against["Date"], tackles_against["Against_tackles"], marker='o', label="Tackles Against")

plt.plot(tackles_against["Date"], tackles_against["Against_tackles_def_3rd"], marker='o', label="Tackles Against Defensive Third")

plt.plot(tackles_against["Date"], tackles_against["Against_tackles_interceptions"], marker='o', label="Interceptions Against")


# Annotate Result + Opponent
metrics = [
    "Against_tackles_won_y",
    "Against_tackles",
    "Against_tackles_def_3rd",
    "Against_tackles_interceptions"
]

for metric in metrics:
    for _, row in tackles_against.iterrows():
        plt.annotate(
            row["Result"],
            (row["Date"], row[metric]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=10,
            alpha=0.6
        )

plt.title("Tackles Against")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()



# ============================================================================
# GOAL CREATION QUERY
# ============================================================================
goal_creation_query = """
SELECT
    Team,
    Date,
    Result,
    For_gca_shots,
    For_goals_per_shot,
    "Goals For"
FROM league_stats_matchlogs
ORDER BY Date
"""

goal_creation = pd.read_sql_query(goal_creation_query, conn)

# Convert Date
goal_creation["Date"] = pd.to_datetime(goal_creation["Date"])

# ---- STATIC MATPLOTLIB PLOT ---- #
plt.figure(figsize=(14, 6))

plt.plot(goal_creation["Date"], goal_creation["For_gca_shots"], marker='o', label="GCA Shots")

plt.plot(goal_creation["Date"], goal_creation["For_goals_per_shot"], marker='o', label="Goals per Shot")

plt.plot(goal_creation["Date"], goal_creation["Goals For"], marker='o', label="Goals For")


# Annotate Result + Opponent
metrics = [
    "For_gca_shots",
    "For_goals_per_shot",
    "Goals For"
]

for metric in metrics:
    for _, row in goal_creation.iterrows():
        plt.annotate(
            row["Result"],
            (row["Date"], row[metric]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=10,
            alpha=0.6
        )

plt.title("Goal Creation")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()



# ============================================================================
# TOUCHES IN DEF PEN AREA QUERY
# ============================================================================
touches_in_def_pen_query = """
SELECT
    Team,
    Date,
    Result,
    For_touches_def_pen_area
FROM league_stats_matchlogs
ORDER BY Date
"""

touches_in_def_pen = pd.read_sql_query(touches_in_def_pen_query, conn)

# Convert Date
touches_in_def_pen["Date"] = pd.to_datetime(touches_in_def_pen["Date"])

# ---- STATIC MATPLOTLIB PLOT ---- #
plt.figure(figsize=(14, 6))

plt.plot(touches_in_def_pen["Date"], touches_in_def_pen["For_touches_def_pen_area"], marker='o')



# Annotate Result + Opponent
metrics = [
    "For_touches_def_pen_area"
]

for metric in metrics:
    for _, row in touches_in_def_pen.iterrows():
        plt.annotate(
            row["Result"],
            (row["Date"], row[metric]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=10,
            alpha=0.6
        )

plt.title("Touches in Defensive Penalty Area")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()















