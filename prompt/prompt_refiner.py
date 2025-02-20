from .analyzers import call_llm_for_analysis, parse_json_response

def iterative_prompt_refinement(initial_message, min_iterations=3, max_iterations=5, threshold=0.9):
    """
    Recursively refine a prompt through multiple iterations,
    ensuring a minimum number of refinements occur.
    
    Args:
        initial_message (str): Original user query
        min_iterations (int): Minimum number of refinement iterations
        max_iterations (int): Maximum refinement iterations
        threshold (float): Quality threshold to stop iterations (0-1)
        
    Returns:
        dict: Final template configuration with high-quality prompt
    """
    
    current_message = initial_message
    current_quality = 0
    iteration = 0
    
    # Keep track of the best configuration so far
    best_config = None
    best_quality = 0
    
    while iteration < max_iterations:
        # Force at least min_iterations regardless of quality score
        force_continue = iteration < min_iterations
        
        # Meta-prompt with simpler JSON structure
        meta_prompt = f"""
        Evaluate this candidate prompt: "{current_message}"
        
        1. Rate the current prompt quality from 0.0 to 1.0
        2. Provide an improved version even if quality is high
        3. Determine the optimal role and parameters for this query
        
        Return your analysis in JSON format:
        {{
            "quality_score": [score between 0-1],
            "improved_prompt": "[refined prompt]",
            "role": "[appropriate expert role]",
            "template": "[prompt template with {{query}} placeholder]",
            "parameters": {{
                "temperature": [appropriate value],
                "num_ctx": [appropriate value],
                "num_predict": [appropriate value]
            }},
            "reasoning": "[explanation of changes made]"
        }}
        """
        
        # Get analysis and refinement
        response = call_llm_for_analysis(meta_prompt)
        result = parse_json_response(response)
        
        # Update tracking variables
        current_quality = result.get("quality_score", 0)
        improved_prompt = result.get("improved_prompt")
        
        # Log the refinement process
        print(f"Iteration {iteration+1}:")
        print(f"Current quality: {current_quality}")
        print(f"Reasoning: {result.get('reasoning', 'No reasoning provided')}")
        
        # Save this as the best config if it has the highest quality so far
        if current_quality > best_quality:
            best_config = result
            best_quality = current_quality
        
        # Update the message if improvements were suggested
        if improved_prompt and improved_prompt != current_message:
            current_message = improved_prompt
        else:
            # If no improvements made or same prompt returned
            if not force_continue and current_quality >= threshold:
                break
            
            # Artificially continue by nudging the prompt
            current_message = f"{current_message} (Please refine this further)"
            
        iteration += 1
        
        # Exit loop if we've reached minimum iterations and quality threshold
        if not force_continue and current_quality >= threshold:
            break
    
    # If we couldn't get a valid config, use a reasonable default for math
    if not best_config:
        best_config = {
            "role": "Mathematician",
            "template": "Calculate the following mathematical expression step-by-step: {query}",
            "parameters": {"temperature": 0.2, "num_ctx": 2048, "num_predict": 1024},
            "final_prompt": current_message,
            "iterations_used": iteration,
            "final_quality": current_quality
        }
    else:
        # Format final configuration
        best_config.update({
            "final_prompt": current_message,
            "iterations_used": iteration,
            "final_quality": current_quality
        })
    
    # Add template validation and final prompt preparation before returning
    if best_config:
        # Clean up and validate the final prompt
        _validate_and_clean_config(best_config, initial_message)
        
    return best_config

def _validate_and_clean_config(config, original_message):
    """
    Validates and cleans a prompt configuration to prevent common issues.
    
    Args:
        config (dict): The prompt configuration to validate
        original_message (str): The original user query
    """
    # 1. Handle final prompt placeholders
    if "final_prompt" in config:
        final_prompt = config["final_prompt"]
        
        # Remove refinement markers
        final_prompt = final_prompt.replace("(Please refine this further)", "").strip()
        
        # Handle placeholders in final prompt
        if "{query}" in final_prompt:
            # Check for potential recursion in math prompts
            if ("calculate" in final_prompt.lower() or 
                "log" in final_prompt.lower() or
                "*" in final_prompt):
                # For math, use a safe direct prompt
                final_prompt = original_message
            else:
                # For other cases, do simple replacement
                final_prompt = final_prompt.replace("{query}", original_message)
                
        config["final_prompt"] = final_prompt
    
    # 2. Validate parameters to ensure they're reasonable
    if "parameters" in config:
        params = config["parameters"]
        # Set minimum/maximum values for critical parameters
        params["num_ctx"] = max(1024, int(params.get("num_ctx", 1024)))
        params["num_predict"] = max(512, int(params.get("num_predict", 512)))
        params["temperature"] = min(max(0.1, float(params.get("temperature", 0.7))), 1.0)


def format_final_prompt(config, original_message):
    """
    Formats the final prompt based on configuration.
    
    Args:
        config (dict): The prompt configuration
        original_message (str): The original user query
        
    Returns:
        str: The formatted prompt ready for the model
    """
    # Get the final prompt from config
    final_prompt = config.get("final_prompt", original_message)
    
    # If we still have template placeholders, fall back to original
    if "{query}" in final_prompt:
        return original_message
        
    return final_prompt