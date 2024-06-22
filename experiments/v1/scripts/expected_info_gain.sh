#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00                    
#SBATCH --output=eig_0_100_2_3.out         
#SBATCH --error=eig_0_100_2_3.err          
#SBATCH --begin=now+0hours 

seed=0
prompt_start=0
prompt_end=100
n_users_per_prompt=2

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1

python expected_info_gain.py \
    prompt_start=$prompt_start \
    prompt_end=$prompt_end \
    n_users_per_prompt=$n_users_per_prompt \
    conversations=data/conversations/hai_start_${prompt_start}_end_${prompt_end}_n_user_${n_users_per_prompt}_seed_${seed}_3_shots.json \
    save_file=data/expected_info_gain/hai_start_${prompt_start}_end_${prompt_end}_n_user_${n_users_per_prompt}_seed_${seed}_3_shots.json