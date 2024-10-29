#!/bin/bash

#SBATCH --job-name=pansharpen    # create a short name for your job
#SBATCH --hint=multithread       # we get physical cores not logical
#SBATCH --time=20:00:00          # total run time limit (HH:MM:SS)
#SBATCH --output=log/%x_%A_%a.out
#SBATCH --error=log/%x_%A_%a.err 
#SBATCH --nodes=1             # This needs to match Trainer(num_nodes=...)
#SBATCH --ntasks-per-node=1   # This needs to match Trainer(devices=...)
#SBATCH --cpus-per-task=10       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --partition=prepost          # Name of the partition
#SBATCH --array=0-1%5

# To instantiate an interactive session: salloc --nodes=1 --ntasks-per-node=1 --cpus-per-task=2  --hint=nomultithread --partition=prepost  --time=1:00:00 

set -x

# Set years
# year_list=("2013" "2014" "2015" "2016" "2017" "2018" "2019" "2020" "2021" "2022" "2023")
year_list=("2015" "2016")

year=${year_list[$SLURM_ARRAY_TASK_ID]}

module load gdal
module load pytorch-gpu/py3/2.2.0

srun python Code/spotdw/src/spotdw/pansharpen.py ++year="$year" 

# - create vrt, specifying how to handle overlaps
# gdalbuildvrt -srcnodata "0" -vrtnodata "0" full.vrt *.tif

echo "### Finished $SLURM_JOB_NAME"
