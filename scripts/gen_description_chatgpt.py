import time
import json
import tqdm
import glob
import openai

openai.api_key = ""

def response(word):
    description = "You are writing a Singlish dictionary. Now, please write a dictionary entry of '{}'. With a full description of the word, its pronunciation and alternate spellings if there are."
    api_result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": description.format(word)},
        ],
    )
    return api_result["choices"][0]["message"]["content"]

def get_processed_words(desc_file):
    dfp = open(desc_file)
    words = []
    for line in dfp:
        jo = json.loads(line)
        words.append(jo["word"])
    return set(words)

def parse_args():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-w', '--word', help='word list file path')
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	word_file = args.word
	desc_file = word_file.replace("0_words.txt", "1_descriptions.jsonl")
	desc_fp = open(desc_file, "a")
	processed_words = get_processed_words(desc_file)

	print("Currently {} words are listed on dictionary.".format(len(processed_words)))

	words = open(word_file).read().strip().split('\n')
	for word in tqdm.tqdm(words):
		word = word.strip()
		if word in processed_words:
			continue
		while True:
			try:
				description = response(word)
			except openai.error.RateLimitError as e:
				time.sleep(10)
			else:
				break
		jo = {"word": word, "description": description}
		json.dump(jo, desc_fp)
		desc_fp.write("\n")
		desc_fp.flush()
