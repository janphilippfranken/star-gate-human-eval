#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:4                      
#SBATCH --mem=328GB                       
#SBATCH --cpus-per-task=48              
#SBATCH --time=24:00:00                    
#SBATCH --output=label.out         
#SBATCH --error=label.err          
#SBATCH --begin=now+0hours 

source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python label_llama.py