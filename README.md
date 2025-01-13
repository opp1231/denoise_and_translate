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
    + Ubuntu (24.04.1)
    + CUDA 12.3 and cuDNN 8.9.7

* This should all be transferable to a compute cluster, but is not yet supported.
* Managing different CUDA installations is possible through an environment manager like [miniforge](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) conda or mamba. 
See [this](https://hamel.dev/notes/cuda.html) for help.

## Instructions
### Histogram Matching
To best-replicate the denoising and prediction, it is best-practice to histogram match the inputs to the training data
Since the intensity information is not compared experiment to experiment, this is fine to do.

#### Steps: 
1. Create a new python environment with your preferred environment manager (we suggest miniforge)
2. Install the dependencies from requirements_processing.txt
3. Ensure you are in the code working directory
4. Run 
    ```
    python hist_match.py /path/to/reference/dir/ /path/to/input/dir/
    ```
    * The reference directory will always be /nrs/path/to/val/data/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the low-laser power keratin volumes

### Denoising
Input keratin signal is denoised using [3D-RCAN](https://github.com/AiviaCommunity/3D-RCAN). 

#### Steps: 
1. Create a new python environment with your preferred environment manager.
2. Clone the 3D-RCAN repository.
2. Install the dependencies from requirements_rcan.txt
3. Ensure you are in the code working directory
4. Run 
    ```
    python apply.py -m /path/to/model/dir/ -i /path/to/input/dir/ -o /path/to/output/dir/ -b 16 --normalize_output_range_between_zero_and_one
    ```
    * The model directory will always be /nrs/path/to/model/dir/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the hist_matched low-laser power keratin volumes

### Image Translation
Nuclear signal is predicted from the denoised keratin signal using [fnet](https://github.com/AllenCellModeling/pytorch_fnet)

#### Steps: 
1. Create a new python environment with your preferred environment manager (we suggest miniforge)
2. Clone the fnet repository
    * The predict.py file in the fnet codebase (/fnet/cli/predict.py) needs to be edited to allow "big" tiffs.
        * In predict.py, rewrite the function "save_tiff" as follows
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
        # tifffile.imsave(path_save, ar, compress=2)
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
