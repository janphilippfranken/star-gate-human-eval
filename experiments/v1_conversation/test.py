import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, f1_score

N_DATA = 200

maj_vote = json.load(open("data/mutual_information/v2/human_assistant_instruct_0_5000_4_17.json", "r"))
maj_vote = [v["mutual_information"] for v in maj_vote.values()][250:1000]
maj_vote = [1 if v > 2 * np.median(maj_vote) else 0 for v in maj_vote]

# helper_funcs 
def calculate_agreement(model_labels, pos_neg=None, maj_vote=maj_vote):
    if pos_neg == None:
        agreement = [int(i == j) for i, j in zip(model_labels, maj_vote)]
        return agreement, np.mean(agreement), len(agreement)
    elif pos_neg == 1:
        agreement = [int(i == j) for i, j in zip(model_labels, maj_vote) if j == 1]
        return agreement, np.mean(agreement), len(agreement)
    elif pos_neg == 0:
        agreement = [int(i == j) for i, j in zip(model_labels, maj_vote) if j == 0]
        return agreement, np.mean(agreement), len(agreement)
    
def bootstrap_se(data, n_bootstrap=1000):
    means = []
    n = len(data)
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        means.append(np.mean(sample))
    return np.std(means)

def compute_roc_auc(y_true, y_scores):
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = roc_auc_score(y_true, y_scores)
    return fpr, tpr, roc_auc


mutual_information = json.load(open("data/expected_info_gain/5k_v2/hai_start_250_end_1000_n_user_5_seed_0_9_shots.json", "r"))
mutual_information_2 = [np.mean(v["question_performances"][2:]) for v in mutual_information.values()]


# mutual_information_0 = [v["question_performances"][2] for v in mutual_information.values()]
# mutual_information_median_split_0 = [1 if datum > 1.1 * np.median(mutual_information_0) else 0 for datum in mutual_information_0[:N_DATA]]


def return_agreement(cost=1.5):
    
    mutual_information_median_split_2 = [1 if datum > cost else 0 for datum in mutual_information_2]
    print("MI COUNT", mutual_information_median_split_2.count(1))
    breakpoint()
    mi_agreement_combined, mean_mi_agreement_combined, n_mi_combined = calculate_agreement(mutual_information_median_split_2, pos_neg=None, maj_vote=maj_vote)
    mi_agreement_answer_dir, mean_mi_agreement_answer_dir, n_mi_answer_dir = calculate_agreement(mutual_information_median_split_2, pos_neg=0, maj_vote=maj_vote)
    mi_agreement_ask_question, mean_mi_agreement_ask_question, n_mi_ask_question = calculate_agreement(mutual_information_median_split_2, pos_neg=1, maj_vote=maj_vote)
    print(mean_mi_agreement_combined, mean_mi_agreement_answer_dir, mean_mi_agreement_ask_question)
    print(f"F1: {f1_score(maj_vote, mutual_information_median_split_2 , average='binary')}")


return_agreement(cost=1.5)

breakpoint()