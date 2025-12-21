import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from src.data.some_dataloader import RedditPostDataset

def jaccard_similarity(list1, list2):
    """ compute jaccard similarity between the sets created from two lists

    Args:
        list1 (list): first list
        list2 (list): second list
    Returns:
        jaccard similarity
    """
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

def heatmap_user_in_commun(post_data):
    """ plots and save heatmap of jaccard similarity between all subreddits in dataframe.

    Args:
        post_data (df): dataframe to plot histogram
    """

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

    jaccard_df = pd.DataFrame(jaccard_matrix, index=subreddits, columns=subreddits)

    plt.figure(figsize=(12, 10))

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
    plt.savefig('docs/assets/heatmap_users.png')
    plt.show()