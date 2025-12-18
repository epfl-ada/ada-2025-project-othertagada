from datetime import datetime
import pandas as pd
import networkx as nx

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


def get_df_time_window(df, from_date, to_date):
    """ Get dataframe of rows for which TIMESTAMP is in time window [from_date, to_date)

    Args:
        df (df): dataframe containing 'TIMESTAMP'
        from_date (str): 'YYYY-MM-DD' Start date included
        to_date (str): 'YYYY-MM-DD' End date excluded

    Returns:
        window_df (df): dataframe with only the rows over time window given
    """

    for date in (from_date, to_date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: '{date}'. Expected 'YYYY-MM-DD'.")

    window_df = df[(df['TIMESTAMP'] >= from_date) & (df['TIMESTAMP'] < to_date)]
    return window_df


def compute_core_subgraph(dataframe: pd.DataFrame, k: int = 10):
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

    # === Build weighted directed graph ===
    edges = (
        dataframe.groupby(["SOURCE_SUBREDDIT", "TARGET_SUBREDDIT"])
        .size()
        .reset_index(name="weight")
    )
    G_full = nx.from_pandas_edgelist(
        edges, "SOURCE_SUBREDDIT", "TARGET_SUBREDDIT", edge_attr="weight", create_using=nx.DiGraph()
    )

    # === Convert to undirected for core analysis ===
    G_undirected = G_full.to_undirected()

    # === Compute core numbers ===
    core_numbers = nx.core_number(G_undirected)
    core_sorted = sorted(core_numbers.items(), key=lambda x: x[1], reverse=True)
    top_subs = [node for node, core in core_sorted[:k]]

    # === Extract subgraph of top subreddits ===
    G_core = G_full.subgraph(top_subs)

    print(f"Top {k} subreddits by graph core density:")
    print(top_subs)
    print(f"Nodes: {G_core.number_of_nodes()}, Edges: {G_core.number_of_edges()}")

    return G_core

def extract_graph_features(G):
    """
    Compute graph-based structural features for each node (subreddit).

    Parameters
    ----------
    G : networkx.Graph or networkx.DiGraph
        The graph representing subreddit interactions (edges may carry sentiment).
        
    Returns
    -------
    features : pandas.DataFrame
        A DataFrame containing one row per node and columns:
        ['subreddit', 'degree', 'in_degree', 'out_degree',
         'clustering', 'pagerank', 'betweenness', 'closeness']
    """


    # Precompute metrics only once
    pagerank_dict = nx.pagerank(G)
    clustering_dict = nx.clustering(G.to_undirected())
    betweenness_centrality_dict = nx.betweenness_centrality(G)
    closeness_centrality_dict = nx.closeness_centrality(G)

    # Build features efficiently
    features = pd.DataFrame({
        'subreddit': list(G.nodes()),
        'degree': [G.degree(n) for n in G.nodes()],
        'in_degree': [G.in_degree(n) for n in G.nodes()],
        'out_degree': [G.out_degree(n) for n in G.nodes()],
        'clustering': [clustering_dict[n] for n in G.nodes()],
        'pagerank': [pagerank_dict[n] for n in G.nodes()],
        'betweenness': [betweenness_centrality_dict[n] for n in G.nodes()],
        'closeness': [closeness_centrality_dict[n] for n in G.nodes()],
    })

    return features


def top_connected(df, subreddit, n=10):
    #links from
    from_counts = (
        df[df['SOURCE_SUBREDDIT'] == subreddit]
        .groupby('TARGET_SUBREDDIT')
        .size()
        .rename('from_count')
    )

    #links to
    to_counts = (
        df[df['TARGET_SUBREDDIT'] == subreddit]
        .groupby('SOURCE_SUBREDDIT')
        .size()
        .rename('to_count')
    )

    merged = pd.concat([from_counts, to_counts], axis=1).fillna(0)
    merged['total'] = merged['from_count'] + merged['to_count']


    return merged.sort_values('total', ascending=False).head(n)    #to sort by total interaction

def get_large_and_restricted_df(hl_data, gamergate_subs) :

    hl_data["source"] = hl_data["SOURCE_SUBREDDIT"].str.lower()
    hl_data["target"] = hl_data["TARGET_SUBREDDIT"].str.lower()

    hl_data['timestamp'] = pd.to_datetime(hl_data['TIMESTAMP'], unit='s')  # dataset timestamps are unix secs

    # weekly aggregation for the df
    hl_data['week'] = hl_data['TIMESTAMP'].dt.to_period('W').apply(lambda r: r.start_time)

    # large data = TARGET or SOURCE part of gamergate_list
    large_gamergate_df = hl_data[(hl_data["source"].isin(gamergate_subs)) | (hl_data["target"].isin(gamergate_subs))].copy()

    # restricted data = TARGET & SOURCE part of gamergate_list
    restricted_gamergate_df = hl_data[(hl_data["source"].isin(gamergate_subs)) & (hl_data["target"].isin(gamergate_subs))].copy()

    return large_gamergate_df, restricted_gamergate_df