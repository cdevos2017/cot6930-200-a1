"""Functions for meta-analysis of prompts and responses using LLMs."""
# Import necessary modules
import json
import re
from config._pipeline import create_payload, model_req

def call_llm_for_analysis(meta_prompt, model="llama3.2:latest", target="open-webui", **model_params):
    """
    Call the LLM specifically for meta-analysis of incoming queries.
    
    Args:
        meta_prompt (str): The prompt asking for analysis of the user query
        model (str): Model to use for analysis
        target (str): Target platform (open-webui, ollama, etc.)
        **model_params: Additional parameters to pass to the model
        
    Returns:
        str: JSON response from the model with template configuration
    """
    # Enhance the prompt with JSON formatting instructions
    enhanced_prompt = (
        "You will analyze a user query and provide a JSON response. "
        "Your response must ONLY contain valid JSON with no commentary before or after. "
        "The JSON must be on a single line with no line breaks within values. "
        "All strings must use double quotes. "
        "The JSON must be parseable by json.loads().\n\n" + meta_prompt
    )
    
    # Set default parameters if not provided
    default_params = {
        "temperature": 0.2,
        "num_ctx": 2048,
        "num_predict": 512
    }
    
    # Use provided parameters, falling back to defaults when needed
    for key, value in default_params.items():
        if key not in model_params:
            model_params[key] = value
    
    # Create payload using the parameters from the caller
    meta_payload = create_payload(
        target=target,
        model=model,
        prompt=enhanced_prompt,
        **model_params
    )
    
    # Call the model using the request function
    _, meta_response = model_req(request_payload=meta_payload)
    
    return meta_response

def parse_json_response(response):
    """
    Extract and parse the JSON configuration from the LLM response.
    Handles potential formatting issues in the response.
    """
    # Default configuration for math problems
    default_config = {
        "quality_score": 0.7,
        "improved_prompt": None,
        "role": "Mathematician",
        "template": "Calculate the following mathematical expression step-by-step: {query}",
        "parameters": {
            "temperature": 0.2,
            "num_ctx": 2048,
            "num_predict": 1024
        },
        "reasoning": "Default configuration for mathematical calculation"
    }
    
    # If response is empty
    if not response:
        print("No response received from model")
        return default_config
    
    # Log the raw response for debugging
    print(f"Raw response to parse: {response[:100]}...")
    
    try:
        # Look for a JSON object
        match = re.search(r'({.+})', response.replace('\n', ' '), re.DOTALL)
        if match:
            json_str = match.group(1)
            # Try to parse the JSON
            try:
                result = json.loads(json_str)
                return result
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                return default_config
        else:
            print("No JSON object found in response")
            return default_config
            
    except Exception as e:
        print(f"Unexpected error during JSON parsing: {str(e)}")
        return default_config