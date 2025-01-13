import numpy as np
from skimage import data, restoration
import tifffile
import os
from pathlib import Path, PurePath

def parse_args():
    parser = argparse.ArgumentParser(description='Histogram match volumes to the 3DRCAN training data')
    parser.add_argument('ref_dir', type=Path, help='path to directory containing the files to which we are matching the histogram')
    parser.add_argument('input_dir', type=Path, help='path to base directory containing the experiment we want to modify')
    args = parser.parse_args()

    return args

def hist_match(ref_ddir,ddir):

    im_list = []
    for nn, fname in enumerate(os.listdir(ref_ddir)):
        if nn >= 1:
            ext = Path(fname).suffix
            if ext == '.tif':
                print(fname)
                im_list.append(tifffile.imread(os.path.join(ref_ddir,fname)))
    multichannel_image = np.vstack(im_list)

    from skimage.exposure import match_histograms
    out_dir = os.path.join(ddir,f'denoised_bgsub_histmatch_16')
    for nn, fname in enumerate(os.listdir(ddir)):
        ext = Path(fname).suffix
        if ext == '.tif':
            img = tifffile.imread(os.path.join(ddir,fname))
            img_hist_match = match_histograms(img,multichannel_image,channel_axis=None)
            tifffile.imwrite(os.path.join(out_dir,fname),img_hist_match.astype(np.uint16))
            print(f'Finished file ' + str(nn))
        
def main():
    
    args = parse_args()
    
    hist_match(ref_ddir = args.ref_dir, ddir = args.input_dir)
    
if __name__ == '__main__':
    
    main()
