#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 11:49:39 2025

@author: benharris
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
import plotly.express as px


df = pd.read_csv('all_squad_stats_matchlogs_24-25_Championship.csv')

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
















