import os
import sys
import json


def combine_gold_responses(gold_responses_paths, output_path):
    gold_responses = json.load(open(gold_responses_paths[0], 'r'))
    for gold_responses_path in gold_responses_paths[1:]:
        with open(gold_responses_path, 'r') as f:
            data = json.load(f)            
            if data.keys() != gold_responses.keys():                
                gold_responses.update(data)
            else:
                for k, v in data.items():
                    gold_responses[k].extend(v)

    with open(output_path, 'w') as f:
        json.dump(gold_responses, f, indent=4)




if __name__ == '__main__':    
    # """ gold responses 20 users 10k """
    # file_paths = [
    #     'data/gold_responses/gold_responses_prompts_0-250_20_users_full.json',
    #     'data/gold_responses/gold_responses_9.750k_20_users_full.json'
    # ]
    # output_path = 'data/gold_responses/gold_responses_10k_20_users_full.json'
    # combine_gold_responses(file_paths, output_path)
    # """" conv 10k 1 user """
    # file_paths = [
    #     'data/conversations/1_user-250_5000_conv.json',
    #     'data/conversations/1_user-5000_10000_conv.json'
    # ]
    # output_path = 'data/conversations/conv_10k-1_user.json'
    # combine_gold_responses(file_paths, output_path)
    # """ conv 10k 2 users """
    # file_paths = [
    #     'data/conversations/2_user-250_1000_conv.json',
    #     'data/conversations/2_user-1000_2000_conv.json',
    #     'data/conversations/2_user-2000_3000_conv.json',
    #     'data/conversations/2_user-3000_5000_conv.json',        
    #     'data/conversations/2_user-5000_7500_conv.json',
    #     'data/conversations/2_user-7500_10000_conv.json'
    # ]
    # output_path = 'data/conversations/conv_10k-2_user.json'
    # combine_gold_responses(file_paths, output_path)
    """ info gain 10k 1 user """
    file_paths = [
        'data/expected_info_gain/logprobs_250_5000.json',
        'data/expected_info_gain/logprobs_5000_10000.json'
    ]
    output_path = 'data/expected_info_gain/logprobs_10k.json'
    combine_gold_responses(file_paths, output_path)
    
    
    
