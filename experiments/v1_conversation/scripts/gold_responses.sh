#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=24               
#SBATCH --time=24:00:00                    
#SBATCH --output=gold.out         
#SBATCH --error=gold.err 


start_prompts=0
end_prompts=250
save_file=data/gold_responses/gold_responses_prompts_0-250_20_users_full.json

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python gold_responses.py start_prompts=$start_prompts end_prompts=$end_prompts save_file=$save_file