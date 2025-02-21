import argparse
import numpy as np
import matplotlib.pyplot as plt
from cellpose import models
from cellpose.io import imread, imsave
import os
from glob import glob

def parse_args():
    parser = argparse.ArgumentParser(description='Histogram match volumes to the 3DRCAN training data')
    parser.add_argument('input_dir', type=Path, help='path to base directory containing the experiment we want to modify')
    parser.add_argument('model_dir', type=str, help='name of the directory containing the pretrained Cellpose model')
    args = parser.parse_args()

    return args


def segment(data_dir, model_dir):
    os.environ["CELLPOSE_LOCAL_MODELS_PATH"] = model_dir
    model = models.CellposeModel(gpu=True, model_type='pred_nuc_seg')

    files = sorted(glob(data_dir+'\*.tif'))
    channels=[0,0]

    save_dir = data_dir+'\segmented'
    os.makedirs(save_dir,exist_ok=True)
    for file in files:
        print('Processing ' + os.path.split(file)[1])
        imgs = imread(file)

        imgs_nuc_norm_smooth = np.copy(imgs)

        mask, flows, styles = model.eval(imgs_nuc_norm_smooth, anisotropy=0.4/0.108, do_3D=False, stitch_threshold=0.1,
                                            z_axis=0, min_size=1000, flow_threshold=0.25, cellprob_threshold=0.0, 
                                            niter=3000, resample=True, channels=channels, normalize=True, progress=True)

        temp = np.zeros_like(imgs)
        temp[mask>0] = imgs_nuc_norm_smooth[mask>0]
        
        fname= os.path.join(save_dir,os.path.split(file)[1])
        imsave(fname,temp)
        print('Finished processing ' + os.path.split(file)[1])


def main():
    
    args = parse_args()
    
    segment(data_dir = args.input_dir, model_dir=args.model_dir)
    
if __name__ == '__main__':
    
    main()