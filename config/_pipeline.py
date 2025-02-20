##
## Prompt Engineering Lab
## Platform for Education and Experimentation with Prompt NEngineering in Generative Intelligent Systems
## _pipeline.py :: Simulated GenAI Pipeline 
## 
#  
# Copyright (c) 2025 Dr. Fernando Koch, The Generative Intelligence Lab @ FAU
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# Documentation and Getting Started:
#    https://github.com/GenILab-FAU/prompt-eng
#
# Disclaimer: 
# Generative AI has been used extensively while developing this package.
# 

import os
import time
import json
import requests
from config.config_loader import load_config

def create_payload(model, prompt, target="ollama", **kwargs):
    """
    Create the Request Payload in the format required byt the Model Server
    @NOTE: 
    Need to adjust here to support multiple target formats
    target can be only ('ollama' or 'open-webui')

    @TODO it should be able to self_discover the target Model Server
    [Issue 1](https://github.com/genilab-fau/prompt-eng/issues/1)
    """

    result_payload = None
    if target == "ollama":
        result_payload = {
            "model": model,
            "prompt": prompt, 
            "stream": False,
        }
        if kwargs:
            result_payload["options"] = {key: value for key, value in kwargs.items()}

    elif target == "open-webui":
        # @TODO need to verify the format for 'parameters' for 'open-webui' is correct.
        # [Issue 2](https://github.com/genilab-fau/prompt-eng/issues/2)
        result_payload = {
            "model": model,
            "messages": [ {"role" : "user", "content": prompt } ]
        }
        
        # Handle parameters for open-webui
        if kwargs:
            result_payload["parameters"] = {key: value for key, value in kwargs.items()}
        
    else:
        print(f'!!ERROR!! Unknown target: {target}')
    return result_payload


def model_req(request_payload=None):
    """
    Issue request to the Model Server
    """
        
    try:
        load_config()
    except FileNotFoundError:
        return -1, "!!ERROR!! Problem loading configuration - File not Found"

    url = os.getenv('URL_GENERATE', None)
    api_key = os.getenv('API_KEY', None)
    delta = resp = None

    headers = dict()
    headers["Content-Type"] = "application/json"
    if api_key: headers["Authorization"] = f"Bearer {api_key}"

    print(request_payload)

    # Send out request to Model Provider
    try:
        start_time = time.time()
        resp = requests.post(url, data=json.dumps(request_payload) if request_payload else None, headers=headers, timeout=30)
        delta = time.time() - start_time
    except requests.RequestException:
        return -1, f"!!ERROR!! Request failed! You need to adjust config with URL({url})"

    # Checking the response and extracting the 'response' field
    if resp is None:
        return -1, "!!ERROR!! There was no response (?)"
    elif resp.status_code == 200:

        ## @NOTE: Need to adjust here to support multiple response formats
        result = ""
        delta = round(delta, 3)

        response_json = resp.json()
        if 'response' in response_json: ## ollama
            result = response_json['response']
        elif 'choices' in response_json: ## open-webui
            result = response_json['choices'][0]['message']['content']
        else:
            result = response_json 
        
        return delta, result
    elif resp.status_code == 401:
        return -1, f"!!ERROR!! Authentication issue. You need to adjust prompt-eng/config with API_KEY ({url})"
    else:
        return -1, f"!!ERROR!! HTTP Response={resp.status_code}, {resp.text}"


###
### DEBUG
###

if __name__ == "__main__":
    MESSAGE = "1 + 1"
    PROMPT = MESSAGE 
    payload = create_payload(
                         target="open-webui",   
                         model="llama3.2:latest", 
                         prompt=PROMPT, 
                         temperature=1.0, 
                         num_ctx=5555555, 
                         num_predict=1)

    time, response = model_req(request_payload=payload)
    print(response)
    if time: print(f'Time taken: {time}s')