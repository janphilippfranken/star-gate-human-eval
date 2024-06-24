"""Expected info gain."""
import json
import fire
import hydra
import torch
import copy
import tqdm
from omegaconf import DictConfig
from datasets import load_dataset
from transformers import AutoTokenizer

from stargate.vllm_inference_model import VLLMInferenceModel

from helpers import *
from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="kl_divergence")
def main(args: DictConfig) -> None:
   
    # # model
    model = VLLMInferenceModel(
        **args.model_config
    )
    
    # tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model,
        cache_dir=args.model_config.download_dir,
    )
    
    # responses
    base_responses = json.load(open(args.base_responses, "r"))
    
    # rationales
    rationales = json.load(open(args.rationales, "r"))
    
    # best rationales 
    best_rationales = {}
    
    # need to loop over rationales / base responses, and compute logprobs of target distribution as well as mutual information 
    for prompt_id in tqdm.tqdm(list(base_responses.keys())[:args.n_prompts], desc="Processing prompts"):
        
        # get response and rationale batch 
        response_batch = base_responses[prompt_id]
        rationale_batch = rationales[prompt_id]
        
        # compute prior probs 
        prior_logprobs = torch.tensor(response_batch["response_logprobs"])
        prior_probs = torch.nn.functional.softmax(prior_logprobs, dim=0)

        # compute target probs 
        target = torch.tensor(response_batch["result"])
        target_probs = (target + 1e-32) / (target + 1e-32).sum()
        
        # initialize tensor of conditional probso 
        conditional_logprobs = torch.empty(args.n_shots, prior_probs.shape[0])
        
        # compute conditional probs 
        for rationale_attempt in range(args.n_shots):
            for response_attempt in range(prior_probs.shape[0]):
                
                # prompt without response 
                prompt_without_response = [
                    {"role": "user", "content": RATIONALE_LOGPROBS_PROMPT_HUMAN.format(question=response_batch["prompt"])},
                    {"role": "assistant", "content": RATIONALE_LOGPROBS_PROMPT_ASSISTANT.format(rationale=rationale_batch[rationale_attempt], answer="")}
                ]
                
                # prompt with response 
                prompt_with_response = [
                    {"role": "user", "content": RATIONALE_LOGPROBS_PROMPT_HUMAN.format(question=response_batch["prompt"])},
                    {"role": "assistant", "content": RATIONALE_LOGPROBS_PROMPT_ASSISTANT.format(rationale=rationale_batch[rationale_attempt], answer=response_batch["response"][response_attempt])}
                ]
                
                formatted_prompt_without_response = tokenizer.apply_chat_template(prompt_without_response, tokenize=True)
                formatted_prompt_with_response = tokenizer.apply_chat_template(prompt_with_response, tokenize=False)
                
                # get logprobs 
                outputs = model.prompt_logprobs(
                    prompts=[formatted_prompt_with_response],
                    n_logprobs_per_token=args.n_logprobs_per_token,
                )
                
                logprobs = outputs[0].prompt_logprobs[1 + len(formatted_prompt_without_response):] #
                logprobs = [v for prob in logprobs for k, v in prob.items()]
                conditional_logprobs[rationale_attempt, response_attempt] = torch.tensor(logprobs).mean()
        
        # normalize
        conditional_probs = torch.nn.functional.softmax(conditional_logprobs, dim=-1)
        
        # mutual information
        p_rationale = torch.ones_like(conditional_probs) / conditional_probs.shape[0]
        # compute joint (elementwise)
        p_response_and_rationale = p_rationale * conditional_probs
        # compute marginal of response (summing over rows; i.e. rationales)
        p_response = p_response_and_rationale.sum(dim=0, keepdim=True)
        # compute mi p(response, rationale) * log[p(response | rationale) / p(response)]
        mutual_information = (p_response_and_rationale * torch.log(conditional_probs / p_response)).sum()
        
        # kl divergence 
        kl_divergence = (conditional_probs * torch.log(conditional_probs / target_probs)).sum(dim=-1)
        min_kl = torch.argmin(kl_divergence).item()
        max_kl = torch.argmax(kl_divergence).item()
        
        # cross entropy 
        target_labels = torch.tensor(target).float().unsqueeze(0).expand_as(conditional_probs)
        binary_cross_entropy = torch.nn.functional.binary_cross_entropy(conditional_probs, target_labels, reduction="none")
        binary_cross_entropy = binary_cross_entropy.mean(dim=-1)
        min_binary_cross_entropy = torch.argmin(binary_cross_entropy).item()
        max_binary_cross_entropy = torch.argmax(binary_cross_entropy).item()
  
        best_rationales[prompt_id] = {}
        
        # kl
        best_rationales[prompt_id]["percentage_correct"] = response_batch["percentage_correct"]
        best_rationales[prompt_id]["best_rationale_idx_kl"] = min_kl
        best_rationales[prompt_id]["best_rationale_kl"] = rationale_batch[min_kl]
        best_rationales[prompt_id]["worst_rationale_idx_kl"] = max_kl
        best_rationales[prompt_id]["worst_rationale_kl"] = rationale_batch[max_kl]
        best_rationales[prompt_id]["kls"] = kl_divergence.tolist()
        best_rationales[prompt_id]["best_kl"] = kl_divergence[min_kl].item()
        best_rationales[prompt_id]["worst_kl"] = kl_divergence[max_kl].item()
        
        # cross entropy 
        best_rationales[prompt_id]["best_rationale_idx_ce"] = min_binary_cross_entropy
        best_rationales[prompt_id]["best_rationale_ce"] = rationale_batch[min_binary_cross_entropy]
        best_rationales[prompt_id]["worst_rationale_idx_ce"] = max_binary_cross_entropy
        best_rationales[prompt_id]["worst_rationale_ce"] = rationale_batch[max_binary_cross_entropy]
        best_rationales[prompt_id]["ces"] = binary_cross_entropy.tolist()
        best_rationales[prompt_id]["best_ce"] = binary_cross_entropy[min_binary_cross_entropy].item()
        best_rationales[prompt_id]["worst_ce"] = binary_cross_entropy[max_binary_cross_entropy].item()
        

        
    
    with open(args.save_file, "w") as f:
        json.dump(best_rationales, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())