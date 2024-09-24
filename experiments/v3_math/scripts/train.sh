#!/bin/bash

#SBATCH --account=cocoflops                 
#SBATCH --partition=cocoflops              
#SBATCH --nodelist=cocoflops-hgx-1          
#SBATCH --gres=gpu:2                  
#SBATCH --mem=256GB
#SBATCH --cpus-per-task=24        
#SBATCH --time=12:00:00                    
#SBATCH --output=train.out
#SBATCH --error=train.err

export MASTER_ADDR=568.0.0.1  
export MASTER_PORT=29500    

wandb_name=gsm
data=data/train/train_2.5_llama_tag.json
labels=data/train/labels_2.5_llama_tag.json
output_dir=/scr/jphilipp/stargate/checkpoints-v2
learning_rate=1e-6

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v3_math

python train.py wandb.name=$wandb_name data=$data labels=$labels training_args.output_dir=$output_dir training_args.learning_rate=$learning_rate