import plotly.graph_objects as go
import networkx as nx
import plotly.io as pio

def write_html_spring_graph_n_nodes(data, avg_df, n):
    """ Create a networkX graph of the dataframe ... COMPLETE DESCRIPTION!!!!!!!

    Args:
        data (df): reddit dataframe
        avg_df (df): dataframe of source subreddits and average outgoing link sentiment
        n (int): number of top source subreddit to get from avg_df for plotting graph
    """

    n_avg_df = avg_df.head(n)

    # dict lookup for hover (still need to fix for target nodes...)
    avg_sent_dict = dict(zip(n_avg_df["SOURCE_SUBREDDIT"], n_avg_df["avg_sentiment"]))

    newdf = data[data['SOURCE_SUBREDDIT'].isin(n_avg_df['SOURCE_SUBREDDIT'].to_list())]

    # Build NetworkX graph
    G = nx.from_pandas_edgelist(
        newdf,
        source="SOURCE_SUBREDDIT",
        target="TARGET_SUBREDDIT",
        edge_attr="LINK_SENTIMENT"
    )

    # Position nodes using spring layout (layout is bad for more than 2 nodes though)
    pos = nx.spring_layout(G, k=0.3, iterations=80, seed=42)

    # Extract edge coordinates
    edge_x = []
    edge_y = []
    edge_colors = []

    for src, tgt, data in G.edges(data=True):
        x0, y0 = pos[src]
        x1, y1 = pos[tgt]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

        sentiment = data["LINK_SENTIMENT"]
        edge_colors.append("green" if sentiment > 0 else "red")

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color="lightgray"),
        mode="lines",
        hoverinfo="none"
    )

    # NEED TO ADD COLOR OF EDGES DEPENDING ON NEG OR POS VALUE

    # Node coordinates & colors
    node_x = []
    node_y = []
    node_colors = []
    node_hover = []

    source_nodes = set(newdf["SOURCE_SUBREDDIT"])
    target_nodes = set(newdf["TARGET_SUBREDDIT"])

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        if node in source_nodes:
            node_colors.append("dodgerblue")
        elif node in target_nodes:
            node_colors.append("orange")
        else:
            node_colors.append("gray")

        # hoover tool
        avg_val = avg_sent_dict.get(node, None)
        if avg_val is None:
            hover_text = f"<b>{node}</b><br>Avg sentiment: N/A"
        else:
            hover_text = f"<b>{node}</b><br>Avg sentiment: {avg_val:.3f}"

        node_hover.append(hover_text)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        textposition="top center",
        hovertemplate="%{hovertext}<extra></extra>",
        hovertext=node_hover,
        marker=dict(
            size=12,
            color=node_colors,
            line=dict(width=1)
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        title="Interactive Subreddit Network (Plotly)",
        title_font_size=18,
        showlegend=False,
        hovermode="closest",
        width=900, height=700,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    pio.write_html(fig, file="reddit_network_plotly.html", auto_open=True)

def mean_sentiment_per_subreddit_in_graph(G, df, features):
    """
    Compute the mean sentiment of each subreddit in the graph G and the variance of these 
    mean sentiment scores within each cluster.
    Add 'mean_sentiment' and 'sentiment_variance' columns to the features.

    Parameters
    ----------
    G : networkx.Graph or networkx.DiGraph
        The subreddit interaction graph. Only subreddits (nodes) present 
        in this graph are considered when computing sentiment averages.

    df : pandas.DataFrame
        The full dataset of subreddit interactions.

    features : pandas.DataFrame
        A DataFrame containing per-subreddit graph features and cluster 
        assignments. 

    Returns
    -------
    features : pandas.DataFrame
        The input `features` DataFrame enriched with new 'mean_sentiment' and 'sentiment_variance'
        columns.
    cluster_variance : pandas.DataFrame
        A separate DataFrame summarizing the variance of mean sentiment per cluster.
    """

    valid_subreddits = set(G.nodes())

    mean_sentiment = (
        df[df['SOURCE_SUBREDDIT'].isin(valid_subreddits)]
        .groupby('SOURCE_SUBREDDIT')['LINK_SENTIMENT']
        .mean()
    )


    # Convert to DataFrame and merge
    sentiment_df = mean_sentiment.reset_index()
    sentiment_df.columns = ['subreddit', 'mean_sentiment']

    # Merge into features
    features = features.merge(sentiment_df, on='subreddit', how='left')

    # --- Variance of sentiment within each cluster ---
    cluster_variance = features.groupby('cluster')['mean_sentiment'].var().reset_index()
    cluster_variance.columns = ['cluster', 'sentiment_variance']

    ### ###
    print("Variance of mean sentiment within each cluster:")
    print(cluster_variance)

    # Add cluster variance to features if useful
    features = features.merge(cluster_variance, on='cluster', how='left')

    return features, cluster_variance
