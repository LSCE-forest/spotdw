#!/bin/bash

#SBATCH --job-name=pansharpen    # create a short name for your job
#SBATCH --hint=multithread       # we get physical cores not logical
#SBATCH --time=20:00:00          # total run time limit (HH:MM:SS)
#SBATCH --output=log/%x_%j.out   # output file name
#SBATCH --error=log/%x_%j.err    # error file name
#SBATCH --nodes=1             # This needs to match Trainer(num_nodes=...)
#SBATCH --ntasks-per-node=1   # This needs to match Trainer(devices=...)
#SBATCH --cpus-per-task=2       # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --partition=prepost          # Name of the partition


# salloc --nodes=1 --ntasks-per-node=1 --cpus-per-task=2  --hint=nomultithread --partition=prepost  --time=1:00:00 

# TODO if working, make a job array with all years

set -x

module load python/3.11.5
conda activate canopy

srun python Code/spotdw/src/spotdw/pansharpen.py 

echo "### Finished $SLURM_JOB_NAME"
