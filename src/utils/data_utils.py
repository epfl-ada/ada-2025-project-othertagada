import plotly.graph_objects as go
import networkx as nx
import plotly.io as pio
from src.data.some_dataloader import RedditDataset
import numpy as np
import matplotlib.pyplot as plt

def get_sorted_subreddits_by_avg_sentiment(data, direction, min_count=500, ascending=True):
    """Sorts the subreddits by average sentiment of outgoing or incomming links

    Args:
        data (df): dataframe to sort
        direction (str): 'SOURCE_SUBREDDIT' for outgoing links or 'TARGET_SUBREDDIT' for incomming links
        min_count (int): min number of apparition of subreddit in df to be included in the sorting
            (default is 500)
        ascending (bool): if True in ascending order, if False in descending order
            (default is True)

    Returns:
        avg_sentiment_by_subreddit (df): sorted subreddits with average link sentiment
    """
    
    if (direction != 'SOURCE_SUBREDDIT') and (direction != 'TARGET_SUBREDDIT'):
        raise ValueError('Direction should be SOURCE_SUBREDDIT or TARGET_SUBREDDIT')

    # Only include subreddits with more than min_count entries
    counts = data[direction].value_counts()
    popular_subs = counts[counts > min_count].index
    print(f'Using {len(popular_subs)} subreddits (>{min_count} posts)')

    # Compute average sentiment only for popular subreddits
    avg_sentiment_by_subreddit = (
        data[data[direction].isin(popular_subs)]
        .groupby(direction)['LINK_SENTIMENT']
        .mean().sort_values(ascending=ascending) 
    )

    return avg_sentiment_by_subreddit.reset_index().rename(columns={'LINK_SENTIMENT': 'avg_sentiment'})

