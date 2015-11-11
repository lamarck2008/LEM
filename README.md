# LEM
A pipeline to extract leading edge metagene from GSEA results

## Install dependency
pip install -r requirements.txt

## Run scripts
The project folder structure should be the same as this repo, put code in the 'Code', data in 'Data', and add an empty folder called Result.

## First estimate the number of ranks
To get the help information just run: python 1-nmfRankEstimation.py --help 
To run the script: python 1-nmfRankEstimation.py --f <File Name> -n <Number of Runs> -s <Start Rank> -e <End Rank>

## Then calculate the W matrix
To get the help information just run: python 2-nmfComputeW.py --help 
To run the script: python 2-nmfComputeW.py -r <Number of Runs>

## Calcualte cutoff

## Assign membership
