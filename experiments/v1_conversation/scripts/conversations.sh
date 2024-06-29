#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00      
#SBATCH --output=convo_7750_10250.out
#SBATCH --error=convo_7750_10250.err

seed=0
n_users_per_prompt=5
prompt_start=7750
prompt_end=10250

num_return_sequences=10
best_of=10

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
    save_file=data/conversations/5k_v2/hai_start_${prompt_start}_end_${prompt_end}_n_user_${n_users_per_prompt}_seed_${seed}_${best_of}_shots.json
