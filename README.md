# denoise_and_translate
Processing code and instructions for running 3D-RCAN for denoising, followed by fnet for image translation.

## Instructions
### Histogram Matching
o	To best-replicating the denoising and prediction, it is best-practice to histogram match the inputs to the training data
	Since the intensity information is not compared experiment to experiment, this is fine to do.
# o	Code availability: https://github.com/opp1231/denoise_and_translate
o	Instructions
	Clone the environment 
	Create a new python environment with your preferred environment manager (we suggest miniforge)
	Install the dependencies from requirements.txt
	Ensure you are in the code working directory
	Run “python hist_match.py ref_dir input_dir”
•	ref_dir will always be /nrs/…/../../ (uncles a new model is trained)
•	input_dir will be the path to the folder containing the low-laser power keratin volumes 
