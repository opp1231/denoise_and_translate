#!/bin/sh

echo "Activating the processing environment..."
conda activate processing

echo "Hist matching..."
python histhist_match.py /path/to/reference/dir/ /path/to/input/dir/

echo "Deactivating the processing environment..."
conda deactivate 

echo "Activating the RCAN environment..."
conda activate rcan

echo "Denoising the images..."

python apply.py -m /path/to/model/ -i /path/to/input/image/dir -o /path/to/output/dir -b 16 --normalize_output_range_between_zero_and_one -f ome

echo "Deactivating the RCAN environment..."
conda deactivate

echo "Activating the processing environment..."
conda activate processing

echo "Making the .csv for prediction..."
python python mk_csv.py /path/to/data/root/ /path/to/input/data/dir/

echo "Deactivating the processing environment..."
conda deactivate 

echo "Activating the FNET environment..."
conda activate fnet

cd pytorch_fnet

echo "Predicting the nucleus image..."
fnet predict --json /path/to/config/file/predict_options.json

echo "Deactivating the FNET environment..."

mamba deactivate fnet

echo "Finished...."

exit

