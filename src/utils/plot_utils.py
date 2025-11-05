import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from src.utils.data_utils import *
import seaborn as sns

def plot_distribution_nb_appearance_subreddits(data):
    """ Plots the distribution of the number of appearances of source and target subreddits

    Args:
        data (df): dataframe to plot
    """
     
    # Counts number of appearances for each subreddit
    source_counts = data['SOURCE_SUBREDDIT'].value_counts()
    target_counts = data['TARGET_SUBREDDIT'].value_counts()

    plt.figure(figsize=(10, 6))
    plt.hist(source_counts, bins=10000, alpha=0.6, label="Source subreddits")
    plt.hist(target_counts, bins=10000, alpha=0.6, label="Target subreddits")
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Distribution of Subreddit Appearances")
    plt.xlabel("Number of appearances")
    plt.ylabel("Number of subreddits")
    plt.legend()
    plt.show()


def plot_mean_sentiment_per_month(data):
    """ Plots a bar plot of the mean sentiment link per month

    Args:
        data (df): dataframe to plot
    """
    data = get_df_time_window(data, '2015-01-01', '2017-05-01') # select full months
    print('hello in plot mean per month')
    data['year_month'] = data['TIMESTAMP'].dt.to_period('M').astype(str)
    monthly_mean = data.groupby('year_month')['LINK_SENTIMENT'].mean()

    plot_bar_chart(monthly_mean, 
                   title='Mean sentiment per Month', 
                   xlabel='date', 
                   ylabel='Mean Sentiment', 
                   ylim=(0.75, 0.85)
                  )

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
    plot_bar_chart(n_sorted_subreddits, title=title, xlabel=direction, ylabel='Average Sentiment')

def plot_subreddit_graph(G: nx.DiGraph, title: str, edge_scale: int = 100):
    """
    Plot a subreddit interaction subgraph.
    
    Parameters
    ----------
    G : networkx.DiGraph
        Graph to plot.
    title : str
        Plot title.
    edge_scale : int
        Divides edge weights to adjust thickness.
    """
    # === Plot ===
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    nx.draw(
        G, pos,
        with_labels=True,
        node_size=1200,
        node_color="lightgreen",
        font_size=10,
        font_weight="bold",
        arrowsize=15
    )
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[w/100 for w in weights])
    plt.title(title)
    plt.show()

# Visualize average sentiment per cluster with standard deviation
def plot_average_sentiment_per_cluster(features) :
    """
    Visualize the average sentiment of subreddits within each cluster.

    Parameters
    ----------
    features : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - 'cluster': numeric or categorical cluster labels (e.g., from KMeans)
        - 'mean_sentiment': average sentiment score per subreddit
          (e.g., mean of LINK_SENTIMENT values for that subreddit)
    """

    plt.figure(figsize=(8,5))
    sns.barplot(data=features, x='cluster', y='mean_sentiment', ci='sd', palette='viridis')
    plt.title('Average subreddit sentiment per cluster')
    plt.show()


def plot_bar_chart(data, title, xlabel, ylabel, ylim=None, xlim=None):
    """
    Plots a bar chart.

    Args:
        data (pd.DataFrame): DataFrame containing 'x' and 'y' columns
        title (str): title of the plot
        xlabel (str): label of the x axis
        ylabel (str): label of the y axis
        ylim (tuple, optional): y-axis limits
        xlim (tuple, optional): x-axis limits
    """
    data.plot(kind='bar', figsize=(10,6))
    plt.ylim(ylim) if ylim else None
    plt.xlim(xlim) if xlim else None
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()