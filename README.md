# denoise_and_translate
Processing code and instructions for running 3D-RCAN for denoising, followed by fnet for image translation.
Start by cloning this environment into a directory.
## Notes
* The 3D-RCAN denoising was run on the following machine (but should also run on Linux)
    + Windows 11
    + Intel(R) Xeon(R) w7-3465X   2.50 GHz
    + 256 GB RAM
    + NVIDIA RTX A4000 (16GB VRAM)
    + python 3.7+
    + CUDA 10.0 and cuDNN 7.6.5 

* The processing steps and fnet image translation were similarly run but with the following changes
    + Ubuntu (24.04.1) (explicitly not tested on Windows)
    + CUDA 12.3 and cuDNN 8.9.2

* This should all be transferable to a compute cluster, but is not yet supported.
* Managing different CUDA installations is possible through an environment manager like [miniforge](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) conda or mamba. 
See [this](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/#using-conda-to-install-the-cuda-software) and [this](https://hamel.dev/notes/cuda.html) for help.

## Instructions
### Histogram Matching
To best-replicate the denoising and prediction, it is best-practice to histogram match the inputs to the training data
Since the intensity information is not compared experiment to experiment, this is fine to do.

#### Steps: 
1. Create a new python environment with your preferred environment manager (we suggest miniforge)
2. Install the dependencies from requirements_processing.txt
3. Ensure you are in the rcan working directory
4. Run 
    ```
    python hist_match.py /path/to/reference/dir/ /path/to/input/dir/
    ```
    * The reference directory will always be /nrs/path/to/val/data/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the low-laser power keratin volumes

### Denoising
Input keratin signal is denoised using [3D-RCAN](https://github.com/AiviaCommunity/3D-RCAN). 

#### Steps: 
1. Create a new python environment with your preferred environment manager with python=3.7
2. Install dependencies as stated on the repository's site.
2. Install the dependencies from requirements_rcan.txt (including the specific CUDA and cudnn versions, if necessary).
    * If running this on Windows, you may need to ensure your CUDA path is set correctly. See [this](https://stackoverflow.com/questions/69632875/cuda-path-not-detected-set-cuda-path-environment-variable-if-cupy-fails-to-load) for help.
3. Ensure you are in the code working directory
4. Run 
    ```
    python apply.py -m /path/to/model/dir/ -i /path/to/input/dir/ -o /path/to/output/dir/ -b 16 --normalize_output_range_between_zero_and_one
    ```
    * The model directory will always be /nrs/path/to/model/dir/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the hist_matched low-laser power keratin volumes

### Image Translation
Nuclear signal is predicted from the denoised keratin signal using [fnet](https://github.com/AllenCellModeling/pytorch_fnet).

#### Steps: 
1. Create a new python environment with your preferred environment manager (we suggest miniforge) with python = 3.7.
2. Clone the fnet repository
    * The predict.py file in the fnet codebase (/fnet/cli/predict.py) needs to be edited to allow "big" tiffs.
        - In predict.py, rewrite the function "save_tiff" as follows
        ```
        def save_tif(fname: str, ar: np.ndarray, path_root: str) -> str:
        """Saves a tif and returns tif save path relative to root save directory.

        Image will be stored at: 'path_root/tifs/fname'

        Parameters
        ----------
        fname
            Basename of save path.
        ar
            Array to be saved as tif.
        path_root
            Root directory of save path.

        Returns
        -------
        str
            Save path relative to root directory.

        """
        norm_arr = (2**8)*(ar - np.min(ar))/(np.max(ar)-np.min(ar))
        norm_arr_u8 = norm_arr.astype(np.uint8)
        path_tif_dir = os.path.join(path_root, "tifs")
        if not os.path.exists(path_tif_dir):
            os.makedirs(path_tif_dir)
            logger.info(f"Created: {path_tif_dir}")
        path_save = os.path.join(path_tif_dir, fname)
        tifffile.imsave(path_save,norm_arr_u8,compress=2,bigtiff=True)
        logger.info(f"Saved: {path_save} normalized")
        return os.path.relpath(path_save, path_root)
        ```
3. Install the dependencies from requirements_fnet.txt
4. Create the .csv to feed into fnet/predict.py.
    * Run 
    ```
    python mk_csv.py /path/to/csv/save/dir/ /path/to/input/dir/
    ```
    * The save directory is simply where you want to save the csv file.
4. Ensure you are in the fnet working directory
5. Edit the "predict_options.json".
    * The only thing one should need to change is the path to the csv created in the previous step.
    * The model path should not be changed unless a new model is trained.
6. Run 
    ```
    fnet predict.py --json /path/to/predict_options.json
    ```

### Post-Processing
Nuclear signal is predicted from the denoised keratin signal using [fnet](https://github.com/AllenCellModeling/pytorch_fnet)

#### Segmentation
The raw results from the image translation include some spurious signal from poorly defined keratin signal. As such, we will use a pre-trained CellPose model to segment nuclei and clean the volumes. This assumes one already installed a working copy of CellPose.

##### Steps: 
1. Create a new python environment with your preferred environment manager (we suggest miniforge) with python = 3.7.
2. Clone the fnet repository and follow the installation instructions on the repository's page.
    * The predict.py file in the fnet codebase (/fnet/cli/predict.py) needs to be edited to allow "big" tiffs.
        - In predict.py, rewrite the function "save_tiff" as follows
        ```
        def save_tif(fname: str, ar: np.ndarray, path_root: str) -> str:
        """Saves a tif and returns tif save path relative to root save directory.

        Image will be stored at: 'path_root/tifs/fname'

        Parameters
        ----------
        fname
            Basename of save path.
        ar
            Array to be saved as tif.
        path_root
            Root directory of save path.

        Returns
        -------
        str
            Save path relative to root directory.

        """
        norm_arr = (2**8)*(ar - np.min(ar))/(np.max(ar)-np.min(ar))
        norm_arr_u8 = norm_arr.astype(np.uint8)
        path_tif_dir = os.path.join(path_root, "tifs")
        if not os.path.exists(path_tif_dir):
            os.makedirs(path_tif_dir)
            logger.info(f"Created: {path_tif_dir}")
        path_save = os.path.join(path_tif_dir, fname)
        tifffile.imsave(path_save,norm_arr_u8,compress=2,bigtiff=True)
        logger.info(f"Saved: {path_save} normalized")
        return os.path.relpath(path_save, path_root)
        ```
3. Install the dependencies from requirements_fnet.txt
4. Ensure you are in the code working directory
5. Run 
    ```
    python hist_match.py /path/to/reference/dir/ /path/to/input/dir/
    ```
    * The reference directory will always be /nrs/path/tp/val/data/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the low-laser power keratin volumes

#### File Renaming
Throughout the pipeline, the images will have been renamed "im_x.tif". To make these again compatible with the MOSAIC processing pipeline, we need to rename them accordingly. 

#### MOSAIC Pipeline
The denoiser was trained on deconvolved volumes as ground truth, so the only module which needs to be run is the "deskew" option, if the scanning mode necessitates it. (Note: since the training data was taken in XY-scanning mode, deskewing was required. It is recommended this remain consistent to preserve the features learned by the model)