import pandas as pd
import plotly.express as px
from src.data.some_dataloader import RedditPostDataset

def proportion_of_gg_in_politics(gg_df, pol_df):
    
    # add quarter timestamp
    gg_df['quarter'] = gg_df['TIMESTAMP'].dt.to_period('Q').dt.to_timestamp()
    pol_df['quarter'] = pol_df['TIMESTAMP'].dt.to_period('Q').dt.to_timestamp()

    gg_users_by_quarter = (gg_df.groupby('quarter')['USERNAME'].apply(set).to_dict())
    pol_users_by_quarter = (pol_df.groupby('quarter')['USERNAME'].apply(set).to_dict())

    results = []

    quarters = sorted(set(gg_users_by_quarter) & set(pol_users_by_quarter))

    for quarter in quarters:
        gg_users = gg_users_by_quarter[quarter]
        pol_users = pol_users_by_quarter[quarter]

        intersection = gg_users & pol_users
        union = gg_users | pol_users

        jaccard = len(intersection) / len(union) if union else 0
        pct_gg_in_pol = len(intersection) / len(gg_users) if gg_users else 0

        results.append({
            'quarter': quarter,
            'users': len(gg_users),
            'pol_users': len(pol_users),
            'shared_users': len(intersection),
            'jaccard_similarity': jaccard,
            'Proportion users in political': pct_gg_in_pol
        })

    overlap_q_df = pd.DataFrame(results).sort_values('quarter')

    fig = px.line(
        overlap_q_df,
        x='quarter',
        y='Proportion users in political',
        markers=True,
        title='Proportion of r/gaming users active in Politics',
        labels={
            'quarter': 'Quarter',
            'Gg active in politics': 'Proportion of Gg user in '
        },
        hover_data={
            'users': True,
            'pol_users': True,
            'shared_users': True,
            'jaccard_similarity': ':.3f'
        }
    )

    fig.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True, tickformat='.0%'),
        hovermode='x unified'
    )

    fig.write_html('docs/assets/gaming_proportion_politics.html')

    fig.show()