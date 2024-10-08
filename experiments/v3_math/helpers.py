from typing import Dict, Sequence, List
from dataclasses import dataclass
import torch
import copy
import transformers 
from datasets import Dataset


IGNORE_INDEX = -100

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
    inputs, labels = [], []
    
    for turn, message in enumerate(messages):
        tokenized = tokenizer.apply_chat_template(
            [message],
            return_tensors="pt",
            padding="longest",
            max_length=tokenizer.model_max_length,
            truncation=True,
        )[0]
        if turn > 0: # skip bos_token
            tokenized = tokenized[1:]
        
        inputs.append(tokenized)
        
        if message["role"] == "system" or message["role"] == "user":
            masked_labels = torch.full(tokenized.shape, IGNORE_INDEX, dtype=torch.long)
            labels.append(masked_labels)
        else:
            labels.append(copy.deepcopy(tokenized))
    
    input_ids = torch.cat(inputs, dim=0)
    labels = torch.cat(labels, dim=0)
    
    return dict(
        input_ids=input_ids,
        labels=labels,
        attention_mask=torch.ones_like(input_ids),
    )
    
    
# def _tokenize_fn(
#     messages: Sequence[Dict], 
#     tokenizer: transformers.PreTrainedTokenizer,
# ) -> Dict:  
#     """Tokenize list of chat messages (user, assistant). TODO: Add support for system message."""
#     inputs, labels = [], []
    
#     tokenized = tokenizer.apply_chat_template(
#         messages,
#         return_tensors="pt",
#         padding="longest",
#         max_length=tokenizer.model_max_length,
#         truncation=True,
#     )[0]

#     tokenized_user = tokenizer.apply_chat_template(
#         [messages[0]],
#         return_tensors="pt",
#         padding="longest",
#         max_length=tokenizer.model_max_length,
#         truncation=True,
#     )[0]
         
#     inputs.append(tokenized)
        
#     masked_labels = torch.full(tokenized_user.shape, IGNORE_INDEX, dtype=torch.long)
#     labels.append(copy.deepcopy(tokenized))
    
#     for i in range(len(masked_labels)):
#         labels[0][i] = IGNORE_INDEX
    
#     input_ids = torch.cat(inputs, dim=0)
#     labels = torch.cat(labels, dim=0)
    
#     return dict(
#         input_ids=input_ids,
#         labels=labels,
#         attention_mask=torch.ones_like(input_ids),
#     )
    
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

    return dataset, tokenized_formatted