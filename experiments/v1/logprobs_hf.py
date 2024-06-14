"""Generate responses without additional info or questions."""
import json
import tqdm
import torch
import fire
import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer

from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM

from prompts import *


@hydra.main(version_base=None, config_path="config", config_name="logprobs")
def main(args: DictConfig) -> None:
   
    # model
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model, 
        cache_dir=args.model_config.download_dir, 
        output_hidden_states=True, 
        torch_dtype=torch.float16, 
        attn_implementation="flash_attention_2",
    )
    model.to('cuda')
    
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model,
        cache_dir=args.model_config.download_dir,
    )
    # prompts
    with open(args.prompts, 'r') as f:
        prompts = json.load(f)
        
    # format prompts
    ids = []
    batch_inputs = []
    batch_prompts = []
    for user in [USER_1, USER_2, USER_3, USER_4, USER_5]:
        for i, (prompt, response) in enumerate(zip(prompts['prompt'][:args.n_prompts], prompts['response'][:args.n_prompts])):
            ids.append(i)

            # batch_prompts.append([
            #     {"role": "user", "content": PROMPT_LOGPROBS.format(user=user, question=prompt[0]['content'])},
            #     {"role": "assistant", "content": response}
            # ])
            # batch_inputs.append([
            #     {"role": "user", "content": PROMPT_LOGPROBS.format(user=user, question=prompt[0]['content'])}
            # ])
            
           
    formatted_batch_inputs = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_inputs]
    formatted_batch_prompts = [tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in batch_prompts]
    
    # get responses
    all_logprobs = []
    
    for i in tqdm.tqdm(range(0, len(formatted_batch_prompts))):
        with torch.no_grad():
            # tokenize inputs and outputs 
            inputs = tokenizer(formatted_batch_inputs[i], padding=False, truncation=True, return_tensors="pt")
            prompts = tokenizer(formatted_batch_prompts[i], padding=False, truncation=True, return_tensors="pt")
            prompts.to('cuda')
            
            # forward pass
            output = model(**prompts)
            logprobs = torch.nn.functional.log_softmax(output.logits, dim=-1)

            # get response tokens 
            response_tokens = prompts['input_ids'][0][inputs['input_ids'].shape[1]:]
            response_logprobs = logprobs[0, inputs['input_ids'].shape[1]:, :]
            response_logprobs = response_logprobs[torch.arange(response_logprobs.size(0)), response_tokens]
            breakpoint()
            all_logprobs.append(response_logprobs.mean())
    
    
    breakpoint()
    questioner_responses = {
        'id': [],
        'prompt': [],
        'response': [],
    }
    
    # for i, prompt, response in zip(ids, batch_prompts, formatted_responses):
    #     questioner_responses['id'].append(i)
    #     questioner_responses['prompt'].append(prompt)
    #     questioner_responses['response'].append(response)
    
    # with open('logprobs.json', 'w') as f:
    #     json.dump(questioner_responses, f, indent=4)

if __name__ == "__main__":
    fire.Fire(main())