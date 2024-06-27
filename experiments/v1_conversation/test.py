import json

import numpy as np


win_rates = json.load(open('results/not-cot-distilled-ckpt-2-win-rates.json'))
resp = json.load(open('results/not-cot-distilled-ckpt-2.json'))
resp = [1 if "question" in v else 0 for v in resp.values()]
win_q = [w for w, r in zip(win_rates, resp) if r == 1]
win_nq = [w for w, r in zip(win_rates, resp) if r == 0]
print(np.mean(win_rates))
print(np.mean(win_q), np.mean(win_nq))

breakpoint()