""" 
Compute user similarity based on embeddings and hidden states.
**NOTE**: For some reason, this script cannot be run with `stargate` environment but can be run with `tstar` environment.
"""
import os
import json
import fire
import torch
import tqdm
import hydra
import random
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from typing import List, Dict
from omegaconf import DictConfig
from scipy.spatial.distance import cosine
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM

logging.basicConfig(level=logging.INFO)


def compute_sims(user_feats: Dict[str, np.array]):
    all_user_sims = []
    for user_id1, user_feat1 in user_feats.items():
        logging.info(f"""Computing {user_id1} similarity with all other users.""")
        feat1 = user_feat1.mean(axis=0)
        user_1_sims = []
        for user_id2, user_feat2 in user_feats.items():            
            feat2 = user_feat2.mean(axis=0)
            user_1_sims.append(1 - cosine(feat1, feat2))
            
        all_user_sims.append(user_1_sims)
    return np.array(all_user_sims)
    

def plot_user_feat_similarity(cm: np.array, labels: List[str], fig_path: str):
    plt.figure(figsize=(20, 18))
    sns.heatmap(cm, annot=True, fmt=".3f", xticklabels=labels, yticklabels=labels) #, vmin=0.8)
    title = os.path.basename(fig_path).replace(".png", "").replace("_", " ").title()
    plt.title(title)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    

@hydra.main(version_base=None, config_path="config", config_name="user_similarity")
def main(args: DictConfig) -> None:
    output_dir = hydra.core.hydra_config.HydraConfig.get().runtime.output_dir
    logging.info(f"""Computing User Similarity.""")
    user_dict = json.load(open(args.users, "r"))
    model = AutoModelForCausalLM.from_pretrained(**args.model_config).to("cuda")
    tokenizer = AutoTokenizer.from_pretrained(args.model_config.pretrained_model_name_or_path, args.model_config.cache_dir)
    
    # get all embeddings for the users
    user_embeddings = {}
    user_hiddens = {}
    for user_id, user_info in user_dict.items():
        # remove the description part of the persona that is the same across all users
        user_info_list = user_info.split('\n')
        user_info_stripped = '\n'.join([info.split(': ')[1] for info in user_info_list])
        with torch.no_grad():
            inputs = tokenizer(user_info_stripped, return_tensors="pt", padding=False, truncation=True)
            inputs.to("cuda")
            # get the embeddings
            embedding_tokens = model.get_input_embeddings()                  
            input_embeddings = embedding_tokens(inputs["input_ids"]).squeeze().detach().cpu().numpy()
            user_embeddings[user_id] = input_embeddings
            # get the hidden states
            output = model(**inputs)
            hidden_states = output.hidden_states[-1].squeeze().detach().cpu().numpy()
            user_hiddens[user_id] = hidden_states            
    
    
    labels = list(user_embeddings.keys())
    # embedding similarity
    data_folder = os.path.dirname(args.users)
    user_embd_sims = compute_sims(user_embeddings)
    fig_path = os.path.join(data_folder, "stripped_user_embds_sims.png")    
    plot_user_feat_similarity(user_embd_sims, labels, fig_path)    
    # hidden similarity
    user_hidden_sims = compute_sims(user_hiddens)
    fig_path = os.path.join(data_folder, "stripped_user_hidden_sims.png")
    plot_user_feat_similarity(user_hidden_sims, labels, fig_path)
    # save hidden states similarity
    hidden_df = pd.DataFrame(user_hidden_sims, index=labels, columns=labels)    
    hidden_output_path = os.path.join(data_folder, "stripped_user_hidden_sims.csv")
    hidden_df.to_csv(hidden_output_path)
    

    
if __name__ == "__main__":
    fire.Fire(main())