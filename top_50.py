"""
Create new dataframes with info for each subreddit. Only top 100 stocks by number of mentions
"""

import os

import pandas as pd
import datetime as dt

today = dt.date.today()

to_analyze = ["wallstreetbets", "pennystocks", "stocks", "overall", "investing"]

for subreddit in to_analyze:
    print(subreddit)
    filename = f"{today}_{subreddit}.csv"

    if os.path.exists(filename):
        df = pd.read_csv(f"{today}_{subreddit}.csv")

        df.sort_values(by="mentions", inplace=True, ascending=False)

        df.set_index("ticker", inplace=True)

        df.drop("DD", axis=0, inplace=True, errors="ignore")

        selected = df[["compound", "mentions"]]

        pretty_names = ["Average Sentiment", "Total Number of Mentions"]

        top_50 = selected.iloc[:50, :]

        top_50.columns = pretty_names
        top_50.index.name = "Ticker"

        top_50.to_csv(f"{subreddit}_top50.csv")
