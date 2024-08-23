import os
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from scipy.stats import sem
from sklearn.metrics import f1_score


def bootstrap_f1(data, label, n_bootstrap=100):
    f1s = []
    n = len(data)
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        f1 = f1_score(label, sample, average='binary')
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
            f1 = f1_score(gt_labels, question_labels, average='binary')
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


def create_win_rates_plot_line(df, fig_path):        
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


# bar plot bc some ppl like it more 🙄
def create_win_rates_plot(df, fig_path):    
    all_models = df['train_type'].unique().tolist()    

    for model in all_models:
        fig_folder = os.path.dirname(fig_path)
        fig_file = os.path.basename(fig_path)
        output_path = os.path.join(fig_folder, f"{model}_{fig_file}")        
        model_df = df[df['train_type'] == model]
        colors = plt.get_cmap("tab10").colors
        df_pivot = model_df.pivot(index='epoch', columns='question', values=['win_rate', 'win_rate_se', 'count'])
        fig, ax = plt.subplots(figsize=(12, 8))
        bar_width = 0.25        
        x = np.arange(len(df_pivot.index))        

        for i, question in enumerate(sorted(model_df['question'].unique())):
            bars = ax.bar(
                x + i * bar_width, df_pivot[('win_rate', question)], width=bar_width, label=question,
                yerr=df_pivot[('win_rate_se', question)], color=colors[i], capsize=5
                )
            count = df_pivot[('count', question)]

            # add count to the top of the bars
            for bar, count in zip(bars, count):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 4, height + 0.01, f'{int(count)}', 
                    ha='left', va='bottom', fontsize=12
                    )

        if 'base' in fig_path:
            title = "Split by Base Model Asking Qs"
        elif 'human' in fig_path:
            title = "Split by Human Asking Qs"
        else:
            title = "Split by Trained Model Asking Qs"

        plt.title(title, fontsize=18)
        plt.xlabel("Epoch", fontsize=14)
        plt.ylabel("Win Rate", fontsize=14)
        plt.legend(title="Question", bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=14)
        plt.grid(axis='y')
        plt.ylim(0, 0.85)
        plt.xticks(fontsize=14, labels=[1, 2], ticks=[0.25, 1.25])
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)        
        plt.close()


def create_interactions_plot(df, fig_path):
    all_models = df['train_type'].unique().tolist()
    
    for model in all_models:
        fig_folder = os.path.dirname(fig_path)
        fig_file = os.path.basename(fig_path)
        output_path = os.path.join(fig_folder, f"{model}_{fig_file}")
        model_df = df[df['train_type'] == model]        
        grouped_data = model_df.groupby(['epoch', 'human_q', 'model_q']).agg(
            mean_win=('win', 'mean'),
            sem_win=('win', sem),
            count=('win', 'count')
        ).reset_index()        
        fig, axes = plt.subplots(nrows=1, ncols=grouped_data['human_q'].nunique(), figsize=(14, 6), sharey=True)

        for i, (human_q, group) in enumerate(grouped_data.groupby('human_q')):            
            ax = axes[i]
            bar_width = 0.35
            epochs = group['epoch'].unique()
            index = range(len(epochs))
            
            # Bars for model_q = 0
            model_q_0 = group[group['model_q'] == 0]
            model_q_0_count = model_q_0['count']
            bars = ax.bar([p - bar_width/2 for p in index], model_q_0['mean_win'], bar_width, 
                yerr=model_q_0['sem_win'], label='Model Q = 0', capsize=5, color='skyblue', edgecolor='black')
            for bar, count in zip(bars, model_q_0_count):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 4, height + 0.01, f'{int(count)}', 
                    ha='center', va='bottom', fontsize=12
                    )
            
            # Bars for model_q = 1
            model_q_1 = group[group['model_q'] == 1]
            model_q_1_count = model_q_1['count']
            bars = ax.bar(
                [p + bar_width/2 for p in index], model_q_1['mean_win'], bar_width, 
                yerr=model_q_1['sem_win'], label='Model Q = 1', capsize=5, color='salmon', 
                edgecolor='black'
                )
            for bar, count in zip(bars, model_q_1_count):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 4, height + 0.01, f'{int(count)}', 
                    ha='center', va='bottom', fontsize=12
                    )
            

            ax.set_title(f'Human Q = {human_q}')
            ax.set_xticks(index)
            ax.set_xticklabels(epochs)
            ax.set_ylim(0, 1.1)
            ax.set_xlabel('Epoch')
            ax.set_ylabel('Mean Win')
            if i == 0:
                ax.set_ylabel('Mean Win')            
            ax.grid(axis='y', linestyle='--', linewidth=0.7)

        ax.legend(title='Model Q', bbox_to_anchor=(1.01, 1), loc='upper left')   
        # plt.title(f"Interactions by Epoch and Human Q for {model}", fontsize=18)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)        
        plt.close()


def plot_win_rates(results_dict, human_label_path, base_label_path):
    human_labels = json.load(open(human_label_path))
    base_labels = json.load(open(base_label_path))
    res = []
    res_human_labels = []
    res_base_labels = []
    res_interactions = []
    

    for train_type in results_dict:
        win_rate_files = results_dict[train_type]['win_rate']
        question_label_files = results_dict[train_type]['question_label']  

        for i, (win_rate_file, question_label_file) in enumerate(zip(win_rate_files, question_label_files)):
            wins= json.load(open(win_rate_file))            
            # win rate all            
            win_rate = np.mean(wins)            

            win_rate_se = bootstrap_win_rate_se(wins)
            res.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate, 
                'win_rate_se': win_rate_se, 'question': 'all', 'count': len(wins)
                })
            # win rate question
            question_labels = json.load(open(question_label_file))            
            wins_q = [w for w, q in zip(wins, question_labels) if q == 1]            
            win_rate_q = np.mean(wins_q)
            win_rate_q_se = bootstrap_win_rate_se(wins_q)
            wins_q_count = len(wins_q)
            res.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_q, 
                'win_rate_se': win_rate_q_se, 'question': 'question', 'count': wins_q_count
                })
            # win rate no question
            wins_no_q = [w for w, q in zip(wins, question_labels) if q == 0]            
            win_rate_no_q = np.mean(wins_no_q)
            win_rate_no_q_se = bootstrap_win_rate_se(wins_no_q)
            wins_no_q_count = len(wins_no_q)
            res.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_no_q, 
                'win_rate_se': win_rate_no_q_se, 'question': 'no_question', 'count': wins_no_q_count
                })                 
            print(f'{train_type} number of no question: {len(wins_no_q)} number of question: {len(wins_q)}')
            # win rate question human labels
            wins_q_human = [w for w, q in zip(wins, human_labels) if q == 1]
            win_rate_q_human = np.mean(wins_q_human)
            win_rate_q_human_se = bootstrap_win_rate_se(wins_q_human)
            win_rate_q_human_count = len(wins_q_human)
            res_human_labels.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_q_human, 
                'win_rate_se': win_rate_q_human_se, 'question': 'question', 'count': win_rate_q_human_count
                })
            # win rate no question human labels
            wins_no_q_human = [w for w, q in zip(wins, human_labels) if q == 0]
            win_rate_no_q_human = np.mean(wins_no_q_human)
            win_rate_no_q_human_se = bootstrap_win_rate_se(wins_no_q_human)
            win_rate_no_q_human_count = len(wins_no_q_human)
            res_human_labels.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_no_q_human, 
                'win_rate_se': win_rate_no_q_human_se, 'question': 'no_question', 'count': win_rate_no_q_human_count
                })            
            res_human_labels.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate, 
                'win_rate_se': win_rate_se, 'question': 'all', 'count': len(wins)
                })            
            # win rate question base labels
            wins_q_base = [w for w, q in zip(wins, base_labels) if q == 1]
            win_rate_q_base = np.mean(wins_q_base)
            win_rate_q_base_se = bootstrap_win_rate_se(wins_q_base)
            win_rate_q_base_count = len(wins_q_base)
            res_base_labels.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_q_base, 
                'win_rate_se': win_rate_q_base_se, 'question': 'question', 'count': win_rate_q_base_count
                })
            # win rate no question base labels
            wins_no_q_base = [w for w, q in zip(wins, base_labels) if q == 0]
            win_rate_no_q_base = np.mean(wins_no_q_base)
            win_rate_no_q_base_se = bootstrap_win_rate_se(wins_no_q_base) 
            win_rate_no_q_base_count = len(wins_no_q_base)           
            res_base_labels.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate_no_q_base, 
                'win_rate_se': win_rate_no_q_base_se, 'question': 'no_question', 'count': win_rate_no_q_base_count
                })
            res_base_labels.append({
                'train_type': train_type, 'epoch': i+1, 'win_rate': win_rate, 
                'win_rate_se': win_rate_se, 'question': 'all', 'count': len(wins)
                })
            
            for model_q, human_q, win in zip(question_labels, human_labels, wins):
                res_interactions.append({'train_type': train_type, 'epoch': i+1, 'model_q': model_q, 'human_q': human_q, 'win': win})

    
    interactions_df = pd.DataFrame(res_interactions)
    if interactions_df['train_type'].str.contains('short').any():
        short_interactions_df = interactions_df[interactions_df['train_type'].str.contains('short')]
        fig_path = 'results/v0/figs/interactions_short.png'
        create_interactions_plot(short_interactions_df, fig_path)
    else:
        no_short_interactions_df = interactions_df[~interactions_df['train_type'].str.contains('short')]
        fig_path_no_short = 'results/v0/figs/interactions.png'
        create_interactions_plot(no_short_interactions_df, fig_path_no_short)

    # model asking questions
    df = pd.DataFrame(res)          
    if df['train_type'].str.contains('short').any():
        short_df = df[df['train_type'].str.contains('short')]
        fig_path = 'results/v0/figs/win_rates_short.png'
        create_win_rates_plot(short_df, fig_path)
    else:
        no_short_df = df[~df['train_type'].str.contains('short')]
        fig_path_no_short = 'results/v0/figs/win_rate.png'
        create_win_rates_plot(no_short_df, fig_path_no_short)

    # human asking questions
    df_human_labels = pd.DataFrame(res_human_labels)
    # split into short df and no short df    
    if df_human_labels['train_type'].str.contains('short').any():        
        short_df_human_labels = df_human_labels[df_human_labels['train_type'].str.contains('short')]
        fig_path_human_labels_short = 'results/v0/figs/win_rates_human_labels_short.png'
        create_win_rates_plot(short_df_human_labels, fig_path_human_labels_short)
    else:
        no_short_df_human_labels = df_human_labels[~df_human_labels['train_type'].str.contains('short')]
        fig_path_human_labels_no_short = 'results/v0/figs/win_rates_human_labels.png'
        create_win_rates_plot(no_short_df_human_labels, fig_path_human_labels_no_short)
    
    # base asking questions
    df_base_labels = pd.DataFrame(res_base_labels)
    # split into short df and no short df
    if df_base_labels['train_type'].str.contains('short').any():
        short_df_base_labels = df_base_labels[df_base_labels['train_type'].str.contains('short')]
        fig_path_base_labels_short = 'results/v0/figs/win_rates_base_labels_short.png'
        create_win_rates_plot(short_df_base_labels, fig_path_base_labels_short)
    else:
        no_short_df_base_labels = df_base_labels[~df_base_labels['train_type'].str.contains('short')]
        fig_path_base_labels_no_short = 'results/v0/figs/win_rates_base_labels.png'
        create_win_rates_plot(no_short_df_base_labels, fig_path_base_labels_no_short)



if __name__ == "__main__":
    """ Human Agreement """    
    label_dict = {        
        'eig_label_logp_qs': [            
            'results/v0/instruct_8b_1_user_questions.json',
            'results/v0/eig_labels_logp_qs_epoch_1_lr7e-6_questions.json',
            'results/v0/eig_labels_logp_qs_epoch_2_lr7e-6_questions.json'
        ],        
        'eig_label_eig_qs': [
            'results/v0/instruct_8b_1_user_questions.json',
            'results/v0/eig_labels_epoch_1_lr7e-6_questions.json',
            'results/v0/eig_labels_epoch_2_lr7e-6_questions.json'
        ],  
        'u4_label_logp_qs': [
            'results/v0/instruct_8b_1_user_questions.json',
            'results/v0/u4_labels_logp_qs_epoch_1_lr7e-6_questions.json',
            'results/v0/u4_labels_logp_qs_epoch_2_lr7e-6_questions.json',
        ],
        'u4_label_eig_qs': [
            'results/v0/instruct_8b_1_user_questions.json',
            'results/v0/u4_labels_eig_qs_epoch_1_lr7e-6_questions.json',
            'results/v0/u4_labels_eig_qs_epoch_2_lr7e-6_questions.json',
        ],

    }
    fig_path = 'results/v0/figs/human_agreement.png'
    # fig_path = 'results/v0/figs/human_agreement_sys.png'
    human_label_path = 'data/labels/exp_when_9_pp_maj_votes_0_200.json'
    plot_human_agrement(human_label_path, label_dict, fig_path)  
    """ Win Rates Against Base Models """
    win_rate_dict = {        
        # label: u4, qs: eig
        'u4_label_eig_qs': {
            'win_rate': [
                'results/v0/instruct_vs_u4_labels_eig_qs_epoch_1_lr7e-6_win_rates.json',
                'results/v0/instruct_vs_u4_labels_eig_qs_epoch_2_lr7e-6_win_rates.json'
                ],
            'question_label': [
                'results/v0/u4_labels_eig_qs_epoch_1_lr7e-6_questions.json',
                'results/v0/u4_labels_eig_qs_epoch_2_lr7e-6_questions.json'
                ]
        },
        # label: u4, qs: logp
        'u4_label_logp_qs': {
            'win_rate': [
                'results/v0/instruct_vs_u4_labels_logp_qs_epoch_1_lr7e-6_win_rates.json',
                'results/v0/instruct_vs_u4_labels_logp_qs_epoch_2_lr7e-6_win_rates.json'
            ],
            'question_label': [
                'results/v0/u4_labels_logp_qs_epoch_1_lr7e-6_questions.json',
                'results/v0/u4_labels_logp_qs_epoch_2_lr7e-6_questions.json'
            ]
        },
        # label: eig, qs: eig
        'eig_label_eig_qs': {
            'win_rate': [
                'results/v0/instruct_vs_eig_labels_epoch_1_lr7e-6_win_rates.json',
                'results/v0/instruct_vs_eig_labels_epoch_2_lr7e-6_win_rates.json'
            ],
            'question_label': [
                'results/v0/eig_labels_epoch_1_lr7e-6_questions.json',
                'results/v0/eig_labels_epoch_2_lr7e-6_questions.json'
            ]
        },
       # # label: eig, qs: logp
       'eig_label_logp_qs': {
            'win_rate': [
                'results/v0/instruct_vs_eig_labels_logp_qs_epoch_1_lr7e-6_win_rates.json',
                'results/v0/instruct_vs_eig_labels_logp_qs_epoch_2_lr7e-6_win_rates.json'
            ],
            'question_label': [
                'results/v0/eig_labels_logp_qs_epoch_1_lr7e-6_questions.json',
                'results/v0/eig_labels_logp_qs_epoch_2_lr7e-6_questions.json'
            ]
         },
    }
    human_label_path = 'data/labels/exp_when_9_pp_maj_votes_0_200.json'
    base_label_path = 'results/v0/instruct_8b_1_user_questions.json' 
    plot_win_rates(win_rate_dict, human_label_path, base_label_path)