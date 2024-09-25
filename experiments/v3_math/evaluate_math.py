import json
import re 
import fire
import random
import hydra
import torch
from omegaconf import DictConfig
from transformers import AutoTokenizer

import logging

from datasets import load_dataset

from stargate.vllm_inference_model import VLLMInferenceModel
from dataset.util import clean_numbers, last_boxed_only, last_boxed_only_string, remove_boxed
from dataset.math_equivalence import is_equiv




SYSTEM_PROMPT = """
You are an expert in generating diverse solutions to math problems and selecting the optimal one. Upon receiving a problem and specific instructions from the user, your tasks are to:

1. Create multiple unique solutions using different methods for each.
2. After completing all solutions, select the best one and enclose it within the `<final_output>` tags.
"""

USER_PROMPT = """
Provide {N} step-by-step solutions to the following math problem. The last line of each solution should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem.

{question}

Remember to generate {N} independent solutions. At the end, enclose the best solution within the `<final_output>` and `</final_output>` XML tags.
"""

USER_EXAMPLE = """Provide 5 step-by-step solutions to the following math problem. The last line of each solution should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem.\n\nIn quadrilateral $ABCD$, $\\angle{BAD}\\cong\\angle{ADC}$ and $\\angle{ABD}\\cong\\angle{BCD}$, $AB = 8$, $BD = 10$, and $BC = 6$. The length $CD$ may be written in the form $\\frac {m}{n}$, where $m$ and $n$ are relatively prime positive integers. Find $m + n$.\n\n\nRemember to generate 5 independent solutions. At the end, enclose the best solution within the `<final_output>` and `</final_output>` XML tags."""

ASSISTANT_EXAMPLE = """<|reserved_special_token_0|>Attempt 1 Starts<|reserved_special_token_0|>\n\nTo solve this problem, we can use the concept of similar triangles and the properties of isosceles triangles.\n\nStep 1:  First, let's analyze the given information about quadrilateral $ABCD$: $\\angle{BAD}\\cong\\angle{ADC}$ and $\\angle{ABD}\\cong\\angle{BCD}$.\nStep 2:  Since $\\angle{BAD} \\cong \\angle{ADC}$, we can conclude that $\\triangle ABD \\sim \\triangle DCE$ because they share angle $D$ and have two pairs of congruent angles.\nStep 3:  Next, since $\\angle{ABD}\\cong\\angle{BCD}$, we can determine that $\\triangle ABD \\sim \\triangle DBC$.\nStep 4:  Therefore, $\\triangle ABD \\sim \\triangle DBC \\sim \\triangle DCE$. This allows us to use the property of similar triangles to establish a relationship between the sides of these triangles.\nStep 5:  Using the property of similar triangles, we get the following proportion: $\\frac{AB}{BD} = \\frac{BD}{BC} = \\frac{CD}{CE}$.\nStep 6:  Given that $AB = 8$, $BD = 10$, and $BC = 6$, we can substitute these values into the proportion to solve for $CD$.\nStep 7:  We have $\\frac{8}{10} = \\frac{10}{6} = \\frac{CD}{CE}$. From the first two fractions, we can solve for $CE$: $CE = \\frac{10 \\cdot 6}{8} = \\frac{15}{2}$.\nStep 8:  Substituting $CE = \\frac{15}{2}$ into the proportion, we get $\\frac{10}{6} = \\frac{CD}{\\frac{15}{2}}$.\nStep 9:  To solve for $CD$, we can cross multiply and simplify: $10 \\cdot \\frac{15}{2} = 6 \\cdot CD$.\nStep 10:  Solving for $CD$, we have $CD = \\frac{10 \\cdot 15}{2 \\cdot 6} = \\frac{25}{2}$.\nStep 11:  Therefore, the length $CD$ can be expressed as $\\frac{25}{2}$.\nStep 12:  Finally, we need to find the sum of the numerator and denominator of $\\frac{25}{2}$, which is $25 + 2 = 27$.\n\nAnswer: 27<|reserved_special_token_0|>Attempt 1 Ends<|reserved_special_token_0|>\n\n<|reserved_special_token_0|>Attempt 2 Starts<|reserved_special_token_0|>\n\nTo solve this problem, we need to use geometric properties and similarity of triangles.\n\nFirst, let's draw a diagram of quadrilateral $ABCD$.\n\n\nIn this diagram, extend $\\overline{AD}$ and $\\overline{BC}$ to meet at point $E$. Since $\\angle BAD$ and $\\angle ADC$ are congruent and $\\angle ABD$ and $\\angle DCE$ are congruent, $\\triangle ABD$ is similar to $\\triangle DCE$. This is due to the Angle-Angle Similarity Theorem, which states that if two angles of one triangle are congruent to two angles of another triangle, the triangles are similar.\n\n\nSince the triangles are similar, the ratio of the corresponding sides are equal. Therefore, we can write the following equation:\n\n\n$\\frac{AB}{BD} = \\frac{CD}{CE}$\n\n\nSubstituting the given values, we have:\n\n\n$\\frac{8}{10} = \\frac{CD}{16}$\n\n\nSimplifying this equation, we get:\n\n\n$CD = \\frac{64}{10}$\n\n\nThis fraction is already in the simplest form, so the sum of the numerator and denominator is:\n\n\n$64 + 10 = 74$\n\n\nAnswer: 74<|reserved_special_token_0|>Attempt 2 Ends<|reserved_special_token_0|>\n\n<|reserved_special_token_0|>Attempt 3 Starts<|reserved_special_token_0|>\n\nTo solve this problem, we can use the concept of similar triangles.\n\nFirst, we extend $\\overline{AD}$ and $\\overline{BC}$ to meet at a point $E$. \n\nSince $\\angle BAD = \\angle ADC$ and $\\angle ABD = \\angle DCE$, we have $\\triangle ABD \\sim \\triangle DCE$ by AA similarity.\n\nNow, let's use the fact that the ratio of corresponding sides of similar triangles is equal.\n\n$\\frac{AB}{BD} = \\frac{CD}{CE}$. We are given that $AB = 8$, $BD = 10$, and $BC = 6$. \n\nUsing the ratio of similar triangles, we get $\\frac{8}{10} = \\frac{CD}{CE}$. To find $CE$, we can use the fact that $CE = BC + BD$. So $CE = 6 + 10 = 16$.\n\nNow, we can substitute the value of $CE$ in the ratio: $\\frac{8}{10} = \\frac{CD}{16}$. To find $CD$, we can cross-multiply: $8 \\times 16 = 10 \\times CD$. \n\nThis simplifies to $128 = 10 \\times CD$, and we can now solve for $CD$ by dividing both sides by $10$: $CD = \\frac{128}{10} = \\frac{64}{5}$.\n\nSo the length $CD$ is $\\frac{64}{5}$, and we need to find $m + n$ where $m$ and $n$ are relatively prime positive integers. In this case, $m = 64$ and $n = 5$, so $m + n = 64 + 5 = 69$.\n\nAnswer: 69<|reserved_special_token_0|>Attempt 3 Ends<|reserved_special_token_0|>\n\n<|reserved_special_token_0|>Attempt 4 Starts<|reserved_special_token_0|>\n\nTo solve this problem, we can extend $\\overline{AB}$ and $\\overline{CD}$ to meet at a point $E$. Since $\\angle BAD = \\angle ADC$, we have $\\triangle ABD \\sim \\triangle DCE$ by the AA similarity postulate. \n\nFrom this similarity, we can set up a proportion to find the value of $x = CD$:\n\n$\\frac{AB}{BD} = \\frac{CE}{CD}$\n\nWe know that $AB = 8$ and $BD = 10$, so we can plug these values into the proportion to get:\n\n$\\frac{8}{10} = \\frac{16}{x}$\n\nCross-multiplying, we get $8x = 160$, so $x = 20$.\n\nHowever, we need to express $x$ in the form $\\frac{m}{n}$ where $m$ and $n$ are relatively prime positive integers. To do this, we can divide both the numerator and the denominator by their greatest common divisor, which is 20.\n\n$\\frac{20}{1}$ can be simplified to $\\frac{1}{1}$, and that has a GCD of 1, so we have $m = 1$ and $n = 1$, giving us $m + n = 2$.\n\nAnswer: 2<|reserved_special_token_0|>Attempt 4 Ends<|reserved_special_token_0|>\n\n<|reserved_special_token_0|>Attempt 5 Starts<|reserved_special_token_0|>\n\nTo solve this problem, we can start by extending $\\overline{AD}$ and $\\overline{BC}$ to meet at a point $E$.\n\nSince $\\angle{BAD}\\cong\\angle{ADC}$ and $\\angle{ABD}\\cong\\angle{BCD}$, we can conclude that $\\triangle ABD \\sim \\triangle DCE$. \n\nUsing the properties of similar triangles, we can write the proportion:\n\n$\\frac{AB}{BD} = \\frac{CD}{CE}$.\n\nWe are given that $AB = 8$ and $BD = 10$, so we can substitute these values into the proportion:\n\n$\\frac{8}{10} = \\frac{CD}{CE}$.\n\nWe are also given that $BC = 6$, so we can find $CE$ by adding $BC$ to $BD$:\n\n$CE = BD + BC = 10 + 6 = 16$.\n\nNow we can substitute $CE = 16$ into the proportion:\n\n$\\frac{8}{10} = \\frac{CD}{16}$.\n\nTo solve for $CD$, we can cross-multiply:\n\n$8 \\cdot 16 = 10 \\cdot CD$\n\n$128 = 10 \\cdot CD$\n\n$CD = \\frac{128}{10}$\n\nWe can simplify the fraction by dividing both the numerator and denominator by their greatest common divisor, which is $2$:\n\n$CD = \\frac{64}{5}$\n\nTherefore, $m = 64$ and $n = 5$, so the sum of $m$ and $n$ is:\n\n$64 + 5 = 69$\n\nAnswer: 69<|reserved_special_token_0|>Attempt 5 Ends<|reserved_special_token_0|>\n\n<final_output>\n\nTo solve this problem, we can use the concept of similar triangles.\n\nFirst, we extend $\\overline{AD}$ and $\\overline{BC}$ to meet at a point $E$. \n\nSince $\\angle BAD = \\angle ADC$ and $\\angle ABD = \\angle DCE$, we have $\\triangle ABD \\sim \\triangle DCE$ by AA similarity.\n\nNow, let's use the fact that the ratio of corresponding sides of similar triangles is equal.\n\n$\\frac{AB}{BD} = \\frac{CD}{CE}$. We are given that $AB = 8$, $BD = 10$, and $BC = 6$. \n\nUsing the ratio of similar triangles, we get $\\frac{8}{10} = \\frac{CD}{CE}$. To find $CE$, we can use the fact that $CE = BC + BD$. So $CE = 6 + 10 = 16$.\n\nNow, we can substitute the value of $CE$ in the ratio: $\\frac{8}{10} = \\frac{CD}{16}$. To find $CD$, we can cross-multiply: $8 \\times 16 = 10 \\times CD$. \n\nThis simplifies to $128 = 10 \\times CD$, and we can now solve for $CD$ by dividing both sides by $10$: $CD = \\frac{128}{10} = \\frac{64}{5}$.\n\nSo the length $CD$ is $\\frac{64}{5}$, and we need to find $m + n$ where $m$ and $n$ are relatively prime positive integers. In this case, $m = 64$ and $n = 5$, so $m + n = 64 + 5 = 69$.\n\nAnswer: 69</final_output>"""

@hydra.main(version_base=None, config_path="config", config_name="evaluate_trained")
def main(args: DictConfig) -> None:
    
    torch.manual_seed(42)
    random.seed(42)
    
    logging.info(args)

    # model
    model = VLLMInferenceModel(
        **args.model_config
    )
    
    # tokenizer 
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=args.model_config.model,
        cache_dir=args.model_config.download_dir,
    )
    
    # prompts
    dataset = load_dataset(
        "hendrycks/competition_math",
        split="test",
        cache_dir="./data/math",
    )
    
    dataset = dataset.shuffle(42)
    breakpoint()
    
    problems = [datum["problem"] for datum in dataset]
    solutions = [datum["solution"] for datum in dataset]
    answer_strings = [remove_boxed(last_boxed_only_string(solution)) for solution in solutions]
    
    prompts = [USER_PROMPT.format(question=question, N=4) for question in problems[:args.end_prompts]]
    
    prompts = [[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_EXAMPLE},
            {"role": "assistant", "content": ASSISTANT_EXAMPLE},
            {"role": "user", "content": prompt}]
        for prompt in prompts]
    breakpoint()

    formatted_batch_prompts = [
        tokenizer.apply_chat_template(prompt, tokenize=False) for prompt in prompts
    ]
    
    batch_responses = model.batch_prompt(
        prompts=formatted_batch_prompts,
        **args.generation_config,
    )
    
    breakpoint()
    # batch_responses = [
    #     response.split("<|start_header_id|>assistant<|end_header_id|>")[1].strip()
    #     for response in batch_responses   
    # ]
    
    best_answers = []
    for response in batch_responses:
        try:
            # Using a more flexible regex pattern to match content between tags
            match = re.search(r"<final_output>([\s\S]*?)</final_output>", response)
            if match:
                best_answers.append(match.group(1))
            else:
                best_answers.append("Null")
        except Exception as e:
            # Log the exception for debugging purposes
            best_answers.append("Null")
    
    breakpoint()

    formatted_batch_responses = []
    
    for response in best_answers:
        try:
            formatted_batch_responses.append(response.split("\n\nAnswer:")[1].strip())
        except:
            formatted_batch_responses.append("Null")

    response_scores = []
    response_rationales = []
    indices = [i for i in range(len(formatted_batch_responses)) if formatted_batch_responses[i] != "Null"]
    
    for i in indices:
        response = formatted_batch_responses[i]
        try:
            res = is_equiv(response, answer_strings[i]) 
            
            response_scores.append(int(res))
        except:
            response_scores.append(0)

    print(sum(response_scores)/len(response_scores))
if __name__ == "__main__":
    fire.Fire(main())