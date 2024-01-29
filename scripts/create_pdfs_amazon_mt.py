from fpdf import FPDF

DATA_PATH = 'data/dictionary/*/1_descriptions.jsonl'

def create_output_dir():
	import os
	cur_path = os.getcwd()
	if not cur_path.endswith('ComeFromWhere'):
		raise Exception('PathError', "The script should be excuted on the root of the main repository('ComeFromeWhere').")
	
	if not os.path.exists('pdfs/'):
		os.mkdir('pdfs')

def load_data():
	import glob
	import json
	import pandas as pd

	total_data = []
	for fp in glob.glob(DATA_PATH):
		d = pd.read_json(path_or_buf=fp, lines=True).to_json(orient='records')
		total_data.extend(json.loads(d))

	return total_data

if __name__ == '__main__':
	create_output_dir()

	data = load_data()

'''
pdf = FPDF()
pdf.add_page()
pdf.set_font('helvetica', size=12)
pdf.cell(txt="hello world")
pdf.output("hello_world.pdf")
'''
