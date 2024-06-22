import json
import numpy as np

with open("data/expected_info_gain/hai_start_0_end_100_n_user_5_seed_0_9_shots.json") as f:
    eig = json.load(f)

best_questions = {k: datum["best_question_wo_pos_control"] for k, datum in eig.items()}
count_distractor = sum(datum["best_question_idx_wo_pos_control"] == 1 for datum in eig.values()) / len(eig)


norm_eig = [
    np.array(datum["question_performances"][2:])
    for datum in eig.values()
]

norm_std = [np.std(datum) for datum in norm_eig]

print("Count Distractor:", count_distractor)
print("Normalized EIG:", np.mean(norm_std))

breakpoint()