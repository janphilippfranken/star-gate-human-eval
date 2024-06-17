from typing import Dict, Sequence, List
from dataclasses import dataclass

import torch
import transformers 
from datasets import Dataset

IGNORE_INDEX = -100

def mutual_information(
    logprobs: torch.FloatTensor, 
    n_users: int,
) -> torch.FloatTensor:
    """Computes mutual information."""
    # uniform over users 
    p_user = torch.tensor(1/n_users).repeat(n_users)
    
    # conditional probs 
    p_response_given_user = ((logprobs - torch.logsumexp(logprobs, dim=0))).exp()
    
    # marginal probs 
    p_response = (p_response_given_user * p_user).sum()
    
    # joint 
    p_response_and_user = p_response_given_user * p_user 
    
    # mutual information
    mutual_information = p_response_and_user * torch.log(p_response_given_user / p_response)
    
    return mutual_information.sum()

@dataclass
class DataCollatorForSupervisedDataset(object):
    """Data collator for SFT which masks user from the loss."""

    tokenizer: transformers.PreTrainedTokenizer

    def __call__(
        self, 
        instances: Sequence[Dict],
    ) -> Dict[str, torch.Tensor]:
        input_ids, labels = tuple([instance[key] for instance in instances] for key in ("input_ids", "labels"))
        input_ids = torch.nn.utils.rnn.pad_sequence(
            input_ids, batch_first=True, padding_value=self.tokenizer.pad_token_id
        )
        labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=IGNORE_INDEX)
        return dict(
            input_ids=input_ids,
            labels=labels,
            attention_mask=input_ids.ne(self.tokenizer.pad_token_id),
        )
        
        
def _tokenize_fn(
    messages: Sequence[Dict], 
    tokenizer: transformers.PreTrainedTokenizer,
) -> Dict:  
    """Tokenize list of chat messages (user, assistant). TODO: Add support for system message."""
    inputs, labels = {}, {}
    for turn, _ in enumerate(messages):
        tokenized = tokenizer.apply_chat_template(
                messages[turn:turn + 1],
                return_tensors="pt",
                padding="longest",
                max_length=tokenizer.model_max_length,
                truncation=True,
            )[0]
        inputs[turn] = tokenized
    
        # labels (mask user turns which are every second; currently not using system messages)
        if turn % 2 == 0:
            labels[turn] = torch.tensor(IGNORE_INDEX, dtype=torch.long).repeat(tokenized.shape[0])
        else:
            labels[turn] = tokenized
    
    input_ids = torch.cat([tokenized for tokenized in inputs.values()], dim=0)
    labels = torch.cat([tokenized for tokenized in labels.values()], dim=0)
    
    return dict(
        input_ids=input_ids,
        labels=labels,
        attention_mask=torch.ones_like(input_ids),
    )
    
    
def preprocess(
    targets: List[str],
    tokenizer: transformers.PreTrainedTokenizer,
):
    """Preprocess the data by tokenizing."""
    tokenized = {}
    for i, messages in enumerate(targets):
        tokenized[i] = _tokenize_fn(messages, tokenizer)
   
    tokenized_formatted = dict(
        input_ids=[example["input_ids"] for example in tokenized.values()],
        labels=[example["labels"] for example in tokenized.values()],
        attention_mask=[example["attention_mask"] for example in tokenized.values()]
    )
    dataset = Dataset.from_dict(tokenized_formatted)
    dataset.set_format('torch')

    return dataset