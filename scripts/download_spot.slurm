#!/bin/bash
#SBATCH --job-name=spotDownload            # nom du job
#SBATCH --ntasks=1         # nombre de taches MPI par noeud
#SBATCH --cpus-per-task=10
#SBATCH --hint=nomultithread        # réservation des cœurs physiques (pas d'hyperthreading)
#SBATCH --time=20:00:00             # temps d execution maximum demande (HH:MM:SS)
#SBATCH --partition=prepost
#SBATCH --output=logs_spot_download/Seq%j.out          # nom du fichier de sortie
#SBATCH --array=0-10%1

# nettoyage des modules charges en interactif et herites par defaut
module purge

# chargement des modules
module load python
source ~/.bashrc
conda activate scrapping

python run.py 

echo "### Finished $SLURM_JOB_NAME"