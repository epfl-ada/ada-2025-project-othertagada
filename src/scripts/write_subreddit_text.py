import pandas as pd
import os

def write_subreddit_text_document():

    df = pd.read_csv("data/gamergate_post_data.csv")
    
    output_folder = "outputs/subreddit_text_documents"
    os.makedirs(output_folder, exist_ok=True)

    df['TITLE'] = df['TITLE'].fillna("")
    df['BODY_TEXT'] = df['BODY_TEXT'].fillna("")

    # Group by subreddit
    for subreddit, group in df.groupby('SUBREDDIT'):

        combined_text = []
        
        for _, row in group.iterrows():
            text_block = f"{row['TITLE']}\n{row['BODY_TEXT']}"
            combined_text.append(text_block)
        
        final_text = "\n".join(combined_text)
        
        file_path = os.path.join(output_folder, f"{subreddit}.txt")
        
        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_text)

        print('Text file for:', subreddit, 'created.')

    print("All text files created in:", output_folder)

if __name__ == '__main__':
	write_subreddit_text_document()