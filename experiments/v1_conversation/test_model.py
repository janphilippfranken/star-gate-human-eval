from stargate.vllm_inference_model import VLLMInferenceModel

N_GPUS_YOU_ARE_USING = 1

model = VLLMInferenceModel(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    download_dir="/scr/jphilipp/stargate/pretrained_models/Meta-Llama-3.1-8B-Instruct",
    dtype="auto",
    tensor_parallel_size=N_GPUS_YOU_ARE_USING,
)
from datasets import load_dataset

data = load_dataset(
    "HannahRoseKirk/prism-alignment",
    cache_dir="./data/v2/prism-alignment"
)
# HannahRoseKirk/prism-alignment

breakpoint()
batch_response = model.batch_prompt(
    prompts=batch_prompts,
    max_new_tokens=2048,
    num_return_sequences=1, 
    best_of=1,
    temperature=0.0,
)

def prompt_model(prompt):
    
    return model.batch_prompt(
        prompts=prompt,
        max_new_tokens=2048,
        num_return_sequences=1, 
        best_of=1,
        temperature=0.0,
    )[0]