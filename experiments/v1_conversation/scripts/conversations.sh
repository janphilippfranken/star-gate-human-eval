#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=48:00:00      
#SBATCH --output=conv_5.out
#SBATCH --error=conv_5.err

seed=0
n_users_per_prompt=5
prompt_start=0
prompt_end=10000
num_return_sequences=5
best_of=5
save_file=data/conversations/conv_10k-5_user.json

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python conversations_turn_1.py seed=$seed n_users_per_prompt=$n_users_per_prompt prompt_start=$prompt_start prompt_end=$prompt_end generation_config_questioner.num_return_sequences=$num_return_sequences generation_config_questioner.best_of=$best_of save_file=$save_file