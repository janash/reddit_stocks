"""
Create "overall" data as a weighted average from all subreddits
"""

import datetime as dt

import os

import pandas as pd

today = dt.date.today()

subreddits = ["wallstreetbets", "stocks", "pennystocks", "investing", "robinhood", "robinhoodpennystocks"]

df = pd.DataFrame()

for subreddit in subreddits:

    filename = f"{today}_{subreddit}.csv"

    if os.path.exists(filename):

        subreddit_df = pd.read_csv(filename)

        df = pd.concat([df, subreddit_df], axis=0)
    
    else:
        subreddits.remove(subreddit)

overall_df = pd.DataFrame()
tickers = []
weighted_averages = []
total_mentions = []

for ticker, data in df.groupby("ticker"):
    weighted_avg = 0
    num_mentions = 0

    for name, row in data.iterrows():
        weighted_avg += row["compound"] * row["mentions"]
        num_mentions += row["mentions"]

    weighted_averages.append(weighted_avg / num_mentions)
    tickers.append(ticker)
    total_mentions.append(num_mentions)

overall_df["ticker"] = tickers
overall_df["compound"] = weighted_averages
overall_df["mentions"] = total_mentions

overall_df.to_csv(f"{today}_overall.csv", index=False)
