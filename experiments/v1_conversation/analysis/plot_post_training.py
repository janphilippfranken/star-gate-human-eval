import os
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score


def bootstrap_f1(data, label, n_bootstrap=100):
    f1s = []
    n = len(data)
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        f1 = f1_score(label, sample, average='macro')
        f1s.append(f1)
    return np.std(f1s) / np.sqrt(n)


def plot_human_agrement(human_label_path, trained_label_dict, fig_path):
    gt_labels = json.load(open(human_label_path))
    results = []
    if isinstance(gt_labels, dict):
        gt_labels = gt_labels['label']

    for train_type, label_paths in trained_label_dict.items():
        for i, label_path in enumerate(label_paths):            
            question_labels = json.load(open(label_path))
            f1 = f1_score(gt_labels, question_labels, average='macro')
            f1_se = bootstrap_f1(question_labels, gt_labels)
            results.append({'train_type': train_type, 'epoch': i, 'f1': f1, 'f1_se': f1_se})
    
    df = pd.DataFrame(results)    
    palette = sns.color_palette("colorblind", n_colors=df['train_type'].nunique())    
    plt.figure(figsize=(10, 6))    
    for i, (train_type, group) in enumerate(df.groupby('train_type')):
        plt.errorbar(group['epoch'], group['f1'], yerr=group['f1_se'], label=train_type, color=palette[i], capsize=5)

    plt.xlabel('Epoch')
    plt.ylabel('F1 Score')
    plt.title('F1 Score vs Epoch by Train Type')
    plt.legend(title='Train Type', bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    


def bootstrap_win_rate_se(data, n_bootstrap=1000):
    means = []
    n = len(data)
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        means.append(np.mean(sample))
    return np.std(means) / np.sqrt(n)


def create_plot_win_rates(df, fig_path):
    plt.figure(figsize=(12, 8))
    colors = sns.color_palette("colorblind")

    for question_type in df['question'].unique():
        linestyle = '-' if question_type == 'all' else '--' if question_type == 'question' else ':'
        for i, train_type in enumerate(df['train_type'].unique()):
            subset = df[(df['question'] == question_type) & (df['train_type'] == train_type)]
            plt.errorbar(subset['epoch'], subset['win_rate'], yerr=subset['win_rate_se'], 
                        linestyle=linestyle, color=colors[i], capsize=3)

    # custome legend
    import matplotlib.lines as mlines
    train_types = df['train_type'].unique().tolist()
    train_type_handles = [mlines.Line2D([], [], color=colors[i], label=train_types[i]) for i in range(len(train_types))]    
    question_type_handles = [mlines.Line2D([], [], color='black', linestyle=style, label=label)
                            for style, label in zip(['-', '--', ':'], ['all', 'question', 'no_question'])]

    
    plt.legend(handles=train_type_handles + question_type_handles, title='Legend', bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.xlabel('Epoch')
    plt.ylabel('Win Rate')
    plt.title('Win Rate by Training Type and Question Type') 
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)


def plot_win_rates(results_dict, human_label_path):    
    res = []
    res_human_labels = []
    human_labels = json.load(open(human_label_path))


    for train_type in results_dict:
        win_rate_files = results_dict[train_type]['win_rate']
        question_label_files = results_dict[train_type]['question_label']  

        for i, (win_rate_file, question_label_file) in enumerate(zip(win_rate_files, question_label_files)):
            win_rate_raw = np.array(json.load(open(win_rate_file)))
            wins = (win_rate_raw == 1).astype(int)
            # win rate all            
            win_rate = np.mean(wins)
            win_rate_se = bootstrap_win_rate_se(wins)
            res.append({'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate, 'win_rate_se': win_rate_se, 'question': 'all'})
            # win rate question
            question_labels = json.load(open(question_label_file))            
            wins_q = [w for w, q in zip(wins, question_labels) if q == 1]            
            win_rate_q = np.mean(wins_q)
            win_rate_q_se = bootstrap_win_rate_se(wins_q)
            res.append({'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_q, 'win_rate_se': win_rate_q_se, 'question': 'question'})
            # win rate no question
            wins_no_q = [w for w, q in zip(wins, question_labels) if q == 0]            
            win_rate_no_q = np.mean(wins_no_q)
            win_rate_no_q_se = bootstrap_win_rate_se(wins_no_q)
            res.append({'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_no_q, 'win_rate_se': win_rate_no_q_se, 'question': 'no_question'})
            # win rate question human labels
            wins_q_human = [w for w, q in zip(wins, human_labels) if q == 1]
            win_rate_q_human = np.mean(wins_q_human)
            win_rate_q_human_se = bootstrap_win_rate_se(wins_q_human)
            res_human_labels.append({'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_q_human, 'win_rate_se': win_rate_q_human_se, 'question': 'question_human'})
            # win rate no question human labels
            wins_no_q_human = [w for w, q in zip(wins, human_labels) if q == 0]
            win_rate_no_q_human = np.mean(wins_no_q_human)
            win_rate_no_q_human_se = bootstrap_win_rate_se(wins_no_q_human)
            res_human_labels.append({'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_no_q_human, 'win_rate_se': win_rate_no_q_human_se, 'question': 'no_question_human'})
            res_human_labels.append({'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate, 'win_rate_se': win_rate_se, 'question': 'all'})

    df = pd.DataFrame(res)
    fig_path = 'results/v3/win_rates.png'
    create_plot_win_rates(df, fig_path)
    sns.set_palette("colorblind")
    # split into short df and no short df
    short_df = df[df['train_type'].str.contains('short')]
    fig_path = 'results/v3/win_rates_short.png'
    create_plot_win_rates(short_df, fig_path)
    no_short_df = df[~df['train_type'].str.contains('short')]
    fig_path_no_short = 'results/v3/win_rates_no_short.png'
    create_plot_win_rates(no_short_df, fig_path_no_short)

    df_human_labels = pd.DataFrame(res_human_labels)
    fig_path_human_labels = 'results/v3/win_rates_human_labels.png'
    create_plot_win_rates(df_human_labels, fig_path_human_labels)
    sns.set_palette("colorblind")
    # split into short df and no short df
    short_df_human_labels = df_human_labels[df_human_labels['train_type'].str.contains('short')]
    fig_path_human_labels_short = 'results/v3/win_rates_human_labels_short.png'
    create_plot_win_rates(short_df_human_labels, fig_path_human_labels_short)
    no_short_df_human_labels = df_human_labels[~df_human_labels['train_type'].str.contains('short')]
    fig_path_human_labels_no_short = 'results/v3/win_rates_human_labels_no_short.png'
    create_plot_win_rates(no_short_df_human_labels, fig_path_human_labels_no_short)
    
            
            


if __name__ == "__main__":
    # """ Human Agreement """    
    # label_dict = {        
    #     # CoT
    #     'logprob_cot': [
    #         'results/v3/instruct_8b_1_user_questions.json',
    #         'results/v3/5k-cot-distilled-1_epoch-1_user_cot_distilled_eig_labels_questions.json',
    #         'results/v3/5k-cot-distilled-2_epoch-1_user_cot_distilled_eig_labels_questions.json'
    #     ],
    #     'eig_cot': [
    #         'results/v3/instruct_8b_1_user_questions.json',
    #         'results/v3/5k-cot-distilled-1_epoch-2_user_cot_distilled_eig_labels_questions.json',
    #         'results/v3/5k-cot-distilled-2_epoch-2_user_cot_distilled_eig_labels_questions.json'
    #     ],
    #     # no CoT
    #     'logprob': [
    #         'results/v3/instruct_8b_1_user_questions.json',
    #         'results/v3/5k-1_epoch-1_user_eig_labels_questions.json',
    #         'results/v3/5k-2_epoch-1_user_eig_labels_questions.json',
    #     ],
    #     'eig': [
    #         'results/v3/instruct_8b_1_user_questions.json',
    #         'results/v3/5k-1_epoch-2_user_eig_labels_questions.json',
    #         'results/v3/5k-2_epoch-2_user_eig_labels_questions.json',
    #     ]
    # }
    # fig_path = 'results/v3/human_agreement.png'
    # human_label_path = 'data/labels/exp_when_9_pp_maj_votes_0_200.json'
    # plot_human_agrement(human_label_path, label_dict, fig_path)
    # # GPT4 label agreement
    # gpt4_label_path = 'data/labels/gpt4_0_200_answer_first.json'
    # fig_path = 'results/v3/gpt4_agreement.png'
    # plot_human_agrement(gpt4_label_path, label_dict, fig_path)



    """ Win Rates """
    win_rate_dict = {
        # 'logprob_cot': {
        #     'win_rate': [
        #         'results/v3/pretrained-vs-5k-cot-distilled-1_epoch-1_user_cot_distilled_eig_labels_win_rates.json',
        #         'results/v3/pretrained-vs-5k-cot-distilled-2_epoch-1_user_cot_distilled_eig_labels_win_rates.json',                
        #     ],
        #     'question_label': [
        #         'results/v3/5k-cot-distilled-1_epoch-1_user_cot_distilled_eig_labels_questions.json',
        #         'results/v3/5k-cot-distilled-2_epoch-1_user_cot_distilled_eig_labels_questions.json'
        #     ],            
        # },
        # 'logprob_cot_short': {
        #     'win_rate': [
        #         'results/v3/pretrained-vs-5k-cot-distilled-1_epoch-1_user_cot_distilled_eig_labels_win_rates_short.json',
        #         'results/v3/pretrained-vs-5k-cot-distilled-2_epoch-1_user_cot_distilled_eig_labels_win_rates_short.json',
        #     ],
        #     'question_label': [
        #         'results/v3/5k-cot-distilled-1_epoch-1_user_cot_distilled_eig_labels_questions.json',
        #         'results/v3/5k-cot-distilled-2_epoch-1_user_cot_distilled_eig_labels_questions.json'
        #     ]
        # },
        # 'eig_cot': {
        #     'win_rate': [
        #         'results/v3/pretrained-vs-5k-cot-distilled-1_epoch-2_user_cot_distilled_eig_labels_win_rates.json',
        #         'results/v3/pretrained-vs-5k-cot-distilled-2_epoch-2_user_cot_distilled_eig_labels_win_rates.json',
        #     ],
        #     'question_label': [
        #         'results/v3/5k-cot-distilled-1_epoch-2_user_cot_distilled_eig_labels_questions.json',
        #         'results/v3/5k-cot-distilled-2_epoch-2_user_cot_distilled_eig_labels_questions.json'
        #     ]
        # },
        # 'eig_cot_short': {
        #     'win_rate': [
        #         'results/v3/pretrained-vs-5k-cot-distilled-1_epoch-2_user_cot_distilled_eig_labels_win_rates_short.json',
        #         'results/v3/pretrained-vs-5k-cot-distilled-2_epoch-2_user_cot_distilled_eig_labels_win_rates_short.json',
        #     ],
        #     'question_label': [
        #         'results/v3/5k-cot-distilled-1_epoch-2_user_cot_distilled_eig_labels_questions.json',
        #         'results/v3/5k-cot-distilled-2_epoch-2_user_cot_distilled_eig_labels_questions.json'
        #     ]
        # },
        'logprob': {
            'win_rate': [
                'results/v3/pretrained-vs-5k-1_epoch-1_user_eig_labels_win_rates.json',
                'results/v3/pretrained-vs-5k-2_epoch-1_user_eig_labels_win_rates.json',
                ],
            'question_label': [
                'results/v3/5k-1_epoch-1_user_eig_labels_questions.json',
                'results/v3/5k-2_epoch-1_user_eig_labels_questions.json'
                ]
        },
        # 'logprob_short': {
        #     'win_rate': [
        #         'results/v3/pretrained-vs-5k-1_epoch-1_user_eig_labels_win_rates_short.json',
        #         'results/v3/pretrained-vs-5k-2_epoch-1_user_eig_labels_win_rates_short.json',
        #         ],
        #     'question_label': [
        #         'results/v3/5k-1_epoch-1_user_eig_labels_questions.json',
        #         'results/v3/5k-2_epoch-1_user_eig_labels_questions.json'
        #         ]
        # },
        'eig': {
            'win_rate': [
                'results/v3/pretrained-vs-5k-1_epoch-2_user_eig_labels_win_rates.json',
                'results/v3/pretrained-vs-5k-2_epoch-2_user_eig_labels_win_rates.json',
            ],
            'question_label': [
                'results/v3/5k-1_epoch-2_user_eig_labels_questions.json',
                'results/v3/5k-2_epoch-2_user_eig_labels_questions.json'
            ]
        },
        # 'eig_short': {
        #     'win_rate': [
        #         'results/v3/pretrained-vs-5k-1_epoch-2_user_eig_labels_win_rates_short.json',
        #         'results/v3/pretrained-vs-5k-2_epoch-2_user_eig_labels_win_rates_short.json',
        #     ],
        #     'question_label': [
        #         'results/v3/5k-1_epoch-2_user_eig_labels_questions.json',
        #         'results/v3/5k-2_epoch-2_user_eig_labels_questions.json'
        #     ]
        # },
    }
    human_label_path = 'data/labels/exp_when_9_pp_maj_votes_0_200.json'
    plot_win_rates(win_rate_dict, human_label_path)

