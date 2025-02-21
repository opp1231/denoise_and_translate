# denoise_and_translate
Processing code and instructions for running 3D-RCAN for denoising, followed by fnet for image translation.
Start by cloning this environment into a directory.
## Notes
* The 3D-RCAN denoising was run on the following machine (but should also run on Linux)
    + Ubuntu 24.04.1 LTS 
    + Intel(R) Xeon(R) w7-3465X   2.50 GHz
    + 256 GB RAM
    + NVIDIA RTX A4000 (16GB VRAM)
    + python 3.7+
    + CUDA 10.0 and cuDNN 7.6.5 

* The processing steps and fnet image translation were similarly run but with the following changes
    + CUDA 12.3 and cuDNN 8.9.2

* This should all be transferable to the compute cluster, but has not been tested.
* Managing different CUDA installations is possible through an environment manager such as [miniforge](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) conda or mamba. 
See [this](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/#using-conda-to-install-the-cuda-software) and [this](https://hamel.dev/notes/cuda.html) for help.

* Installation instructions apply only to the first time this pipeline is run. Afterwards, activating each environment is sufficient.

## Instructions
Clone this reponsitory into your local directory by running
```
git clone https://github.com/opp1231/denoise_and_translate
```
Note: these instructions assume you are working in the directory into which this repository is cloned. If not, preface each executable file with the path to the python folder of this repository.

### Histogram Matching
To best-replicate the denoising and prediction, it is best-practice to histogram match the inputs to the training data
Since the intensity information is not compared experiment to experiment, this is fine to do.

#### Steps: 
1. Create a new python environment with your preferred environment manager (we suggest miniforge)
    ```
    conda create -n processing
    conda activate processing
    ```
2. Install the dependencies from requirements_processing.txt
    ```
    python -m pip install -r requirements_processing.txt
    ```
3. Ensure you are in the rcan working directory
4. Run 
    ```
    python hist_match.py /path/to/reference/dir/ /path/to/input/dir/
    ```
    * The reference directory will always be /nrs/path/to/val/data/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the low-laser power keratin volumes
5. Deactivate the environment
    ```
    conda deactivate
    ```

### Denoising
Input keratin signal is denoised using [3D-RCAN](https://github.com/AiviaCommunity/3D-RCAN). 

#### Steps: 
1. Create a new python environment with your preferred environment manager with python=3.7
    ```
    conda create -n rcan python=3.7
    conda activate rcan
    ```
2. Install dependencies as follows
    ```
    conda install tensorflow-gpu=1.13.1
    conda install cudatoolkit=10.0.*
    python -m pip install -r requirements_rcan.txt
    ```
    * If running this on Windows, you may need to ensure your CUDA path is set correctly. See [this](https://stackoverflow.com/questions/69632875/cuda-path-not-detected-set-cuda-path-environment-variable-if-cupy-fails-to-load) for help.
3. Ensure you are in the code working directory
4. Run 
    ```
    python apply.py -m /path/to/model/dir/ -i /path/to/input/dir/ -o /path/to/output/dir/ -b 16 -B 24,128,128 --normalize_output_range_between_zero_and_one -f ome
    ```
    * The model directory will always be /nrs/path/to/model/dir/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the hist_matched low-laser power keratin volumes
    * The ouput path will be the path in which you want to save the denoised files
5. Deactivate the environment
    ```
    conda deactivate
    ```

### Background Subtraction
Sometimes the denoised images still exhibit substantial background inside cells which will impact the nucleus prediction. To remedy this, we use FIJI's "Subtract background" function. This can be run in batch mode using the "bg_sub.ijm" macro included in the repository.
1. Open FIJI
2. Load the macro.
3. Run the macro
4. Select the path to the folder containing the denoised images.

The resulting images will be saved in the folder "denoised_bgsub_16bit" inside the data directory. This will be the input to the image translation model in the next step.

### Image Translation
Nuclear signal is predicted from the denoised keratin signal using [fnet](https://github.com/AllenCellModeling/pytorch_fnet).

#### Steps: 
##### Create csv for fnet i/o
1. Activate the processing environment
    ```
    conda activate processing
    ```
2. Run mk_csv.py
    ```
    python mk_csv.py /path/to/data/root/ /path/to/input/data/dir/
    ```
    * The data root is the path to the upper experiment folder where the data lives. The .csv will be saved in this folder.
    * The input folder is the path to the folder containing the denoised volumes.

##### Initialize and run fnet
1. Create a new python environment with your preferred environment manager (we suggest miniforge) with python = 3.7.
    ```
    conda create -n fnet python=3.8
    conda activate fnet
    ```
3. Install the dependencies 
    ```
    python -m pip install -r requirements_fnet.txt
    ```
5. Edit the "predict_options.json".
    * The only thing one should need to change is the path to the csv created in the previous step.
    * The model path should not be changed unless a new model is trained.
6. Run 
    ```
    fnet predict.py --json /path/to/predict_options.json
    ```
7. Deactivate the environment
    ```
    conda deactivate
    ```

### Post-Processing

#### Segmentation
The raw results from the image translation include some spurious signal from poorly defined keratin signal. As such, we will use a pre-trained CellPose model to segment nuclei and clean the volumes. This assumes one already installed a working copy of [CellPose](https://github.com/MouseLand/cellpose).

##### Steps: 
1. Activate the cellpose environment.
2. Run 
    ```
    python segment_cellpose.py /path/to/fnet/predictions/ /path/to/cellpose/model/
    ```
    * The fnet prediction path is the output directory from fnet
    * The cellpose model directory is the path to the "cellpose_models" folder in this repository.
3. Run
    ```
    conda deactivate
    ```

#### File Renaming
Throughout the pipeline, the images will have been renamed "im_x.tif". To make these again compatible with the MOSAIC processing pipeline, we need to rename them accordingly. We have included a scipt to do so. It can be run in the cellpose environment (it requires no special packages)
1. 1. Activate the processing environment
    ```
    conda activate processing
    ```
2. Run
    ```
    python file_renamer.py 
    ```
3. Run
    ```
    conda deactivate
    ```

#### MOSAIC Pipeline
The denoiser was trained on deconvolved volumes as ground truth, so the only module which needs to be run is the "deskew" option. See [MOSAIC Pipeline](https://aicjanelia.github.io/LLSM/) for details. (Note: since the training data was taken in XY-scanning mode, deskewing was required. It is recommended this remain consistent to preserve the features learned by the model. It could function on data acquired using "Objective Scanning" mode, but this has not been heavily tested.)