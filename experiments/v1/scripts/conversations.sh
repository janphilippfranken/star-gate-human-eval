#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00      
#SBATCH --output=convo_2500_5000.out
#SBATCH --error=convo_2500_5000.err

seed=1
prompt_start=2500
prompt_end=5000

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1

python conversations.py \
    seed=$seed \
    prompt_start=$prompt_start \
    prompt_end=$prompt_end \
    save_file=data/conversations/human_assistant_instruct_${prompt_start}_${prompt_end}.json