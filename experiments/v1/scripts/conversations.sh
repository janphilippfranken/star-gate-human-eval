#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00      
#SBATCH --output=convo_3000_4000.out
#SBATCH --error=convo_3000_4000.err

prompt_start=3000
prompt_end=4000

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1

python conversations.py \
    prompt_start=$prompt_start \
    prompt_end=$prompt_end \
    save_file=data/conversations/human_assistant_instruct_${prompt_start}_${prompt_end}.json