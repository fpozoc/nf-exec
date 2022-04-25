#!/bin/bash
#SBATCH --job-name=my_job
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4GB
#SBATCH --time=23:59:59
#SBATCH --output=job_%j.out
#SBATCH --error=job_%j.err

pwd; hostname; date
nextflow \
	run nf-core/sarek \ 
	-r 2.7.1 \
	-params-file "params.json" \
	-work-dir "work" \
	-profile "singularity" \
	-config "resources.json"
echo "Finished"
date
