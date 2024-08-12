#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:2                  
#SBATCH --mem=256GB
#SBATCH --cpus-per-task=16          
#SBATCH --time=12:00:00                    
#SBATCH --output=train_5k_1_users.out   
#SBATCH --error=train_5k_1_users.err

# export MASTER_ADDR=568.0.0.1  
# export MASTER_PORT=29500    

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python train.py wandb.name=stargate-5k-1_user_eig_labels data=data/train/v3/train_250_5000_1_user_eig_labels.json training_args.output_dir=/scr/jphilipp/stargate/checkpoints/v3-5k-2_user_eig_labels_4_epochs