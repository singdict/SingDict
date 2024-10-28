import sys, csv, json

def parse_args():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required=True, help='input csv file')
	parser.add_argument('-v', '--verbose', action='count', default=0)
	return parser.parse_args()

def get_csv_reader():
	input_file = open(args.input, 'r')
	csv_reader = csv.reader(input_file, delimiter=',')
	return csv_reader

def is_head(row):
	if ''.join(row).startswith('WordDescription'):
		if args.verbose != 0:
			print(row)
		return True
	return False

def parse_row(row):
	#['Word', 'Description', 'Description OK', 'Description (updated)', Description (final), 'Example (final)', 'Remarks (if applicable)', 'POS', 'Pronun', 'Origin', 'Reference']
	word, old_desc, desc_ok, new_desc, final_desc, example, alt_spell, _, pos, pronun, origin, license_, reference = row[:13]

	if desc_ok.startswith('Not sure'): return None

	if len(final_desc) == 0 or not final_desc: return None

	return [word, final_desc, example, pos, pronun, origin]

def postproc_desc(desc):
	import re

def main():
	csv_reader = get_csv_reader()

	statistics = {'has_def':0, 'no_has_def':0}
	for row in csv_reader:
		if is_head(row): continue
		parsed_row = parse_row(row)
		if not parsed_row: continue

		word, desc, example, pos, pronun, origin = parsed_row

		jo = {"Word": word, "POS": pos, "Pronunciation": pronun, "Definition": desc, "Example": example, "Origin": origin}
		with open('{}.jsonl'.format(word), 'w') as ofp:
			json.dump(jo, ofp, ensure_ascii=False)

if __name__ == '__main__':
	args = parse_args()
	main()
