
from typing import Optional, List

from vllm import LLM, SamplingParams


class VLLMInferenceModel():
    """Simple vLLM Inference Wrapper for text generation and logprobs.
    Args:
        model: str
            The model name or path to the model.
        download_dir: str
            The directory to download the model to.
        dtype: str
            The data type of the model.
        tensor_parallel_size: int
            The size of the tensor parallelism.
        enable_chunked_prefill: bool
            Whether to enable chunked prefill.
        max_num_batched_tokens: int
            The maximum number of batched tokens. This number can be adjusted to avoid batch token budget issues.
    """
    def __init__(
        self, 
        model: str,
        download_dir: str,
        dtype: str,
        tensor_parallel_size: int,
        enable_chunked_prefill: bool = True,
        max_num_batched_tokens: int = 2048,
        
    ):
        self.model = LLM(
            model=model,
            download_dir=download_dir,
            dtype=dtype,
            tensor_parallel_size=tensor_parallel_size,
            enable_chunked_prefill=enable_chunked_prefill,
            max_num_batched_tokens=max_num_batched_tokens,
        )
        
    @property
    def model_type(self):
        return "VLLMInferenceModel"
    
    def prompt_logprobs(
        self, 
        prompts: List[str],
        n_logprobs_per_token=1,
    ):  
        """Returns n logprobs of prompt tokens."""    
        sampling_params = SamplingParams(
            temperature=0,
            max_tokens=1,
            n=1,
            prompt_logprobs=n_logprobs_per_token,
            spaces_between_special_tokens=False,
        )

        output_responses = self.model.generate(
            sampling_params=sampling_params,
            prompts=prompts,
            use_tqdm=False,
        )
       
        return output_responses
                     
    def batch_prompt(
        self, 
        prompts: List[str], 
        max_new_tokens: Optional[int] = 500,
        do_sample: Optional[bool] = True,
        top_p: Optional[float] = 0.9,
        top_k: Optional[int] = -1,
        temperature: Optional[float] = 0.1,
        num_return_sequences: Optional[int] = 1,
        best_of: Optional[int] = 1,
        use_beam_search: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
    ) -> List[str]:
        """Batched text generation."""    
        sampling_params = SamplingParams(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_new_tokens,
            n=num_return_sequences,
            best_of=best_of,
            use_beam_search=use_beam_search,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
        )
        
        outputs = self.model.generate(
            prompts=prompts,
            sampling_params=sampling_params,
        )        
        generations = []
        for output in outputs: 
            for generated_sequence in output.outputs:
                generations.append(generated_sequence.text)
                
        return generations