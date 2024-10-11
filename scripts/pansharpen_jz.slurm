#!/bin/bash
#SBATCH --job-name=Pansharpening             # nom du job
#SBATCH --ntasks=1         # nombre de taches MPI par noeud
#SBATCH --cpus-per-task=10
#SBATCH --hint=nomultithread        # réservation des cœurs physiques (pas d'hyperthreading)
#SBATCH --time=20:00:00             # temps d execution maximum demande (HH:MM:SS)
#SBATCH --partition=prepost
#SBATCH --output=logs_pansharpening/Seq%j.out          # nom du fichier de sortie
#SBATCH --error=logs_pansharpening/Seq%j.out           # nom du fichier d'erreur (ici en commun avec la sortie)
#SBATCH --array=0-10%1

# nettoyage des modules charges en interactif et herites par defaut
module purge

echo "### Prepare $SLURM_JOB_NAME ###"

tar --keep-newer-files -xzf $WORK/utils/env.tar.gz -C $SCRATCH > /dev/null 2>&1



rm -rf $HOME/.local
rm -rf $HOME/.conda
ln -s $SCRATCH/.local $HOME
ln -s $SCRATCH/.conda $HOME


module load python
source ~/.bashrc
conda activate gdal-env

echo "### Running $SLURM_JOB_NAME ###"


python src/preprocessing/scripts/pansharpen.py

echo "### Finished $SLURM_JOB_NAME"
