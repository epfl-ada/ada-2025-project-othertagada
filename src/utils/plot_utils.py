import plotly.graph_objects as go
import networkx as nx
import plotly.io as pio
from src.data.some_dataloader import RedditDataset
import numpy as np
import matplotlib.pyplot as plt

def plot_mean_sentiment_per_month(data):

    monthly_mean = data.groupby('year_month')['LINK_SENTIMENT'].mean()

    monthly_mean.plot(kind='bar')
    plt.ylim(0.75, 0.85)
    plt.title('Mean sentiment per Month')
    plt.xlabel('date')
    plt.ylabel('Mean Sentiment')
    plt.tight_layout()
    plt.show()

def plot_sorted_subreddits(sorted_subreddits,n, direction, title ):
    """ Plots Top/bottom n subreddits from sorted df 

    Args:
        sorted_subreddits (df): sorted df of subreddits
        n (int): number of subreddits to plot
        direction (str): 'SOURCE_SUBREDDIT' for outgoing links or 'TARGET_SUBREDDITS' for incomming links
        title (str): Title of plot
    """

    if (direction != 'SOURCE_SUBREDDIT') and (direction != 'TARGET_SUBREDDIT'):
        raise ValueError('Direction should be SOURCE_SUBREDDIT or TARGET_SUBREDDIT')

    n_sorted_subreddits = sorted_subreddits.head(n).set_index(direction)
    n_sorted_subreddits['avg_sentiment'].plot(kind='bar', figsize=(12,6))
    plt.title(title)
    plt.xlabel(direction)
    plt.ylabel('Average Sentiment')
    plt.tight_layout()
    plt.show()