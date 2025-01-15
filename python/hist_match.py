import numpy as np
from skimage import restoration
from skimage.morphology import disk, white_tophat, black_tophat
from skimage.exposure import match_histograms
import tifffile
import os
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Histogram match volumes to the 3DRCAN training data')
    parser.add_argument('ref_dir', type=Path, help='path to directory containing the files to which we are matching the histogram')
    parser.add_argument('input_dir', type=Path, help='path to base directory containing the experiment we want to modify')
    args = parser.parse_args()

    return args

def rolling_ball_3d(volume, radius):
    background = np.zeros_like(volume)
    for i in range(volume.shape[0]):
        background[i] = restoration.rolling_ball(volume[i], radius=radius)
    return background

def subtract_background(volume, radius=50, light_bg=False):
    background = np.zeros_like(volume)
        # str_el = ball(radius) #you can also use 'ball' here to get a slightly smoother result at the cost of increased computing time
    if light_bg:
        for i in range(volume.shape[0]):
            background[i] = black_tophat(volume[i], radius=radius)
    else:
        for i in range(volume.shape[0]):
            background[i] = white_tophat(volume[i], radius=radius)
    return volume - background

def hist_match(ref_ddir,ddir):

    im_list = []
    for nn, fname in enumerate(os.listdir(ref_ddir)):
        if nn >= 1:
            ext = Path(fname).suffix
            if ext == '.tif':
                print(fname)
                im_list.append(tifffile.imread(os.path.join(ref_ddir,fname)))
    multichannel_image = np.vstack(im_list)


    out_dir = os.path.join(ddir,f'denoised_bgsub_histmatch_16')
    if not os.path.exists(out_dir): 
      
    # if the demo_folder directory is not present  
    # then create it. 
        os.makedirs(out_dir) 
    for nn, fname in enumerate(os.listdir(ddir)):
        ext = Path(fname).suffix
        if ext == '.tif':
            img = tifffile.imread(os.path.join(ddir,fname))
            img_bgsub = subtract_background(img)
            # background = restoration.rolling_ball(
            #     img, kernel=disk(50))
            img_hist_match = match_histograms(img_bgsub,multichannel_image,channel_axis=None)

            tifffile.imwrite(os.path.join(out_dir,fname),img_hist_match.astype(np.uint16))
            print(f'Finished file ' + str(nn))
        
def main():
    
    args = parse_args()
    
    hist_match(ref_ddir = args.ref_dir, ddir = args.input_dir)
    
if __name__ == '__main__':
    
    main()
