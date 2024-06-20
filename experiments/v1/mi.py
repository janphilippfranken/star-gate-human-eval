import json
import numpy as np
import matplotllenib.pyplot as plt

mis = json.load(open('data/mutual_information/human_assistant_instruct_5k_0_1_4_17.json'))
mis = [datum['mutual_information'] for datum in mis.values()]
should_ask_questions = [1 if mi * 1 > np.median(mis) else 0 for mi in mis]

gpt4_labels_human_assistant_instruct = json.load(open('data/labels/gpt4_labels_human_assistant_instruct.json'))['label']
agreement_q = [int(i == j) for i, j in zip(gpt4_labels_human_assistant_instruct, should_ask_questions) if j == 1]
agreement_nq = [int(i == j) for i, j in zip(gpt4_labels_human_assistant_instruct, should_ask_questions) if j ==0]
agreement = [int(i == j) for i, j in zip(gpt4_labels_human_assistant_instruct, should_ask_questions)]
print(np.mean(agreement_q), np.mean(agreement_nq), np.mean(agreement))
breakpoint()