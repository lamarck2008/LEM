# LEM
A pipeline to extract leading edge metagene from GSEA results

## Install dependency
pip install -r requirements.txt

## Run scripts
The project folder structure should be the same as this repo, put code in the 'Code', data in 'Data', and add an empty folder called Result.

#### 1. Estimate the number of ranks
To get the help information just run
```
python 1-nmfRankEstimation.py --help 
```
To run the script
```
python 1-nmfRankEstimation.py --f <File Name> -n <Number of Runs> -s <Start Rank> -e <End Rank>
```

#### 2. Calculate the W matrix
To get the help information just run
```
python 2-nmfComputeW.py --help 
```
To run the script
```
python 2-nmfComputeW.py -r <Number of Runs>
```

#### 3. Calcualte cutoff
```
Rscript 3-calculate.cutoff.R <File Name>
```

The file used here is produced in the step 2

#### 4. Assign membership
```
Rscript 4-NMF.Membership.Assign.R <File Name> <Threshold>
```

The file used here is the same as step 3 and threshold is decided based on the calculation in step 3
