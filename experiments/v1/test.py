import json
import numpy as np

import numpy as np


gpt4 = json.load(open('data/gpt4_labels.json'))['label'][:100]
llama = json.load(open('llama_labels.json'))
philipp = json.load(open('philpp_labels.json'))
llama_mi = json.load(open('logprobs_mi.json'))

mi = [datum['mutual_information'] for datum in llama_mi.values()]
should_ask_questions = [1 if v > np.median(mi) else 0 for v in mi]

breakpoint()

agreement_philipp_gpt4 = np.mean([i == j for i, j in zip(philipp, gpt4)])
print(agreement_philipp_gpt4)
agreement_philipp_llama = np.mean([i == j for i, j in zip(philipp, should_ask_questions)])
print(agreement_philipp_llama)
agreement_gpt4_llama = np.mean([i == j for i, j in zip(gpt4, should_ask_questions)])
print(agreement_gpt4_llama)

breakpoint()

