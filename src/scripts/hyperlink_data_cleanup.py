import pandas as pd
import zstandard as zstd
import csv
import sqlite3
from build_id_timestamp_db import build_hyperlink_data_db
# If len(id) != 6 remove last character (Some IDs have an extra 's' at the end and in our datset all IDs have length 6) 
# Timestamps seem quite inaccurate, we should replace them using the post IDs to fetch accurate timestamps from the new dataset
def clean_hyperlink_data():
    build_hyperlink_data_db()

    conn = sqlite3.connect("data/timestamps.db")
    cur = conn.cursor()

    paths = [["data/soc-redditHyperlinks-title.tsv", "data/soc-redditHyperlinks-title-cleaned.tsv"], ["data/soc-redditHyperlinks-body.tsv", "data/soc-redditHyperlinks-body-cleaned.tsv"]]

    for in_path, out_path in paths:
        data = pd.read_csv(in_path, sep='\t', header=0)
        data['POST_ID'] = data['POST_ID'].apply(lambda x: x[:-1] if len(str(x)) != 6 else x)

        def _fetch_ts(row):
            cur.execute("SELECT ts FROM ts WHERE id=?", (row["POST_ID"],))
            rec = cur.fetchone()
            if rec:
                row["TIMESTAMP"] = rec[0]
            return row

        data = data.apply(_fetch_ts, axis=1)

        data.to_csv(out_path, sep="\t")
    
    cur.execute("DROP TABLE IF EXISTS ts")
    conn.close()



