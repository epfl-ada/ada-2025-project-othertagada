import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import networkx as nx
import numpy as np
from src.utils.data_utils import *
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, display
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objects import Figure, Table
from matplotlib.ticker import PercentFormatter

def plot_jaccard_similarity_user_heatmap(post_data):

    def jaccard_similarity(list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        return len(s1.intersection(s2)) / len(s1.union(s2))
    
    subreddit_users = post_data.groupby("SUBREDDIT")["USERNAME"].apply(set)
    subreddits = subreddit_users.index
    n = len(subreddits)

    jaccard_matrix = np.zeros((n, n))

    for i, sub1 in enumerate(subreddits):
        for j, sub2 in enumerate(subreddits):
            jaccard_matrix[i, j] = jaccard_similarity(
                subreddit_users[sub1], 
                subreddit_users[sub2]
            )
    plt.figure(figsize=(7,6))

    jaccard_df = pd.DataFrame(jaccard_matrix, index=subreddits, columns=subreddits)

    sns.heatmap(
        jaccard_df,
        cmap="mako", 
        norm=LogNorm(vmin=jaccard_df.values.min() + 1e-5, vmax=jaccard_df.values.max()),  # Log scale
        annot=False,
        linewidths=0.5,
        linecolor='gray'
    )

    plt.title("Jaccard Similarity Between Subreddit User Sets")
    plt.tight_layout()
    #plt.savefig('outputs/graph/heatmap_users.png')
    plt.show()
    

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
    data = get_df_time_window(data, '2014-01-01', '2017-05-01') # select full months
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

def plot_subreddit_graph(G: nx.DiGraph, title: str, pos : dict = None, edge_scale: int = 100):
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
    plt.figure(figsize=(10, 8))
    
    # Use provided positions, or generate new ones if none given
    if pos is None:
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
    nx.draw_networkx_edges(G, pos, width=[w / edge_scale for w in weights])
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

def plot_cluster_sentiment_variance(cluster_variance):
    """
    Visualize the variance of mean sentiment within each subreddit cluster.

    Parameters
    ----------
    cluster_variance : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - 'cluster': numeric or categorical label representing a subreddit cluster
        - 'sentiment_variance': numerical value representing the variance of 
          mean sentiment within that cluster.

    """
    plt.figure(figsize=(8,5))
    sns.barplot(data=cluster_variance, x='cluster', y='sentiment_variance')
    plt.title('sentiment variance per subreddit cluster')
    plt.show()


def animate_subreddit_evolution(graphs, labels, pos, save_path="./outputs/subreddit_evolution.gif", interval=500, show_inline=True):
    """
    Animate subreddit interaction graphs over time (one frame per week).
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    def update(frame):
        ax.clear()
        G = graphs[frame]
        nx.draw(
            G, pos,
            with_labels=True,
            node_size=1200,
            node_color="lightgreen",
            font_size=10,
            font_weight="bold",
            arrowsize=15,
            ax=ax
        )
        weights = [G[u][v]['weight'] for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos, width=[w / 100 for w in weights], ax=ax)
        ax.set_title(f"Subreddit Interactions\n{labels[frame]}")
        ax.axis("off")

    ani = FuncAnimation(fig, update, frames=len(graphs), interval=interval, repeat=True)
    ani.save(save_path, writer="pillow", dpi=150)
    print(f"Saved animation to {save_path}")

    if show_inline:
        plt.close(fig)
        display(HTML(ani.to_jshtml()))
    return ani


def get_animation_weekly(G, window, data, year):
    core_subreddits = list(G.nodes())

    # Compute fixed positions once
    G_master = nx.DiGraph()
    G_master.add_nodes_from(core_subreddits)
    pos = nx.spring_layout(G_master, k=0.5, seed=42)

    graphs = []
    labels = []

    for i in range(len(window) - 1):
        start = window[i].strftime("%Y-%m-%d")
        end = window[i + 1].strftime("%Y-%m-%d")

        df_core = data[
            data["SOURCE_SUBREDDIT"].isin(core_subreddits)
            & data["TARGET_SUBREDDIT"].isin(core_subreddits)
        ]

        df_window = get_df_time_window(df_core, start, end)

        edges = (
            df_window.groupby(["SOURCE_SUBREDDIT", "TARGET_SUBREDDIT"])
            .size()
            .reset_index(name="weight")
        )

        G_week = nx.from_pandas_edgelist(
            edges,
            "SOURCE_SUBREDDIT",
            "TARGET_SUBREDDIT",
            ["weight"],
            create_using=nx.DiGraph()
        )

        graphs.append(G_week)
        labels.append(f"Week of {start}")


    animate_subreddit_evolution(graphs, labels, pos, save_path=f"./outputs/subreddit_{year}_weekly.gif", interval=400)


def plot_interactions(links_dataset, subreddit, n=50):

    top50 = top_connected(links_dataset, subreddit, n)

    top10 = top50.head(10)

    #aggregate the rest (ranks 11–50)
    others_total = top50.iloc[10:]['total'].sum()

    #labels and values
    labels = list(top10.index) + ['Others (rank 11–' + str(n) + ')']
    values = list(top10['total']) + [others_total]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0,
            sort=False,
            textinfo='label+percent',
            showlegend=False,
            textposition='outside'
        )
    )
    fig.show()

def plot_stacked_bar_chart(links_dataset, html_output=False):
    #count out links
    out_counts = (
        links_dataset
        .groupby(['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
        .size()
        .reset_index(name='count')
        .rename(columns={'SOURCE_SUBREDDIT': 'SUBREDDIT', 'TARGET_SUBREDDIT': 'OTHER'})
    )

    #count in links
    in_counts = (
        links_dataset
        .groupby(['TARGET_SUBREDDIT', 'SOURCE_SUBREDDIT'])
        .size()
        .reset_index(name='count')
        .rename(columns={'TARGET_SUBREDDIT': 'SUBREDDIT', 'SOURCE_SUBREDDIT': 'OTHER'})
    )

    def split_counts(df):
        kia   = df[df['OTHER'] == 'kotakuinaction'].groupby('SUBREDDIT')['count'].sum()
        ghazi = df[df['OTHER'] == 'gamerghazi'].groupby('SUBREDDIT')['count'].sum()
        other = df[~df['OTHER'].isin(['kotakuinaction', 'gamerghazi'])].groupby('SUBREDDIT')['count'].sum()
        return kia, ghazi, other


    out_kia, out_ghazi, out_other = split_counts(out_counts)
    in_kia,  in_ghazi,  in_other  = split_counts(in_counts)

    #list of subreddits
    subs = sorted(
        set(links_dataset['SOURCE_SUBREDDIT']) | set(links_dataset['TARGET_SUBREDDIT'])
    )

    #offset for the two bars per subreddit
    x_base = list(range(len(subs)))
    x_out  = [x - 0.2 for x in x_base]   # left bar
    x_in   = [x + 0.2 for x in x_base]   # right bar


    out_kia_y   = [out_kia.get(s, 0)   for s in subs]
    out_ghazi_y = [out_ghazi.get(s, 0) for s in subs]
    out_other_y = [out_other.get(s, 0) for s in subs]

    in_kia_y    = [in_kia.get(s, 0)    for s in subs]
    in_ghazi_y  = [in_ghazi.get(s, 0)  for s in subs]
    in_other_y  = [in_other.get(s, 0)  for s in subs]

    fig = go.Figure()
    #out
    fig.add_bar(x=x_out, y=out_kia_y,   name="OUT → KIA",   marker_color="red")
    fig.add_bar(x=x_out, y=out_ghazi_y, name="OUT → Ghazi", marker_color="blue")
    fig.add_bar(x=x_out, y=out_other_y, name="OUT → Other", marker_color="green", visible="legendonly")

    #in
    fig.add_bar(x=x_in, y=in_kia_y,   name="IN ← KIA",   marker_color="red",  opacity=0.8)
    fig.add_bar(x=x_in, y=in_ghazi_y, name="IN ← Ghazi", marker_color="blue", opacity=0.8)
    fig.add_bar(x=x_in, y=in_other_y, name="IN ← Other", marker_color="green", opacity=0.8, visible="legendonly")

    fig.update_layout(
        barmode="stack",
        xaxis=dict(
            tickmode="array",
            tickvals=x_base,
            ticktext=subs
        ),
        xaxis_title="Subreddit",
        yaxis_title="Number of links",
        title="Outgoing and incoming links per subreddit",
        xaxis_tickangle=-45,
    )

    fig.show()
    if html_output:
        fig.write_html("./docs/assets/stacked_bar_transition.html")



def plot_histogram_nbposts_per_user(post_data: pd.DataFrame, subs_of_interest):
    subreddits_posts_per_user = post_data.groupby(["SUBREDDIT", "USERNAME"]).size().reset_index(name="post_count")
    subreddit_sizes = (
        subreddits_posts_per_user
        .groupby("SUBREDDIT")
        .size()
        .rename("subreddit_size")
    )

    # Join back to original dataframe
    subreddits_posts_per_user = (
        subreddits_posts_per_user
        .join(subreddit_sizes, on="SUBREDDIT")
        .sort_values("subreddit_size", ascending=False)
    )
    sns.histplot(
        data=subreddits_posts_per_user[subreddits_posts_per_user["SUBREDDIT"].isin(subs_of_interest)],
        x = "post_count",
        hue = "SUBREDDIT",
        bins=100,
        log_scale=True,
        multiple="stack", # stack the different subredddits instead of overlaying them
        alpha=1,
    )
    plt.xlabel("Number of posts per user")
    plt.ylabel("Number of users")
    plt.title("Histogram of Posts per User")
    plt.yscale("log")
    plt.xscale("log")
    plt.show()

def plot_posts_percent_positive_by_posts_per_user(post_data: pd.DataFrame, hl_data: pd.DataFrame, subs_of_interest):
    merged_df = pd.merge(left=post_data, right=hl_data, how="inner", on="POST_ID").loc[lambda d: d["SUBREDDIT"].isin(subs_of_interest)]
    df_plot = merged_df.groupby(["LINK_SENTIMENT", "USERNAME"]).size().reset_index(name="post_count")

    fig, ax = plt.subplots(figsize=(8, 5))

    # Define bins
    bins = np.logspace(
        np.log10(max(1, df_plot["post_count"].min())),
        np.log10(df_plot["post_count"].max()),
        10
    )
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Stacked distribution histogram
    sns.histplot(
        data=df_plot.loc[df_plot.index.repeat(df_plot["post_count"])],
        x="post_count",
        hue="LINK_SENTIMENT",
        bins=bins,
        multiple="fill",
        stat="probability",
        alpha=0.8,
        ax=ax
    )

    ax.set_xscale("log")
    ax.set_xlabel("Posts per user (log scale)")
    ax.set_ylabel("Percent of posts")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))

    #  Compute confidence intervals
    df_plot["bin"] = np.digitize(df_plot["post_count"], bins)
    df_plot["bin"] = df_plot["bin"].clip(1, len(bin_centers))
    n_df = (
        df_plot
        .groupby("bin")["post_count"]
        .sum()
        .reset_index(name="n_posts")
    )

    k_df = (
        df_plot
        .groupby(["bin", "LINK_SENTIMENT"])["post_count"]
        .sum()
        .reset_index(name="k_posts")
    )

    ci_data = k_df.merge(n_df, on="bin", how="left")

    ci_data["p"] = ci_data["k_posts"] / ci_data["n_posts"]
    ci_data["ci"] = 1.96 * np.sqrt(
        ci_data["p"] * (1 - ci_data["p"]) / ci_data["n_posts"]
    )

    # Overlay CI bars
    sub_h = ci_data[ci_data["LINK_SENTIMENT"] == 1]

    xpos = bin_centers[sub_h["bin"].values - 1]

    ax.errorbar(
        xpos,
        sub_h["p"],
        yerr=sub_h["ci"],
        fmt="none",
        ecolor="black",
        capsize=2,
    )

    ax.set_xlim(1, df_plot["post_count"].max())

    plt.tight_layout()
    plt.show()


def plot_link_neg_frac(hl_data, large_gamergate_df):
    ## outgoing negativity comparision (by negative outgoing link fraction)

    ## whole dataset
    overall_mean = (hl_data["LINK_SENTIMENT"] == -1).mean()

    ## gamergate
    gamergate_mean = (large_gamergate_df["LINK_SENTIMENT"] == -1).mean()

    fig = go.Figure()

    fig.add_bar(
        x=["Whole Dataset", "Gamergate-related"],
        y=[overall_mean, gamergate_mean],
        marker_color=["gray", "crimson"]
    )

    fig.update_layout(
        title="Fraction of outgoing negative link : Whole Reddit vs Gamergate-related Subreddits",
        yaxis_title="Negative Link fraction",
        yaxis_tickformat=".0%",
        template="plotly_white"
    )

    fig.show()


def plot_link_neg_frac_per_subs(gamergate_df, gamergate_subs):

    gg_sub_neg_frac = (
        gamergate_df
        .groupby("source")["LINK_SENTIMENT"]
        .apply(lambda s: (s == -1).mean())
        .sort_values(ascending=False)
        .reset_index(name="neg_frac")
    )

    gg_sub_neg_frac = gg_sub_neg_frac[
        gg_sub_neg_frac["source"].isin(gamergate_subs)
    ]

    fig = go.Figure()

    fig.add_bar(
        x=gg_sub_neg_frac["source"],
        y=gg_sub_neg_frac["neg_frac"],
        marker_color=gg_sub_neg_frac["neg_frac"],
        marker_colorscale="Reds"
    )

    fig.update_layout(
        title="Fraction of Negative Links by Gamergate Subreddit",
        xaxis_title="Subreddit",
        yaxis_title="Fraction of negative links",
        yaxis_tickformat=".0%",
        template="plotly_white"
    )

    fig.show()

def inter_plot_pred_accuracy_per_subs(test_set, link_prediction, gamergate_subs, title, output_path) :
    
    test_set["link_prediction"] = (pd.Series(link_prediction, index=test_set.index).replace(0, -1))

    pred_acc_per_subreddit = test_set.groupby('source').apply(lambda x : (x['link_prediction'] == x['LINK_SENTIMENT']).mean())

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=list(gamergate_subs),
            y=pred_acc_per_subreddit[list(gamergate_subs)],
            text=[f"{a:.3f}" for a in pred_acc_per_subreddit[list(gamergate_subs)]],
            textposition="auto",
            name="Accuracy"
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Subreddit",
        yaxis_title="Accuracy",
        template="plotly_white",
    )

    fig.write_html(output_path)

    fig.show()

def plot_feature_coef_and_significance(log_reg, feature_columns, title, output_path):

    coef_df = pd.DataFrame({
        'Feature': feature_columns,
        'Coefficient': log_reg.params.values,
        'p_value': log_reg.pvalues.values
    })

    coef_df['Significant'] = coef_df['p_value'] < 0.025
    coef_df['Significance'] = coef_df['Significant'].map({True: 'Yes', False: 'No'})
    coef_df['abs_coef'] = coef_df['Coefficient'].abs()

    # Sort for nicer plotting
    coef_df = coef_df.sort_values('Coefficient')

    def bar_color(row):
        if row['Coefficient'] > 0 and row['Significant']:
            return 'rgb(33,102,172)'      # dark blue
        if row['Coefficient'] > 0 and not row['Significant']:
            return 'rgba(33,102,172,0.4)' # light blue
        if row['Coefficient'] < 0 and row['Significant']:
            return 'rgb(178,24,43)'       # dark red
        return 'rgba(178,24,43,0.4)'      # light red

    coef_df['color'] = coef_df.apply(bar_color, axis=1)

    fig = px.bar(
        coef_df,
        x='Coefficient',
        y='Feature',
        orientation='h',
        hover_data={
            'Coefficient': ':.3f',
            'p_value': ':.3e',
            'Significance': True
        },
        title=title
    )

    fig.update_traces(marker_color=coef_df['color'])
    fig.add_vline(x=0, line_dash='dash', line_color='black')

    fig.update_layout(
        xaxis_title='Coefficient (log-odds)',
        yaxis_title='Feature'
    )

    fig.write_html(output_path)

    fig.show()

    return coef_df

def feature_coef_significance_grid(coef_df, title, output_path):
    table = Figure(
        data=[
            Table(
                header=dict(
                    values=['Feature', 'Coefficient', 'p-value', 'Significant'],
                    fill_color='lightgrey',
                    align='left'
                ),
                cells=dict(
                    values=[
                        coef_df['Feature'],
                        coef_df['Coefficient'].round(3),
                        coef_df['p_value'].apply(lambda x: f"{x:.2e}"),
                        coef_df['Significance']
                    ],
                    fill_color=[
                        ['#e8f4ff' if s else '#fdecea' for s in coef_df['Significant']]
                    ],
                    align='left'
                )
            )
        ]
    )

    table.update_layout(title=title)
    table.write_html(output_path)

    table.show()

def plot_in_and_out_neg_link_frac_per_subs(large_gamergate_df, gamergate_subs):
## fraction of outgoing and ingoing negative links per subreddits in gamergate subs

    out_neg = (
        large_gamergate_df
        .groupby("source")["LINK_SENTIMENT"]
        .apply(lambda s: (s == -1).mean())
        .reset_index(name="neg_out_frac")
    )

    # keep only gamergate subreddits
    out_neg = out_neg[out_neg["source"].isin(gamergate_subs)]

    in_neg = (
        large_gamergate_df
        .groupby("target")["LINK_SENTIMENT"]
        .apply(lambda s: (s == -1).mean())
        .reset_index(name="neg_in_frac")
    )

    # keep only gamergate subreddits
    in_neg = in_neg[in_neg["target"].isin(gamergate_subs)]

    negativity_df = (
        out_neg.merge(
            in_neg,
            left_on="source",
            right_on="target",
            how="outer"
        )
    )

    negativity_df["subreddit"] = negativity_df["source"].combine_first(
        negativity_df["target"]
    )

    negativity_df = negativity_df[
        ["subreddit", "neg_out_frac", "neg_in_frac"]
    ].fillna(0)

    fig = go.Figure()

    fig.add_bar(
        x=negativity_df["subreddit"],
        y=negativity_df["neg_out_frac"],
        name="Negative outgoing",
        marker_color="crimson"
    )

    fig.add_bar(
        x=negativity_df["subreddit"],
        y=negativity_df["neg_in_frac"],
        name="Negative incoming",
        marker_color="royalblue"
    )

    fig.update_layout(
        barmode="group",
        title="Negative Incoming vs Outgoing Links (Gamergate Subreddits)",
        xaxis_title="Subreddit",
        yaxis_title="Fraction of negative links",
        yaxis_tickformat=".0%",
        template="plotly_white"
    )

    fig.show()



def plot_out_pos_neg_link_per_subs(large_gamergate_df, gamergate_subs):
## fraction of outgoing and ingoing negative links per subreddits in gamergate subs

    out_neg = (
        large_gamergate_df
        .groupby("source")["LINK_SENTIMENT"]
        .apply(lambda s: (s == -1).count())
        .reset_index(name="neg_out")
    )

    # keep only gamergate subreddits
    out_neg = out_neg[out_neg["source"].isin(gamergate_subs)]

    out_pos = (
        large_gamergate_df
        .groupby("source")["LINK_SENTIMENT"]
        .apply(lambda s: (s == 1).count())
        .reset_index(name="pos_out")
    )

    # keep only gamergate subreddits
    out_pos = out_pos[out_pos["source"].isin(gamergate_subs)]

    negativity_df = (
        out_neg.merge(
            out_pos,
            left_on="source",
            right_on="source",
            how="outer"
        )
    )

    negativity_df["subreddit"] = negativity_df["source"].combine_first(
        negativity_df["source"]
    )

    negativity_df = negativity_df[
        ["subreddit", "neg_out", "pos_out"]
    ].fillna(0)

    fig = go.Figure()

    fig.add_bar(
        x=negativity_df["subreddit"],
        y=negativity_df["neg_out"],
        name="Negative outgoing",
        marker_color="crimson"
    )

    fig.add_bar(
        x=negativity_df["subreddit"],
        y=negativity_df["pos_out"],
        name="Positive outgoing",
        marker_color="royalblue"
    )

    fig.update_layout(
        barmode="group",
        title="Outgoing Positive vs Negative Links (Gamergate Subreddits)",
        xaxis_title="Subreddit",
        yaxis_title="Number of links",
        template="plotly_white"
    )

    fig.show()