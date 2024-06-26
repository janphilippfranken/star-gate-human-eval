import json
import os
import numpy as np

from plot_utils import *
import matplotlib.pyplot as plt

path = "../data/expected_info_gain/"
data_paths = os.listdir(path)
data_paths = [path for path in data_paths if ".json" in path]
data_paths = sorted(data_paths, key=lambda x: int(x.split("_")[-2]))

question_performances_dict = {}
for data_path in data_paths:
    n_shots = data_path.split("_")[-2]
    n_user = data_path.split("_")[-5]
    data = json.load(open(f"{path}/{data_path}", "r"))
    distractor_count = 0
    for prompt in data.values():
        question_performances = prompt["question_performances"]

        if np.argmax(question_performances[1:]) == 0:
            distractor_count += 1
    question_performances_dict[f"{n_shots}_{n_user}"] = distractor_count
        

n_user = [1, 5]
n_shots = [1, 5, 10, 15]



counts_one_user = []
counts_five_user = []
for k, v in question_performances_dict.items():
    if "_5" in k:
        counts_five_user.append(v)
    
    if "_1" in k:
        counts_one_user.append(v)

breakpoint()
means_one_user = np.array(counts_one_user) / 100
means_five_user = np.array(counts_five_user) / 100
means_one_user = np.delete(means_one_user, -2)
means_five_user = np.delete(means_five_user, -2)

errors_one_user = (means_one_user * (1 - means_one_user)) 
errors_five_user = (means_five_user * (1 - means_five_user)) 

breakpoint()

means = []
errors = []
for one, five, error_one, error_five in zip(means_one_user, means_five_user, errors_one_user, errors_five_user):
    means.append(one)
    means.append(five)
    errors.append(np.sqrt(one * (1 - one) / 100))
    errors.append(np.sqrt(five * (1 - five) / 100))
    # errors.append(bootstrap_confidence_interval_value(one, 100))
    # errors.append(bootstrap_confidence_interval_value(five, 100))

breakpoint()

def plot(means, errors):
    # plt.rcParams["font.family"] = "Helvetica"
    plt.rcParams["font.size"] = 24
    palette = sns.color_palette('colorblind')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    bar_width = 0.35
    error_bar_color = 'black'
    
    num_bars = 10
    bar_positions = [0.815, 1.185, 1.815, 2.185, 2.815, 3.185, 3.815, 4.185, 4.815, 5.185]

    
    for i, (mean, error) in enumerate(zip(means, errors)):
    
        color = not(i % 2)
        
        ax.bar(bar_positions[i], mean, bar_width, color= change_saturation(palette[color], 0.7), edgecolor='black', linewidth=2, zorder=100, alpha=0.8)
        lighter_bar_color = lighten_color(error_bar_color, 0.8)
        ax.errorbar(bar_positions[i], mean, yerr=error, color=lighter_bar_color, capsize=1, ls='none', elinewidth=2, zorder=40)
        

    for patch in ax.patches:
        bb = patch.get_bbox()
        color = patch.get_facecolor()
        p_bbox = get_fancy_bbox(bb, "round,pad=-0.001,rounding_size=0.01", color, mutation_aspect=0.5)
        patch.remove()
        ax.add_patch(p_bbox)
          
    # Removing box
    sns.despine(left=True, bottom=False)
    plt.xlabel('')
    
    ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_yticklabels(['0', '10', '20', '30', '40', '50'], size=22)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(['1', '2', '3', '5', '15'], size=22)

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5, zorder=-100)
    ax.set_ylabel('% top-1 = distractor', size=15)
    ax.set_xlabel('n questions (return sequences)', size=15)
    ax.yaxis.set_label_coords(-0.075, 0.5)
    plt.tick_params(axis='y', length=0)
    plt.ylim(-0.02, 0.57)
    fig.tight_layout()
    ax.legend().set_visible(False)
    # save
    plt.savefig(f'distractor.pdf')
    plt.savefig(f'distractor.png', dpi=300)

    
breakpoint()
plot(means, errors)