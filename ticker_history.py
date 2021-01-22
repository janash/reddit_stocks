"""
adds the %change and end-of-day price to the sentiment DataFrame

Parameters
----------
df : pd.DataFrame
    DataFrame which contains the ticker, average sentiment, and mentions from a specific subreddit

Returns
-------
df_comment_sentiment : pd.DataFrame
    A dataframe with %change and EOD price to sentiment DataFrame
"""
import os


import pandas as pd
import datetime as dt
import yfinance as yf


today = dt.date.today()
yesterday = today - dt.timedelta(days = 1) 
to_analyze = ["wallstreetbets", "pennystocks", "stocks", "overall", "investing"]
mentioned_tickers = []

for subreddit in to_analyze:
    filename = f'{today}_{subreddit}.csv'
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        tickers = df['ticker'].tolist()
        for ticker in tickers:
            if ticker not in mentioned_tickers:
                mentioned_tickers.append(ticker)
   
stock_df = pd.DataFrame()
final_df = pd.DataFrame()

for ticker in mentioned_tickers:
    tick = yf.Ticker(ticker)
    tickdf = tick.history('1d')
    tickdf = tickdf.reset_index()
    tickdf['ticker'] = ticker
    tickdf = tickdf.groupby("ticker").mean()
    stock_df = stock_df.append(tickdf)

final_df['ticker'] = mentioned_tickers
final_df['open'] = stock_df['Open'].values
final_df['close'] = stock_df['Close'].values
final_df["percent change"] = 100*((final_df['close']-final_df['open'])/final_df['open'])        
final_df.to_csv(f"{today}_stock-info.csv")
