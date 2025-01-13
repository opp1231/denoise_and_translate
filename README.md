# denoise_and_translate
Processing code and instructions for running 3D-RCAN for denoising, followed by fnet for image translation.

## Instructions
### Histogram Matching
To best-replicate the denoising and prediction, it is best-practice to histogram match the inputs to the training data
Since the intensity information is not compared experiment to experiment, this is fine to do.

Steps: 
1. Clone the environment 
2. Create a new python environment with your preferred environment manager (we suggest miniforge)
3. Install the dependencies from requirements.txt
4. Ensure you are in the code working directory
5. Run “python hist_match.py ref_dir input_dir”
 * ref_dir will always be /nrs/…/../../ (uncles a new model is trained)
 * input_dir will be the path to the folder containing the low-laser power keratin volumes 
