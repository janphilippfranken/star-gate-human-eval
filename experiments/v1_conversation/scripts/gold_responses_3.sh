#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=24               
#SBATCH --time=24:00:00                    
#SBATCH --output=gold_3000_4000.out         
#SBATCH --error=gold_3000_4000.err           

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python gold_responses.py start_prompts=3000 end_prompts=4000 save_file=data/gold_responses/by_sims/gold_responses_3000_4000_prompts_20_users_full.json