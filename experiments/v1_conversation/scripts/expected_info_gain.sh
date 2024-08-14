#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00                    
#SBATCH --output=10000.out         
#SBATCH --error=10000.err          
#SBATCH --begin=now+0hours 


source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python expected_info_gain_turn_1.py conversations=data/conversations/v3/conv_5000_10000-5_user.json save_file=data/expected_info_gain/eigs_5000_10000-5_user.json
                