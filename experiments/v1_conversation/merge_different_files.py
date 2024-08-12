import os
import sys
import json


def combine_gold_responses(gold_responses_paths, output_path):
    gold_responses = json.load(open(gold_responses_paths[0], 'r'))
    for gold_responses_path in gold_responses_paths[1:]:
        with open(gold_responses_path, 'r') as f:
            data = json.load(f)
            assert data.keys() == gold_responses.keys(), f"Keys don't match!"
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
    # conv 2 users
    chat_2_user_paths = [
        'data/conversations/convo_0_500_prompts_2_users.json',
        'data/conversations/convo_500_1500_prompts_2_users.json',
        'data/conversations/convo_1500_2500_prompts_2_users.json',
        'data/conversations/convo_2500_3500_prompts_2_users.json',
        'data/conversations/convo_3500_5000_prompts_2_users.json'
    ]
    chat_2_user_output_path = 'data/conversations/convo_0_5000_prompts_2_users.json'
    combine_gold_responses(chat_2_user_paths, chat_2_user_output_path)


