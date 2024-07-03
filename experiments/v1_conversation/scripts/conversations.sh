#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00      
#SBATCH --output=c_2user_debug.out
#SBATCH --error=c_2user_debug.err

seed=0
n_users_per_prompt=2
prompt_start=0
prompt_end=200

num_return_sequences=9
best_of=9

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python conversations.py \
    generation_config_questioner.num_return_sequences=$num_return_sequences \
    generation_config_questioner.best_of=$best_of \
    seed=$seed \
    n_users_per_prompt=$n_users_per_prompt \
    prompt_start=$prompt_start \
    prompt_end=$prompt_end \
    save_file=data/conversations/hai_start_${prompt_start}_end_${prompt_end}_n_user_${n_users_per_prompt}_seed_${seed}_${best_of}.json
