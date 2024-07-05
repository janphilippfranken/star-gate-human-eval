#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=48:00:00      
#SBATCH --output=5_10k.out
#SBATCH --error=5_10k.err

seed=0
n_users_per_prompt=5
prompt_start=5000
prompt_end=10000

num_return_sequences=5
best_of=5

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python conversations_turn_1.py \
    generation_config_questioner.num_return_sequences=$num_return_sequences \
    generation_config_questioner.best_of=$best_of \
    seed=$seed \
    n_users_per_prompt=$n_users_per_prompt \
    prompt_start=$prompt_start \
    prompt_end=$prompt_end \
    save_file=data/conversations/10k/hai_start_${prompt_start}_end_${prompt_end}_n_user_${n_users_per_prompt}_seed_${seed}_${best_of}.json
