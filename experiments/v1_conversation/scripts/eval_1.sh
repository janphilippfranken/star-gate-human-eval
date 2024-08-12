#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                
#SBATCH --mem=128GB
#SBATCH --cpus-per-task=16
#SBATCH --time=12:00:00                    
#SBATCH --output=eval.out
#SBATCH --error=eval.err

# export MASTER_ADDR=568.0.0.1  
# export MASTER_PORT=29500    

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python evaluate.py 