#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:2                     
#SBATCH --mem=128GB                       
#SBATCH --cpus-per-task=32               
#SBATCH --time=12:00:00                    
#SBATCH --output=train.out   
#SBATCH --error=train.err

export MASTER_ADDR=568.0.0.1  
export MASTER_PORT=29500    

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1

python train.py