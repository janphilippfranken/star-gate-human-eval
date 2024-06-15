import torch


def mutual_information(
    logprobs: torch.FloatTensor, 
    n_users: int,
) -> torch.FloatTensor:
    
    # uniform over users 
    p_user = torch.tensor(1/n_users).repeat(n_users)
    
    # conditional probs 
    p_response_given_user = ((logprobs - torch.logsumexp(logprobs, dim=0))).exp()
    
    # marginal probs 
    p_response = (p_response_given_user * p_user).sum()
    
    # joint 
    p_response_and_user = p_response_given_user * p_user 
    
    # mutual information
    mutual_information = p_response_and_user * torch.log(p_response_given_user / p_response)
    
    return mutual_information.sum()