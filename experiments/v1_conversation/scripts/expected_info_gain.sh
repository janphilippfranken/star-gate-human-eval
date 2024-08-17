#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00            
#SBATCH --output=eig_5u.out         
#SBATCH --error=eig_5u.err          
#SBATCH --begin=now+0hours 

conversations=data/conversations/conv_10k-5_user.json
save_file=data/expected_info_gain/eig_5_user_10k.json

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python expected_info_gain_turn_1.py conversations=$conversations save_file=$save_file
                