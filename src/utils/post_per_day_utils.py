import plotly.express as px
import pandas as pd

def plot_posts_per_day(subreddit_names, posts_per_day, rolling_window=10):
    """
    Plots the number of posts per day for a given subreddit using Plotly.

    Parameters
    ----------
    subreddit_names : list of str or str
        The name(s) of the subreddit(s).
    posts_per_day : pandas.DataFrame
        A DataFrame with columns 'subreddit', 'date', and 'post_count'.
    rolling_window : int
        The window size for the rolling average.
    """
    if isinstance(subreddit_names, str):
        subreddit_names = [subreddit_names]

    for subreddit_name in subreddit_names:
        data = posts_per_day[posts_per_day['subreddit'] == subreddit_name].copy()
        data['date'] = pd.to_datetime(data['date'])
        data = data.sort_values('date')
        data['post_count'] = data['post_count'].rolling(window=rolling_window).mean()
        
        title = f'Number of Posts per Day in r/{subreddit_name}, {rolling_window} day rolling average'
        
        fig = px.line(data, x='date', y='post_count', title=title,
                      labels={'date': 'Date', 'post_count': 'Number of Posts'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Number of Posts')
        fig.show()
        # Export to HTML
        fig.write_html(f'docs/assets/posts_per_day_{subreddit_name}.html')