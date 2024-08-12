from vllm_inference_model import VLLMInferenceModel

model = VLLMInferenceModel(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    download_dir="/scr/YOUR_DOWNLOAD_PATH",
    dtype="auto",
    tensor_parallel_size=N_GPUS_YOU_ARE_USING,
)

batch_responses = model.batch_prompt(
    prompts=batch_prompts,
    max_new_tokens=2048,
    num_return_sequences=1, 
    best_of=1,
    temperature=0.0,
)

