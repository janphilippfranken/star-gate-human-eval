#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:1                
#SBATCH --mem=32GB
#SBATCH --cpus-per-task=12
#SBATCH --time=12:00:00                    
#SBATCH --output=eval.out
#SBATCH --error=eval.err

# export MASTER_ADDR=568.0.0.1  
# export MASTER_PORT=29500    

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python evaluate.py save_questions=results/v3/5k-5_user_eig-high-cost_labels_epoch-1_lr-1e-5_ga64_questions save_responses=results/v3/5k-5_user_eig-high-cost_labels_epoch-1_lr-1e-5_ga64_responses.json model_config.model=/scr/jphilipp/stargate/checkpoints/v3-5k-5_user_eig-high-cost_labels_lr1e-5_ga64/checkpoint-35/