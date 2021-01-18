"""
Get comments which contain stock tickers from specified subreddits.
"""

import os

import praw
import datetime as dt
import pandas as pd
import numpy as np
from get_all_tickers import get_tickers as gt
import re

from praw.models import Comment

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

    stockRegex = re.compile(r"[A-Z]{2,4}[,.\s]")

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

if __name__ == "__main__":

    reddit = praw.Reddit(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        user_agent="Stock Sentiment Analysis",
        password=os.environ["REDDIT_PASSWORD"],
    )

    # Set Up
    today = dt.datetime.today()
    subreddits = ["wallstreetbets", "stocks", "pennystocks", "investing"]

    for subreddit in subreddits:
        print(f"Retrieving subreddit {subreddit}")
        df = get_ticker_comments(subreddit, reddit, time_period="hour")

        df.to_csv(f"{subreddit}_comments.csv", index=False)
