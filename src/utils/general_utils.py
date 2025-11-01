import plotly.graph_objects as go
import networkx as nx
import plotly.io as pio
from src.data.some_dataloader import RedditDataset
import numpy as np
import matplotlib.pyplot as plt

def write_html_spring_graph_n_nodes(data, avg_df, n):

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

        # >>> ADDED: build hover tooltip with avg sentiment
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
        hovertemplate="%{hovertext}<extra></extra>",  # >>> ADDED
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
