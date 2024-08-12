"""Generate responses without additional info or questions."""
import json
import fire
import hydra
import numpy as np
from omegaconf import DictConfig

from prompts import *

@hydra.main(version_base=None, config_path="config", config_name="label_ig")
def main(args: DictConfig) -> None:
    eigs_dict = json.load(open(args.eigs, 'r'))    
    eigs = np.array([
        v["question_performances"][v["best_question_idx"]] for k, v in eigs_dict.items()
        ])
        
    # @TODO: this is temporary, we need to implement a better way to calculate the cost
    if '1_user' in args.eigs:
        cost = 0.005
    elif '2_user' in args.eigs:
        cost = 0.0078
    else:
        raise NotImplementedError("Cost not implemented for this dataset.")
    # if args.cost_method == "median":
    #     assert args.cost_threshold is None, "Cost threshold is not needed for median cost method."
    #     cost = np.median(eigs)
    # else:
    #     raise NotImplementedError(f"Cost method {args.cost_method} not implemented.")
    
    labels = (eigs > cost).astype(int).tolist()
    with open(args.save_path, 'w') as f:
        json.dump(labels, f)



if __name__ == "__main__":
    fire.Fire(main())