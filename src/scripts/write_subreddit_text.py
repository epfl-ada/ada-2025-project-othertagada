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

def write_subreddit_monthly_text_documents():

    df = pd.read_csv("data/gamergate_post_data.csv")

    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce')

    df['TITLE'] = df['TITLE'].fillna("")
    df['BODY_TEXT'] = df['BODY_TEXT'].fillna("")

    df['YEAR_MONTH'] = df['TIMESTAMP'].dt.to_period('M').astype(str)

    output_folder = "outputs/subreddit_text_documents_monthly"
    os.makedirs(output_folder, exist_ok=True)

    for subreddit, sub_group in df.groupby('SUBREDDIT'):
        for year_month, month_group in sub_group.groupby('YEAR_MONTH'):

            combined_text = []

            for _, row in month_group.iterrows():
                text_block = f"{row['TITLE']}\n{row['BODY_TEXT']}"
                combined_text.append(text_block)

            final_text = "\n".join(combined_text)

            sub_folder = os.path.join(output_folder, subreddit)
            os.makedirs(sub_folder, exist_ok=True)

            file_path = os.path.join(sub_folder, f"{subreddit}_{year_month}.txt")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_text)

            print(f"Created: {file_path}")

    print("All monthly subreddit text files created in:", output_folder)

if __name__ == '__main__':
	write_subreddit_monthly_text_documents()
     