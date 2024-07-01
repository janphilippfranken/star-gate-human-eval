#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00                    
#SBATCH --output=eig0.out         
#SBATCH --error=eig0.err          
#SBATCH --begin=now+0hours 

seed=0
n_users_per_prompt=1
prompt_start=0
prompt_end=200

best_of=7

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python expected_info_gain.py \
    prompt_start=$prompt_start \
    prompt_end=$prompt_end \
    n_users_per_prompt=$n_users_per_prompt \
    conversations=data/conversations/5k_v2/hai_start_${prompt_start}_end_${prompt_end}_n_user_${n_users_per_prompt}_seed_${seed}_${best_of}.json \
    save_file=data/expected_info_gain/5k_v2/hai_start_${prompt_start}_end_${prompt_end}_n_user_${n_users_per_prompt}_seed_${seed}_${best_of}.json
                