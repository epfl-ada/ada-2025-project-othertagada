import statsmodels.formula.api as smf
import pickle
import pandas as pd
from src.utils.data_utils import *
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix
import statsmodels.api as sm

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


def kmeans_cluster_graph_features(features, n_clusters=10):
    """
    Perform KMeans clustering on extracted graph features and add cluster labels.

    Parameters
    ----------
    features : pandas.DataFrame
        The node-level features computed by `extract_graph_features`.
    n_clusters : int, optional
        Number of clusters for KMeans (default is 10).

    Returns
    -------
    features_with_clusters : pandas.DataFrame
        Same as input, but with an extra column: 'cluster'.
    kmeans : sklearn.cluster.KMeans
        The trained KMeans model (for later analysis or visualization).
    """


    # Normalize features
    X = features[['degree', 'in_degree', 'out_degree', 'clustering', 'pagerank', 'betweenness','closeness']]
    X_scaled = StandardScaler().fit_transform(X)

    # Cluster subreddits
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    features['cluster'] = kmeans.fit_predict(X_scaled)

    return features, kmeans

def train_test_set(data):

    train_set, test_set = train_test_split(data, test_size=0.2,random_state=42)
   

    return train_set, test_set

def data_scaling_for_training(train_set, test_set, feature_columns, feature_to_exclude):
    """
    Scales feature matrices for training and testing and prepares binary labels
    for link sentiment classification.

    Parameters
    ----------
    train_set : pandas.DataFrame
        Training dataset containing feature columns and a 'LINK_SENTIMENT' column.

    test_set : pandas.DataFrame
        Test dataset containing feature columns and a 'LINK_SENTIMENT' column.

    feature_columns : list of str
        List of feature column names to be used for model training.

    feature_to_exclude : str or None
        Name of a feature to exclude from the feature set (used for ablation
        or significance analysis). If None, all features are used.

    Returns
    -------
    X_train : numpy.ndarray
        Standardized feature matrix for the training set.

    y_train : pandas.Series
        Binary training labels (True if LINK_SENTIMENT == 1, False otherwise).

    X_test : numpy.ndarray
        Standardized feature matrix for the test set.

    y_test : pandas.Series
        Binary test labels (True if LINK_SENTIMENT == 1, False otherwise).
    """

    
    new_feature_columns = feature_columns.copy()

    ## remove one feature to evaluate its significance
    if feature_to_exclude != None :
        new_feature_columns.remove(feature_to_exclude)

    

    X_train = StandardScaler().fit_transform(train_set[new_feature_columns])
    y_train = train_set["LINK_SENTIMENT"].map(lambda x : (x == 1))  
    X_test = StandardScaler().fit_transform(test_set[new_feature_columns])
    y_test = test_set["LINK_SENTIMENT"].map(lambda x : (x == 1))

    return X_train, y_train, X_test, y_test 

def logistic_regression(X_train, y_train, X_test, y_test):
    """
    Trains a scikit-learn logistic regression model.

    Parameters
    ----------
    X_train : numpy.ndarray
        Feature matrix for training.

    y_train : array-like
        Binary training labels.

    X_test : numpy.ndarray
        Feature matrix for testing.

    y_test : array-like
        Binary test labels.

    Returns
    -------
    logistic : sklearn.linear_model.LogisticRegression
        Fitted logistic regression model.

    link_prediction : numpy.ndarray
        Predicted binary labels for the test set.
    """


    logistic = LogisticRegression().fit(X_train, y_train)

    link_prediction = logistic.predict(X_test)

    return logistic, link_prediction

def sm_log_reg(X_train, y_train, X_test, y_test):
    """
    Fits a logistic regression model using statsmodels and evaluates its
    predictive performance on a test set.

    Parameters
    ----------
    X_train : numpy.ndarray
        Feature matrix for training.

    y_train : array-like
        Binary training labels.

    X_test : numpy.ndarray
        Feature matrix for testing.

    y_test : array-like
        Binary test labels.

    Returns
    -------
    log_reg : statsmodels.discrete.discrete_model.BinaryResults
        Fitted statsmodels logistic regression object.

    prediction : list of int
        Binary predictions (0 or 1) for the test set.
    """


    log_reg = sm.Logit(y_train, X_train).fit()
    yhat = log_reg.predict(X_test)
    prediction = list(map(round, yhat))
    print('Test accuracy = ', accuracy_score(y_test, prediction)) 
    print(log_reg.summary())

    return log_reg, prediction