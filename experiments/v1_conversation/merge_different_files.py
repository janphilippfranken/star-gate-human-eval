import os
import sys
import json


def combine_gold_responses(gold_responses_paths, output_path):
    gold_responses = json.load(open(gold_responses_paths[0], 'r'))
    for gold_responses_path in gold_responses_paths[1:]:
        with open(gold_responses_path, 'r') as f:
            data = json.load(f)            
            if data.keys() != gold_responses.keys():
                assert 'eig' in gold_responses_path, 'This is only for merging EIG files'
                gold_responses.update(data)
            else:
                for k, v in data.items():
                    gold_responses[k].extend(v)

    with open(output_path, 'w') as f:
        json.dump(gold_responses, f, indent=4)




if __name__ == '__main__':
    # # gold responses
    # gold_responses_paths = [
    # 'data/gold_responses/gold_responses_0_500_prompts_20_users_full.json',
    # 'data/gold_responses/gold_responses_500_1500_prompts_20_users_full.json',
    # 'data/gold_responses/gold_responses_1500_3000_prompts_20_users_full.json',
    # 'data/gold_responses/gold_responses_3000_4000_prompts_20_users_full.json',
    # 'data/gold_responses/gold_responses_4000_5000_prompts_20_users_full.json',
    # ]
    # gold_responses_output_path = 'data/gold_responses/gold_responses_0_5000_prompts_20_users_full.json'
    # combine_gold_responses(gold_responses_paths, gold_responses_output_path)
    # # conv 2 users
    # chat_2_user_paths = [
    #     'data/conversations/convo_0_500_prompts_2_users.json',
    #     'data/conversations/convo_500_1500_prompts_2_users.json',
    #     'data/conversations/convo_1500_2500_prompts_2_users.json',
    #     'data/conversations/convo_2500_3500_prompts_2_users.json',
    #     'data/conversations/convo_3500_5000_prompts_2_users.json'
    # ]
    # chat_2_user_output_path = 'data/conversations/convo_0_5000_prompts_2_users.json'
    # combine_gold_responses(chat_2_user_paths, chat_2_user_output_path)
    # # conv 4-17 users 5k
    # chat_4_17_user_paths = [
    #     'data/conversations/user_4-17/conv_0_250-user_4_17.json',
    #     'data/conversations/user_4-17/conv_250_1000-user_4_17.json',
    #     'data/conversations/user_4-17/conv_1000_2000-user_4_17.json',
    #     'data/conversations/user_4-17/conv_2000_3000-user_4_17.json',
    #     'data/conversations/user_4-17/conv_3000_4000-user_4_17.json',
    #     'data/conversations/user_4-17/conv_4000_5000-user_4_17.json',
    # ]
    # chat_4_17_user_output_path = 'data/conversations/user_4-17/conv_5k-user_4_17.json'
    # combine_gold_responses(chat_4_17_user_paths, chat_4_17_user_output_path)

    # # conv 5 users 5k
    # chat_5_users_5k_paths = [
    #     'data/conversations/v3/conv_250_750-5_user.json',
    #     'data/conversations/v3/conv_750_1250-5_user.json',
    #     'data/conversations/v3/conv_1250_1750-5_user.json',
    #     'data/conversations/v3/conv_1750_2500-5_user.json',
    #     'data/conversations/v3/conv_2500_3200-5_user.json',
    #     'data/conversations/v3/conv_3200_3900-5_user.json',
    #     'data/conversations/v3/conv_3900_4400-5_user.json',
    #     'data/conversations/v3/conv_4400_5000-5_user.json'
    # ]
    # chat_5_users_5k_output_path = 'data/conversations/v3/conv_5k-5_user.json'
    # combine_gold_responses(chat_5_users_5k_paths, chat_5_users_5k_output_path)

    # eig 5 users 5k
    gold_responses_20_users_10k_paths = [
        'data/gold_responses/gold_responses_prompts_0-250_20_users_full.json',
        'data/gold_responses/gold_responses_9.750k_20_users_full.json'
    ]
    gold_responses_20_users_10k_output_path = 'data/gold_responses/gold_responses_10k_20_users_full.json'
    combine_gold_responses(gold_responses_20_users_10k_paths, gold_responses_20_users_10k_output_path)
    
