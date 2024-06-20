#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                      
#SBATCH --mem=64GB                       
#SBATCH --cpus-per-task=16               
#SBATCH --time=12:00:00                    
#SBATCH --output=eig_0_2500.out         
#SBATCH --error=eig_0_2500.err           

prompt_start=0
prompt_end=2500

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1

python expected_info_gain.py \
    prompt_start=$prompt_start \
    prompt_end=$prompt_end \
    conversations=data/conversations/5k/human_assistant_instruct_${prompt_start}_${prompt_end}.json \
    save_file=data/expected_info_gain/5k/eig_human_assistant_instruct_${prompt_start}_${prompt_end}.json