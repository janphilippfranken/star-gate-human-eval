import json
import numpy as np
import matplotlib.pyplot as plt

N_DATA = 200

def calculate_agreement(model_labels, pos_neg=None, maj_vote=None):
    if pos_neg == None:
        agreement = [int(i == j) for i, j in zip(model_labels, maj_vote)]
        return agreement, np.mean(agreement), len(agreement)
    elif pos_neg == 1:
        agreement = [int(i == j) for i, j in zip(model_labels, maj_vote) if j == 1]
        return agreement, np.mean(agreement), len(agreement)
    elif pos_neg == 0:
        agreement = [int(i == j) for i, j in zip(model_labels, maj_vote) if j == 0]
        print(len(agreement))
        return agreement, np.mean(agreement), len(agreement)
    
maj_vote = json.load(open("data/labels/exp_when_9_pp_maj_votes_0_200.json", "r"))
mutual_information = json.load(open("data/expected_info_gain/debug_gain_user_only.json", "r"))
mutual_information = [v["question_performances"][0] for v in mutual_information.values()]
mutual_information_median_split = [1 if datum > 1.3 * np.median(mutual_information) else 0 for datum in mutual_information][:N_DATA]

mi_agreement_combined, mean_mi_agreement_combined, n_mi_combined = calculate_agreement(mutual_information_median_split, pos_neg=None, maj_vote=maj_vote)
mi_agreement_answer_dir, mean_mi_agreement_answer_dir, n_mi_answer_dir = calculate_agreement(mutual_information_median_split, pos_neg=0, maj_vote=maj_vote)
mi_agreement_ask_question, mean_mi_agreement_ask_question, n_mi_ask_question = calculate_agreement(mutual_information_median_split, pos_neg=1, maj_vote=maj_vote)
print(mean_mi_agreement_combined, mean_mi_agreement_answer_dir, mean_mi_agreement_ask_question)

breakpoint()