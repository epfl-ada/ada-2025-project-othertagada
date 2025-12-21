import pandas as pd
import plotly.express as px
from src.data.some_dataloader import RedditPostDataset


def get_core_gg_users(gg_df, subs_gg, min_posts=2):
    gg_filtered = gg_df[gg_df["SUBREDDIT"].isin(subs_gg)]

    gg_user_counts = gg_filtered.groupby("USERNAME").size()
    core_users = set(gg_user_counts[gg_user_counts >= min_posts].index)

    return core_users

def proportion_of_gg_in_politics(gg_df, pol_df, max_n=10):
    subs_gg = {
        'shitghazisays',
        'kotakuinaction',
        'amrsucks',
        'srssucks',
        'kiachatroom',
    }

    subs_pol = {
        'the_donald',
        'conservative',
        'conspiracy',
    }

    gg_only = gg_df[gg_df["SUBREDDIT"].isin(subs_gg)].copy()
    pol_only = pol_df[pol_df["SUBREDDIT"].isin(subs_pol)].copy()

    # Add quarters once
    gg_only["quarter"] = gg_only["TIMESTAMP"].dt.to_period("Q").dt.to_timestamp()
    pol_only["quarter"] = pol_only["TIMESTAMP"].dt.to_period("Q").dt.to_timestamp()

    quarters = sorted(gg_only["quarter"].unique())

    all_results = []

    # -------------------------------------------------
    # Loop over min_posts = 1 ... max_n
    # -------------------------------------------------
    for min_posts in range(1, max_n + 1):

        # ---- 1) GG cohort definition
        gg_counts = gg_only.groupby("USERNAME").size()
        gg_users = set(gg_counts[gg_counts >= min_posts].index)

        if not gg_users:
            continue

        # ---- 2) When each GG user first appears (for eligibility by quarter)
        gg_first_seen = (
            gg_only[gg_only["USERNAME"].isin(gg_users)]
            .groupby("USERNAME")["quarter"]
            .min()
        )

        # ---- 3) Political activity restricted to GG users
        pol_users_by_quarter = (
            pol_only[pol_only["USERNAME"].isin(gg_users)]
            .groupby("quarter")["USERNAME"]
            .apply(set)
            .to_dict()
        )

        # ---- 4) Per-quarter proportions
        for q in quarters:
            eligible_gg_users = set(
                gg_first_seen[gg_first_seen <= q].index
            )

            pol_users_q = pol_users_by_quarter.get(q, set())
            active_in_pol = eligible_gg_users & pol_users_q

            proportion = (
                len(active_in_pol) / len(eligible_gg_users)
                if eligible_gg_users else 0
            )

            all_results.append({
                "quarter": q,
                "min_posts": min_posts,
                "eligible_gg_users": len(eligible_gg_users),
                "gg_users_active_in_politics": len(active_in_pol),
                "Proportion users in political": proportion,
            })

    df = pd.DataFrame(all_results).sort_values(["min_posts", "quarter"])

    # -------------------------------------------------
    # Plot
    # -------------------------------------------------
    fig = px.line(
        df,
        x="quarter",
        y="Proportion users in political",
        color="min_posts",
        markers=True,
        title="Political activity per quarter among Gamergate users (varying GG activity threshold)",
        labels={
            "min_posts": "Min. GG posts (n)",
            "Proportion users in political": "Proportion active in political subreddits",
        },
        hover_data={
            "eligible_gg_users": True,
            "gg_users_active_in_politics": True,
        },
    )

    fig.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True, tickformat=".0%"),
        hovermode="x unified",
        legend_title_text="GG activity threshold",
    )

    fig.write_html(
        "docs/assets/gamergate_proportion_politics_multiple_lines.html",
        include_plotlyjs=False,
        full_html=False,
    )

    fig.show()