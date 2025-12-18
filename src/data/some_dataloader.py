import torch
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, Dataset

class RedditHyperlinkDataset(Dataset):
    """
    A dataset implements 2 functions
        - __len__  (returns the number of samples in our dataset)
        - __getitem__ (returns a sample from the dataset at the given index idx)
    """

    def __init__(self, data_path_title = "data/soc-redditHyperlinks-title-cleaned.tsv", data_path_body = "data/soc-redditHyperlinks-body-cleaned.tsv"):
        super().__init__()

        self.data_path_title = data_path_title  
        self.data_path_body = data_path_body

        self.data_title = pd.read_csv(data_path_title, sep='\t', header=0) # Read TSV file
        self.data_body = pd.read_csv(data_path_body, sep='\t', header=0) # Read TSV file

        self.data_title['TIMESTAMP'] = pd.to_datetime(self.data_title['TIMESTAMP']) # Convert time
        self.data_body['TIMESTAMP'] = pd.to_datetime(self.data_body['TIMESTAMP']) # Convert time

        self.data_title['PROPERTIES'] = self.data_title['PROPERTIES'].apply(lambda x: [float(i) for i in str(x).split(',')])
        self.data_body['PROPERTIES'] = self.data_body['PROPERTIES'].apply(lambda x: [float(i) for i in str(x).split(',')])

        self.data = pd.concat([self.data_title, self.data_body], ignore_index=True, sort=False)

        liwc_cols = [
            "chars","chars_no_ws","frac_alpha","frac_digits","frac_upper","frac_ws",
            "frac_special","num_words","num_unique","num_long_words","avg_word_len",
            "num_stopwords","frac_stopwords","num_sentences","num_long_sentences",
            "avg_chars_sentence","avg_words_sentence","automated_readability",
            "vader_pos","vader_neg","vader_compound",
            "LIWC_Funct","LIWC_Pronoun","LIWC_Ppron","LIWC_I","LIWC_We","LIWC_You",
            "LIWC_SheHe","LIWC_They","LIWC_Ipron","LIWC_Article","LIWC_Verbs",
            "LIWC_AuxVb","LIWC_Past","LIWC_Present","LIWC_Future","LIWC_Adverbs",
            "LIWC_Prep","LIWC_Conj","LIWC_Negate","LIWC_Quant","LIWC_Numbers",
            "LIWC_Swear","LIWC_Social","LIWC_Family","LIWC_Friends","LIWC_Humans",
            "LIWC_Affect","LIWC_Posemo","LIWC_Negemo","LIWC_Anx","LIWC_Anger",
            "LIWC_Sad","LIWC_CogMech","LIWC_Insight","LIWC_Cause","LIWC_Discrep",
            "LIWC_Tentat","LIWC_Certain","LIWC_Inhib","LIWC_Incl","LIWC_Excl",
            "LIWC_Percept","LIWC_See","LIWC_Hear","LIWC_Feel","LIWC_Bio",
            "LIWC_Body","LIWC_Health","LIWC_Sexual","LIWC_Ingest","LIWC_Relativ",
            "LIWC_Motion","LIWC_Space","LIWC_Time","LIWC_Work","LIWC_Achiev",
            "LIWC_Leisure","LIWC_Home","LIWC_Money","LIWC_Relig","LIWC_Death",
            "LIWC_Assent","LIWC_Dissent","LIWC_Nonflu","LIWC_Filler"
        ]

        def unpack_properties(row):
            return {col: row[i] for i, col in enumerate(liwc_cols)}

        liwc_df = self.data['PROPERTIES'].apply(unpack_properties).apply(pd.Series)

        self.data = pd.concat([self.data, liwc_df], axis=1)
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # support tensor indices from DataLoader samplers
        if isinstance(idx, (torch.Tensor, np.ndarray)):
            idx = idx.tolist()

        row = self.data.iloc[idx]

        # Basic fields
        source = row.get('SOURCE_SUBREDDIT') if 'SOURCE_SUBREDDIT' in self.data.columns else None
        target = row.get('TARGET_SUBREDDIT') if 'TARGET_SUBREDDIT' in self.data.columns else None
        post_id = row.get('POST_ID') if 'POST_ID' in self.data.columns else None
        timestamp = row.get('TIMESTAMP') if 'TIMESTAMP' in self.data.columns else None
        link_sentiment = row.get('LINK_SENTIMENT') if 'LINK_SENTIMENT' in self.data.columns else None
        properties = row.get('PROPERTIES') if 'PROPERTIES' in self.data.columns else None

        sample = {
            'source_subreddit': source,
            'target_subreddit': target,
            'post_id': post_id,
            'timestamp': timestamp,
            'properties': properties,
            'link_sentiment': link_sentiment,
        }

        return sample

class RedditPostDataset(Dataset):
    """
    A dataset implements 2 functions
        - __len__  (returns the number of samples in our dataset)
        - __getitem__ (returns a sample from the dataset at the given index idx)
    """

    def __init__(self, data_path = "data/gamergate_post_data.csv"):
        super().__init__()

        self.data_path = data_path
        self.data = pd.read_csv(data_path, header=0) # Read CSV file

        self.data['TIMESTAMP'] = pd.to_datetime(self.data['TIMESTAMP']) # Convert time
        self.data = self.data[~(self.data['SUBREDDIT'] == 'the_donald')] # getting rid of unrelated subreddit
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # support tensor indices from DataLoader samplers
        if isinstance(idx, (torch.Tensor, np.ndarray)):
            idx = idx.tolist()

        row = self.data.iloc[idx]

        # Basic fields
        timestamp = row.get('TIMESTAMP') if 'TIMESTAMP' in self.data.columns else None
        subreddit = row.get('SUBREDDIT') if 'SUBREDDIT' in self.data.columns else None
        username = row.get('USERNAME') if 'USERNAME' in self.data.columns else None
        title = row.get('TITLE') if 'TITLE' in self.data.columns else None
        body_text = row.get('BODY_TEXT') if 'BODY_TEXT' in self.data.columns else None
        num_comments = row.get('NUM_COMMENTS') if 'NUM_COMMENTS' in self.data.columns else None
        post_id = row.get('POST_ID') if 'POST_ID' in self.data.columns else None

        sample = {
            'timestamp': timestamp,
            'subreddit': subreddit,
            'username': username,
            'title': title,
            'body_text': body_text,
            'num_comment': num_comments,
            'post_id': post_id,
        }

        return sample

class RedditPoliticalPostDataset(Dataset):
    """
    A dataset implements 2 functions
        - __len__  (returns the number of samples in our dataset)
        - __getitem__ (returns a sample from the dataset at the given index idx)
    """

    def __init__(self, data_path = "data/gamergate_post_data.csv"):
        super().__init__()

        self.data_path = data_path
        self.data = pd.read_csv(data_path, header=0) # Read CSV file

        self.data['TIMESTAMP'] = pd.to_datetime(self.data['TIMESTAMP']) # Convert time
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # support tensor indices from DataLoader samplers
        if isinstance(idx, (torch.Tensor, np.ndarray)):
            idx = idx.tolist()

        row = self.data.iloc[idx]

        # Basic fields
        timestamp = row.get('TIMESTAMP') if 'TIMESTAMP' in self.data.columns else None
        subreddit = row.get('SUBREDDIT') if 'SUBREDDIT' in self.data.columns else None
        username = row.get('USERNAME') if 'USERNAME' in self.data.columns else None
        title = row.get('TITLE') if 'TITLE' in self.data.columns else None
        body_text = row.get('BODY_TEXT') if 'BODY_TEXT' in self.data.columns else None
        num_comments = row.get('NUM_COMMENTS') if 'NUM_COMMENTS' in self.data.columns else None
        post_id = row.get('POST_ID') if 'POST_ID' in self.data.columns else None

        sample = {
            'timestamp': timestamp,
            'subreddit': subreddit,
            'username': username,
            'title': title,
            'body_text': body_text,
            'num_comment': num_comments,
            'post_id': post_id,
        }

        return sample

class SomeDatamodule(DataLoader):
    """
    Allows you to sample train/val/test data, to later do training with models.
        
    """
    def __init__(self):
        super().__init__()
        ...