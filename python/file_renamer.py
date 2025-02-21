import os
import sys
import re
import argparse
from pathlib import Path, PurePath

def parse_args():
    parser = argparse.ArgumentParser(description='Simple file renamer for putting fnet images into MOSAIC-compatible format')
    parser.add_argument('inpath', type=Path, help='path to the data')
    parser.add_argument('camera',type=str, help = 'Camera A or B')
    parser.add_argument('refpath', type=Path, help='path to data name to copy')
    parser.add_argument('--dry-run', '-d',default=False, action='store_true', dest='dryrun',help='execute by printing names to output.txt rather than renaming')
    args = parser.parse_args()

    return args

def string_finder(old_str, old_phrases):
    vars = []
    for str in old_phrases:
        new_str = old_str.partition(str)[2]
        new_str1 = new_str.partition('_')[0]
        vars.append(new_str1)
    return dict(zip(old_phrases,vars))

def tag_filename(filename, string):
    f = PurePath(filename)
    return f.stem + '_' + string + f.suffix

def file_renamer(folder,comp_folder,cam,tag,dryrun=False):

    original_stdout = sys.stdout
    with open(Path(folder) / Path('output.txt'),'w') as file:
        sys.stdout = file

        comp_fnames = os.listdir(comp_folder)
        comp_fnames_camb = []
        for nn, fname in enumerate(os.listdir(comp_folder)):

            ext = Path(fname).suffix
            if ext=='.tif':
                if fname.partition('Cam')[-1].split('_')[0] == cam:
                    comp_fnames_camb.append(fname)

        pattern_tile = re.compile(r'(?<=[stack])[0-9]+')
        for count, filename in enumerate(os.listdir(folder)):
            print(filename)
            ext = Path(filename).suffix
            m = re.findall(pattern_tile,filename)
            # if ext=='.tif' and m[0]:
            if ext=='.tif':
                str_split = filename.split('_')
                stack = str_split[1].split('.')[0].zfill(4)
                print(stack)

                for nn, fname in enumerate(comp_fnames_camb):
                    m = re.findall(pattern_tile,fname)
                    if m[0] == stack:
                        src = Path(folder) / Path(filename)
                        if tag != 'None':
                            dst_new = Path(folder) / Path(tag_filename(fname,tag))
                        else:
                            dst_new = Path(folder) / Path(fname)
                        if dryrun:
                            print(src)
                            print(dst_new)
                        else:
                            os.rename(src,dst_new)

    sys.stdout = original_stdout

    return 1


def main():
    args = parse_args()

    file_renamer(folder=args.inpath,comp_folder=args.refpath,cam=args.camera,tag='prednuc',dryrun=args.dryrun)


if __name__ == '__main__':

    main()