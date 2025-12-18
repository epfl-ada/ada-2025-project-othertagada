# SOURCE: https://github.com/Watchful1/PushshiftDumps/blob/master/scripts/iterate_folder.py
# Modified by Robin

import zstandard
import os
import json
import sys
from datetime import datetime, UTC
import logging.handlers
import csv
import argparse


log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

# These are the subreddits related to gamergate
gamergate_subs = {
		"srssucks",
		"shitghazisays",
		"kotakuinaction",
		"amrsucks",
		"drama",
		"subredditdrama",
		"againstgamergate",
		"ggfreeforall",
		"shitliberalssay",
		"kiachatroom",
		"circlebroke2",
		"gamerghazi",
		"topmindsofreddit",
		"bestofoutrageculture",
		"shitredditsays",
		"panichistory",
		"the_donald",
    }

def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk
	try:
		return chunk.decode()
	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		log.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


def read_lines_zst(file_name):
	with open(file_name, 'rb') as file_handle:
		buffer = ''
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)

			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line.strip(), file_handle.tell()

			buffer = lines[-1]

		reader.close()

def zst_to_gamer_gate_csv(subs=gamergate_subs, output_file_path="data/gamergate_post_data.csv"):
	# Init output file
	with open(output_file_path, "w", encoding='utf-8', newline="") as output_file:
		writer = csv.writer(output_file)
		writer.writerow(["TIMESTAMP", "SUBREDDIT", "USERNAME", "TITLE", "BODY_TEXT", "NUM_COMMENTS", "POST_ID"])

		input_folder = "data/RedditDataset/reddit/submissions/"
		input_files = []
		total_size = 0
		for subdir, dirs, files in os.walk(input_folder):
			for filename in files:
				input_path = os.path.join(subdir, filename)
				if input_path.endswith(".zst"):
					file_size = os.stat(input_path).st_size
					total_size += file_size
					input_files.append([input_path, file_size])
					
		# Sort input files to process older files first
		input_files.sort(key=lambda x: (int(os.path.basename(x[0]).split('_')[1].split('-')[0]), int(os.path.basename(x[0]).split('_')[1].split('-')[1].split('.')[0])))

		log.info(f"Processing {len(input_files)} files of {(total_size / (2**30)):.2f} gigabytes")

		total_lines = 0
		total_bytes_processed = 0
		
		# Define fields to extract
		fields = ["created_utc", "subreddit", "author", "title", "text", "num_comments", "id"]

		for input_file in input_files:
			file_lines = 0
			file_bytes_processed = 0
			created = None
			for line, file_bytes_processed in read_lines_zst(input_file[0]):
				obj = json.loads(line)
				output_obj = []
				for field in fields:
					if field == "created_utc":
						value = datetime.fromtimestamp(int(obj['created_utc']), UTC).strftime("%Y-%m-%d %H:%M:%S")
					elif field == "subreddit":
						if 'permalink' in obj:
							subreddit_lower = f"{obj['permalink'].split('/')[2].lower()}"
						else:
							subreddit_lower = f"{obj['subreddit'].lower()}"
						if subreddit_lower not in subs:
							break
						value = subreddit_lower
					elif field == "author":
						value = f"u/{obj['author']}"
					elif field == "text":
						if 'selftext' in obj:
							value = obj['selftext']#[:32000] # remove first # if the subreddit has very large text posts and you want to open this in excel
						else:
							value = ""
					else:
						value = obj[field]
					output_obj.append(str(value).encode("utf-8", errors='replace').decode())
				
				created = output_obj[0]
				file_lines += 1

				if file_lines == 1:
					log.info(f"{created} : {file_lines + total_lines:,} : 0% : {(total_bytes_processed / total_size) * 100:.0f}%")
				if file_lines % 100000 == 0:
					log.info(f"{created} : {file_lines + total_lines:,} : {(file_bytes_processed / input_file[1]) * 100:.0f}% : {(total_bytes_processed / total_size) * 100:.0f}%")
				
				# Only write if all fields are present (i.e. subreddit is in subs)
				if(len(output_obj) == len(fields)):
					writer.writerow(output_obj)
			total_lines += file_lines
			total_bytes_processed += input_file[1]
			log.info(f"{created} : {total_lines:,} : 100% : {(total_bytes_processed / total_size) * 100:.0f}%")
			
		log.info(f"Total: {total_lines}")
		output_file.close()


if __name__ == '__main__':
	# Parse arguments
	parser = argparse.ArgumentParser("zst_to_gamergate_csv")
	parser.add_argument('-l','--subreddit_list', nargs='+', help='List of subreddits', required=False)
	parser.add_argument('-o', '--file_output_path', help="Output path", type=str, required=False)
	args = parser.parse_args()
	subs = gamergate_subs
	if args.subreddit_list:
		subs = args.subreddit_list
		print(f"Using subreddit list: {subs}")
	output_file_path = "data/gamergate_post_data.csv"
	if args.file_output_path:
		output_file_path = args.file_output_path

	zst_to_gamer_gate_csv(subs=subs, output_file_path=output_file_path)

