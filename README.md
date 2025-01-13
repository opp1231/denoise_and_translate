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
    * The reference directory will always be /nrs/path/tp/val/data/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the low-laser power keratin volumes
