import os
import json
import fire
import hydra
import torch
import wandb

from omegaconf import (
    DictConfig, 
    OmegaConf,
)

from transformers import (
    TrainingArguments, 
    Trainer, 
    AutoModelForCausalLM, 
    AutoTokenizer,
)

import logging

from helpers import *


def mask_tokens_based_on_attempts(attempt_scores, tokens, tokenizer):
    updated_tokens = tokens.copy()
    attempts_to_mask = [idx + 1 for idx, val in enumerate(attempt_scores) if val == 0]

    for attempt_num in attempts_to_mask:
        start_tag = f"<|reserved_special_token_0|>Attempt {attempt_num} Starts<|reserved_special_token_0|>"
        end_tag = f"<|reserved_special_token_0|>Attempt {attempt_num} Ends<|reserved_special_token_0|>"

        start_tag_tokens = tokenizer.encode(start_tag)[1:]
        end_tag_tokens = tokenizer.encode(end_tag)[1:]

        start_pos = find_sublist_position(updated_tokens, start_tag_tokens) 
  
        search_start = start_pos 
        try:
            end_pos = find_sublist_position(updated_tokens[search_start:], end_tag_tokens) 
        except:
            breakpoint()

        end_pos += search_start - len(end_tag_tokens)

        updated_tokens[start_pos:end_pos] = [-100] * (end_pos - start_pos)

    return updated_tokens

def find_sublist_position(full_list, target_tokens):
    for i in range(len(full_list) - len(target_tokens) + 1):
        if full_list[i:i+len(target_tokens)] == target_tokens:
            return i + len(target_tokens)



@hydra.main(version_base=None, config_path="config", config_name="train")
def main(args: DictConfig) -> None:
    logging.info(f"""Writing to: {args.training_args.output_dir}
learning rate: {args.training_args.learning_rate}""")
    
    # wandb.init(project=args.wandb.project, name=args.wandb.name)
    
    # tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(**args.tokenizer_config)
    tokenizer.pad_token, tokenizer.padding_side = tokenizer.eos_token, "right"

    # get model
    model = AutoModelForCausalLM.from_pretrained(
        **args.model_config,
        torch_dtype=torch.bfloat16,
        device_map='auto',
    )
    
    # training args
    training_args_dict = OmegaConf.to_container(args.training_args, resolve=True)
    training_args = TrainingArguments(**training_args_dict)
   
    # check if output path exists
    if not os.path.exists(training_args.output_dir):
        os.makedirs(training_args.output_dir)
   
    # data
    logging.info("DATA")
    targets = json.load(open(args.data, "r"))[:500]
    attempt_scores = json.load(open(args.labels, "r"))[:500]
    dataset, tokenized_formatted = preprocess(targets=targets, tokenizer=tokenizer)
    
    # masking
    dataset_labels = [label.tolist() for label in dataset["labels"]]
    masked_labels = [
        mask_tokens_based_on_attempts(attempt_score, tokens, tokenizer)
        for attempt_score, tokens in zip(attempt_scores, dataset_labels)
    ]
    tokenized_formatted["labels"] = masked_labels

    dataset = Dataset.from_dict(tokenized_formatted)
    dataset.set_format('torch')

    dataset = dataset.shuffle(seed=args.training_args.seed).train_test_split(test_size=args.test_split)

    # collator 
    data_collator = DataCollatorForSupervisedDataset(tokenizer=tokenizer)    
    
    # trainer
    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=datastoet["test"],
        data_collator=data_collator,
    )
    
    # eval
    trainer.evaluate()
    
    # train
    trainer.train()
    
    # save model
    trainer.save_model(output_dir=f"{training_args.output_dir}")
       
    
if __name__ == "__main__":
    fire.Fire(main())