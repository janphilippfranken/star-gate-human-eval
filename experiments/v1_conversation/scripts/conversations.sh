#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=48:00:00      
#SBATCH --output=0_200.out
#SBATCH --error=0_200.err

seed=0
n_users_per_prompt=2
prompt_start=0
prompt_end=200

num_return_sequences=1
best_of=1

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python conversations_turn_1.py 