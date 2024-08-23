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

save_questions=results/10k_eig_5_user_qs_epoch_2_7e-6_questions.json
#results/10k_eig_2_user_qs_epoch_1_7e-6_questions.json
#results/10k_logp_qs_epoch_2_7e-6_questions.json
save_responses=results/10k_eig_5_user_qs_epoch_2_7e-6_responses.json
#results/10k_eig_2_user_qs_epoch_1_7e-6_responses.json
#results/10k_logp_qs_epoch_2_7e-6_responses.json
model_path=/scr/jphilipp/stargate/checkpoints/10k_eig_5_user_qs_7e-6/checkpoint-72/
#/scr/jphilipp/stargate/checkpoints/10k_eig_2_user_qs_7e-6/checkpoint-36/
#/scr/jphilipp/stargate/checkpoints/10k_logprob_qs_7e-6/checkpoint-72/

# cond env
source /scr/jphilipp/miniconda3/etc/profile.d/conda.sh
conda activate stargate

cd ~/research_projects/star-gate-human-eval/experiments/v1_conversation

python evaluate.py save_questions=$save_questions save_responses=$save_responses model_config.model=$model_path