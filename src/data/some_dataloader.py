import torch
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, Dataset

class RedditDataset(Dataset):
    """
    A dataset implements 2 functions
        - __len__  (returns the number of samples in our dataset)
        - __getitem__ (returns a sample from the dataset at the given index idx)
    """

    def __init__(self, data_path):
        super().__init__()
        self.data_path = data_path
        self.data = pd.read_csv(data_path, sep='\t', header=0) # Read TSV file
    
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
        properties = row.get('PROPERTIES').split(',') if 'PROPERTIES' in self.data.columns else None

        sample = {
            'source_subreddit': source,
            'target_subreddit': target,
            'post_id': post_id,
            'timestamp': timestamp,
            'properties': properties,
            'link_sentiment': link_sentiment,
        }

        return sample


class SomeDatamodule(DataLoader):
    """
    Allows you to sample train/val/test data, to later do training with models.
        
    """
    def __init__(self):
        super().__init__()
        ...