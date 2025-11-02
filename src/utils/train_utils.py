import statsmodels.formula.api as smf
import pickle
import pandas as pd
from src.utils.data_utils import *

def train_logit_link_sentiment_timewindow(df, properties, save_path, from_date, to_date):
    """ Train logistic regression model over properties features to classify link sentiment of post
        over a given time window. 
    
    Args:
        data (df): dataframe containing 'LINK_SENTIMENT', 'TIMESTAMP' and 'PROPERTIES'
        properties (int[]): list of the properties to use for logit, the number refers to 
            the place of the property in the vector 'PROPERIES' as given in the paper
        save_path (str): file path to save the model 
        from_date (str): 'YYYY-MM-DD' Start date included
        to_date (str): 'YYYY-MM-DD' End date excluded
    """

    window_df = get_df_time_window(df, from_date, to_date)
    train_logit_link_sentiment(window_df, properties, save_path)


def train_logit_link_sentiment(df, properties, save_path):
    """ Train logistic regression model over properties features to classify link sentiment of post.

    Args:
        df (df): dataframe containing 'LINK_SENTIMENT' and 'PROPERTIES'
        properties (int[]): list of the properties to use for logit, the number refers to 
            the place of the property in the vector 'PROPERTIES' as given in the paper
        save_path (str): save model in this file
    """

    # check properties are in the reddit dataset
    for p in properties:
        if p < 1 or p > 86:
            raise ValueError('Prperties must be between 1 and 86.')
    
    # check dataframe has LINK_SENTIMENT 
    if 'LINK_SENTIMENT' not in df.columns:
        raise ValueError("LINK_SENTIMENT column is missing")

    # Expand property vectors into individual columns
    prop_df = pd.DataFrame(df['PROPERTIES'].tolist())
    prop_df.columns = [f"prop_{i+1}" for i in range(prop_df.shape[1])]
    selected_cols = [prop_df.columns[i-1] for i in properties]
    df = pd.concat([df, prop_df[selected_cols]], axis=1)

    # logistic regression demands value 0 or 1 (-1.0 => 0.0)
    df['LINK_SENTIMENT'] = df['LINK_SENTIMENT'].astype(float)
    df["LINK_SENTIMENT"] = df["LINK_SENTIMENT"].replace(-1.0, 0.0)

    # Fit model
    formula = "LINK_SENTIMENT ~ " + " + ".join(selected_cols)
    model = smf.logit(formula=formula, data=df).fit(disp=False)

    # Save model to path
    with open(save_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Model saved to {save_path}")
    print(model.summary())
