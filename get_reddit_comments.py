"""
Get comments which contain stock tickers from specified subreddits.
"""

import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import praw
import datetime as dt
import pandas as pd
import numpy as np
from get_all_tickers import get_tickers as gt
import re
import yfinance as yf
from praw.models import Comment

nltk.download("vader_lexicon")
nltk.download("stopwords")



# Get subreddit comments. Filter for tickers
def get_ticker_comments(subreddit_name, reddit, time_period="day"):
    """
    Get comments from the specified subreddit which contain tickers.

    Parameters
    ----------
    subreddit_name : str
        The name of the subreddit for which to retrieve comments
    reddit : praw object
        A praw object
    time_period : str, optiona;
        The time period to retrieve comments for

    Returns
    -------
    ticker_comments : pd.DataFrame
        A dataframe of the comments which contain tickers.
    """

    all_stocks = gt.get_tickers()

    stockRegex = re.compile(r"[A-Z]{2,4}[,./\s]")

    comment_dictionary = {"ticker": [], "comment": []}
    for submission in reddit.subreddit(subreddit_name).top(time_period):
        submission_comments = submission.comments.list()

        for comment in submission_comments:
            if isinstance(comment, Comment):
                comment_body = comment.body
                comment_body += " "
                tickers_in_comment = stockRegex.findall(comment_body)

                if tickers_in_comment:
                    unique_set = np.unique(tickers_in_comment)

                    # This gets the punctuation off the stock ticker
                    unique_set = [x[:-1] for x in unique_set]

                    # This gets elements which are in both lists.
                    true_stocks = np.intersect1d(unique_set, all_stocks)

                    for stock in true_stocks:
                        comment_dictionary["ticker"].append(stock)
                        comment_dictionary["comment"].append(comment_body[:-1])

    df = pd.DataFrame.from_dict(comment_dictionary)

    return df


# Perform sentiment analysis on comments
def get_comment_sentiment(df):
    """
    Analyze the  sentiment of each ticker in a comment.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame which contains the ticker and comment from a specific subreddit

    Returns
    -------
    df_comment_sentiment : pd.DataFrame
        A dataframe of the comments which contain tickers and the sentiment of the comment.
    """
    sia = SIA()
    sentiment_df = df["comment"].apply(sia.polarity_scores)
    sentiment_df = pd.json_normalize(sentiment_df.to_numpy())
    df_concat = pd.concat([df, sentiment_df], axis=1)

    return df_concat


# perform an average on the comment sentiment
def get_mean_ticker_sentiment(df):
    """
    Translates sentiment dataframe into averages of pos, neg, neu, and compound sentiment

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame which contains the ticker, comment, sentiment from a specific subreddit

    Returns
    -------
    df_comment_sentiment : pd.DataFrame
        A dataframe of the average ticker sentiments
    """
    df["mentions"] = df.groupby("ticker")["ticker"].transform("count")
    df_sentiment_stocks = df.groupby("ticker").mean()

    return df_sentiment_stocks

def add_stock_information(df, today, yesterday):
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
    #date_time = dt.datetime.today()
    df = df.reset_index()
    tickers = df['ticker'].tolist()
    stock_df = pd.DataFrame()
    for ticker in tickers:
        tick = yf.Ticker(ticker)
        tickdf = tick.history('1d')
        tickdf = tickdf.reset_index()
        tickdf['ticker'] = ticker
        tickdf = tickdf.groupby("ticker").mean()
        stock_df = stock_df.append(tickdf)
    print(stock_df)
    df['date'] = yesterday
    df['open'] = stock_df['Open'].values
    df['close'] = stock_df['Close'].values
    df["percent change"] = 100*((df['close']-df['open'])/df['open'])

    return df

if __name__ == "__main__":

    reddit = praw.Reddit(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        user_agent="Stock Sentiment Analysis",
        password=os.environ["REDDIT_PASSWORD"],
    )

    # Set Up
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=1)
    subreddits = ["wallstreetbets", "stocks", "pennystocks", "investing", "robinhood", "robinhoodpennystocks"]

    for subreddit in subreddits:
        print(f"Retrieving subreddit {subreddit}")
        df = get_ticker_comments(subreddit, reddit, time_period="day")
        sentiment_df = get_comment_sentiment(df)
        sentiment_df.to_csv(f"{today}_{subreddit}_comments.csv")
        average_df = get_mean_ticker_sentiment(sentiment_df)
        average_df.to_csv(f"{today}_{subreddit}.csv")
        # stock_price_df = add_stock_information(average_df, today, yesterday)
        # stock_price_df.to_csv(f"{today}_{subreddit}_priceinfo.csv")
