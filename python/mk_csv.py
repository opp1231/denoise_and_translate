import csv
import re
import os
import argparse
from pathlib import Path, PurePath

def parse_args():

	parser = argparse.ArgumentParser(description="Creates .csv to define input/output paths for images to send to fnet.predict")
	parser.add_argument('data_dir', type=Path, help='path to save csv')
	parser.add_argument('inpath', type=Path, help='path to input directory')
	args = parser.parse_args()

	return args

def list_files_of_type(ddir, extension):
	files = [f for f in os.listdir(ddir) if os.path.isfile(os.path.join(ddir,f)) and f.endswith(extension)]
	return files

def make_csv(ddir,inpath):
	in_ims_dir = inpath
	out_ims_dir = inpath

	with open(os.path.join(ddir,'data_pred_new_temp.csv'), 'w', newline='') as file:
		writer = csv.writer(file, delimiter=',',
					quotechar='|', quoting=csv.QUOTE_MINIMAL)

		in_ims = list_files_of_type(in_ims_dir,'.tif')
		writer.writerow(["Image","Signal","Target"])
		for f in range(len(in_ims)):
			# pattern = re.compile(r'(scan\d+')
			# match = re.search(pattern,in_ims[f])
			# print(match)
			# if f > 52:
			writer.writerow([f,os.path.join(in_ims_dir,in_ims[f]), 
					os.path.join(out_ims_dir,in_ims[f])])
			

	return inpath

def main():
	args = parse_args()

	make_csv(args.data_dir,args.inpath)

if __name__ == '__main__':

	main()
