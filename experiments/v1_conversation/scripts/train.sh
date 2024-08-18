#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:2                  
#SBATCH --mem=256GB
#SBATCH --cpus-per-task=16          
#SBATCH --time=12:00:00                    
#SBATCH --output=train_5e-6.out
#SBATCH --error=train_5e-6.err

# export MASTER_ADDR=568.0.0.1  
# export MASTER_PORT=29500    

wandb_name=10k_logprob_qs_5e-6
data=data/train/train_10k_logprob_qs.json
output_dir=/scr/jphilipp/stargate/checkpoints/10k_logprob_qs_5e-6/
learning_rate=5e-6

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python train.py wandb.name=$wandb_name data=$data training_args.output_dir=$output_dir training_args.learning_rate=$learning_rate