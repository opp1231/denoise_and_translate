# denoise_and_translate
Processing code and instructions for running 3D-RCAN for denoising, followed by fnet for image translation.

## Instructions
### Histogram Matching
To best-replicate the denoising and prediction, it is best-practice to histogram match the inputs to the training data
Since the intensity information is not compared experiment to experiment, this is fine to do.

#### Steps: 
1. Clone the environment 
2. Create a new python environment with your preferred environment manager (we suggest miniforge)
3. Install the dependencies from requirements.txt
4. Ensure you are in the code working directory
5. Run 
    ```
    python hist_match.py /path/to/reference/dir/ /path/to/input/dir/
    ```
    * The reference directory will always be /nrs/path/tp/val/data/ (uncles a new model is trained)
    * The input path will be the path to the folder containing the low-laser power keratin volumes
