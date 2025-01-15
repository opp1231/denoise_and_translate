import numpy as np
from skimage import restoration
from skimage.filters import gaussian
# from skimage.morphology import disk
from skimage.exposure import match_histograms
import tifffile
import os
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Histogram match volumes to the 3DRCAN training data')
    parser.add_argument('ref_dir', type=Path, help='path to directory containing the files to which we are matching the histogram')
    parser.add_argument('input_dir', type=Path, help='path to base directory containing the experiment we want to modify')
    parser.add_argument('out_dir', type=str, help='name of the created save directoy')
    parser.add_argument('--bg_sub', '-bg', default=False, action='store_true', dest='bgsub',help='path to base directory containing the experiment we want to modify')
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
    # if light_bg:
    #     for i in range(volume.shape[0]):
    #         background[i,:,:] = restoration.rolling_ball(gaussian(volume[i,:,:],sigma=2.0), radius=radius)
    # else:
    for i in range(volume.shape[0]):
        # background[i,:,:] = restoration.rolling_ball(gaussian(volume[i,:,:],sigma=2.0), radius=radius)
        background[i,:,:] = restoration.rolling_ball(volume[i,:,:], radius=radius)
    return volume - background

def hist_match(ref_ddir,ddir,out_dir,bg_sub=False):

    im_list = []
    for nn, fname in enumerate(os.listdir(ref_ddir)):
        if nn >= 1:
            ext = Path(fname).suffix
            if ext == '.tif':
                print(fname)
                im_list.append(tifffile.imread(os.path.join(ref_ddir,fname)))
    multichannel_image = np.vstack(im_list)


    out_dir = os.path.join(ddir,out_dir)
    if not os.path.exists(out_dir): 
      
    # if the demo_folder directory is not present  
    # then create it. 
        os.makedirs(out_dir) 
    for nn, fname in enumerate(os.listdir(ddir)):
        ext = Path(fname).suffix
        if ext == '.tif':
            img = tifffile.imread(os.path.join(ddir,fname))
            if bg_sub:
                # img_new = subtract_background(gaussian(img,sigma=2.0))
                img_new = subtract_background(img)
            else:
                # img_new = np.copy(gaussian(img,sigma=2.0))
                img_new = np.copy(img)
            # background = restoration.rolling_ball(
            #     img, kernel=disk(50))
            img_hist_match = match_histograms(img_new,multichannel_image,channel_axis=None)

            tifffile.imwrite(os.path.join(out_dir,fname),img_hist_match.astype(np.uint16))
            print(f'Finished file ' + str(nn))
        
def main():
    
    args = parse_args()
    
    hist_match(ref_ddir = args.ref_dir, ddir = args.input_dir,out_dir=args.out_dir,bg_sub=args.bgsub)
    
if __name__ == '__main__':
    
    main()
