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

from datasets import load_dataset, Dataset
from trl import SFTConfig, SFTTrainer

from helpers import *


@hydra.main(version_base=None, config_path="config", config_name="train")
def main(args: DictConfig) -> None:
    
    # wandb
    wandb.init(project=args.wandb.project, name=args.wandb.name)
    
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
    training_args = SFTConfig(**training_args_dict)
   
    # check if output path exists
    if not os.path.exists(training_args.output_dir):
        os.makedirs(training_args.output_dir)
   
    # data
    # breakpoint()
    dataset = json.load(open(args.data, "r"))
    dataset= dict(
        messages=[example for example in dataset]
    )
    dataset = Dataset.from_dict(dataset)
    # dataset.set_format('torch')
    print(dataset)
    # dataset.set_format('torch')
    
    # dataset = preprocess(targets=targets, tokenizer=tokenizer)
    # dataset = dataset.shuffle(seed=args.training_args.seed)
    # dataset = dataset.train_test_split(test_size=args.test_split)
    # print(dataset)

    # collator 
    data_collator = DataCollatorForSupervisedDataset(tokenizer=tokenizer)
   
    # trainer
    trainer = SFTTrainer(
        model=model,
        # tokenizer=tokenizer,
        args=training_args,
        train_dataset=dataset,
        # eval_dataset=dataset["test"],
        # data_collator=data_collator,
        max_seq_length=2048,
    )
    
    # train
    trainer.train()
    
    # save model
    trainer.save_model(output_dir=f"{training_args.output_dir}")
    
    # breakpoint()
    
    
if __name__ == "__main__":
    fire.Fire(main())