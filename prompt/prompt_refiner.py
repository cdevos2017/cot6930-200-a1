"""
Prompt refinement module for iteratively improving prompts.
"""

import time
from .analyzers import call_llm_for_analysis, parse_json_response
from .template_generator import determine_template
from .utils import format_prompt_with_template
from .techniques import select_technique
from .templates import get_technique_template
from .parameters import validate_parameters, get_parameters_for_task

def iterative_prompt_refinement(initial_message, min_iterations=3, max_iterations=5, threshold=0.9):
    """
    Recursively refine a prompt through multiple iterations
    
    Args:
        initial_message (str): Original user query
        min_iterations (int): Minimum number of refinement iterations
        max_iterations (int): Maximum refinement iterations
        threshold (float): Quality threshold to stop iterations (0-1)
        
    Returns:
        dict: Final template configuration with high-quality prompt
    """
    # Initialize tracking variables
    current_message = initial_message
    current_quality = 0.0
    best_quality = 0.0
    iteration = 0
    best_config = None
    
    # Get initial template configuration
    template_config = determine_template(initial_message)
    current_role = template_config.get("role", "Assistant")
    current_task_type = template_config.get("task_type", "default")
    current_technique = template_config.get("technique", "zero_shot")
    
    while iteration < max_iterations:
        force_continue = iteration < min_iterations
        
        # Construct meta-prompt with current configuration
        meta_prompt = f"""
        Evaluate this candidate prompt: "{current_message}"
        Current configuration:
        - Role: {current_role}
        - Technique: {current_technique}
        - Task Type: {current_task_type}
        
        1. Rate the current prompt quality from 0.0 to 1.0
        2. Provide an improved version even if quality is high
        3. Determine if the current role and technique are optimal for this task
        
        Return your analysis in JSON format:
        {{
            "quality_score": [score between 0-1],
            "improved_prompt": "[refined prompt]",
            "role": "[appropriate expert role]",
            "technique": "[suggested prompt technique]",
            "task_type": "[specific task category]",
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
        current_quality = float(result.get("quality_score", 0.0))
        improved_prompt = result.get("improved_prompt")
        
        # Log the refinement process
        print(f"Iteration {iteration+1}:")
        print(f"Current quality: {current_quality}")
        print(f"Reasoning: {result.get('reasoning', 'No reasoning provided')}")
        
        # Save this as the best config if it has the highest quality
        if current_quality > best_quality:
            best_config = result.copy()
            best_quality = current_quality
            
            # Update configuration if role or technique changed
            if (result.get("role") != current_role or 
                result.get("technique") != current_technique):
                new_template_config = determine_template(current_message, result)
                current_role = new_template_config.get("role", current_role)
                current_technique = new_template_config.get("technique", current_technique)
                current_task_type = new_template_config.get("task_type", current_task_type)
                template_config.update(new_template_config)
        
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
    
    # If we couldn't get a valid config, use template_config as base
    if not best_config:
        best_config = template_config.copy()
        best_config.update({
            "final_prompt": current_message,
            "iterations_used": iteration,
            "final_quality": current_quality
        })
    else:
        # Validate and clean the configuration
        best_config = _validate_and_clean_config(best_config, initial_message)
        
        # Format the final prompt safely
        try:
            formatted_prompt = format_prompt_with_template(
                best_config.get("template", "{query}"),
                current_message,
                role=best_config.get("role"),
                technique=best_config.get("technique")
            )
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error formatting prompt: {e}")
            formatted_prompt = current_message
        
        # Update configuration with final values
        best_config.update({
            "final_prompt": formatted_prompt,
            "iterations_used": iteration,
            "final_quality": current_quality,
            "parameters": validate_parameters(best_config.get("parameters", {}))
        })
    
    # Final validation and cleanup
    return _validate_and_clean_config(best_config, initial_message)

def format_final_prompt(config, original_message):
    """
    Formats the final prompt based on configuration
    
    Args:
        config (dict): The prompt configuration
        original_message (str): The original user query
        
    Returns:
        str: The formatted prompt ready for the model
    """
    try:
        # If we have a final prompt in the config, use that
        if "final_prompt" in config:
            final_prompt = config["final_prompt"]
            
            # Check if final_prompt is a string
            if isinstance(final_prompt, str):
                # Remove refinement markers
                final_prompt = final_prompt.replace("(Please refine this further)", "").strip()
                
                # Format with appropriate templates if needed
                return format_prompt_with_template(
                    final_prompt,
                    original_message,
                    role=config.get("role"),
                    technique=config.get("technique")
                )
            elif isinstance(final_prompt, dict):
                # If it's a dictionary, extract the text or return original
                if "text" in final_prompt:
                    return final_prompt["text"]
                else:
                    print(f"Error: final_prompt is a dict without text field: {final_prompt}")
                    return original_message
            else:
                print(f"Error: final_prompt is neither string nor dict: {type(final_prompt)}")
                return original_message
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error in format_final_prompt: {e}")
    
    # Fall back to original message if anything fails
    return original_message

def _validate_and_clean_config(config, original_message):
    """
    Validates and cleans a prompt configuration
    
    Args:
        config (dict): The prompt configuration to validate
        original_message (str): The original user query
        
    Returns:
        dict: Validated and cleaned configuration
    """
    # Validate final prompt
    if "final_prompt" in config:
        config["final_prompt"] = format_final_prompt(config, original_message)
    
    # Validate parameters
    if "parameters" in config:
        config["parameters"] = validate_parameters(config["parameters"])
    
    # Ensure we have all required fields
    required_fields = ["role", "template", "parameters", "task_type", "technique"]
    for field in required_fields:
        if field not in config:
            if field == "role":
                config[field] = "Assistant"
            elif field == "template":
                config[field] = "{query}"
            elif field == "parameters":
                config[field] = get_parameters_for_task("default")
            elif field == "task_type":
                config[field] = "default"
            elif field == "technique":
                config[field] = None
    
    # Validate parameter values
    if "parameters" in config:
        params = config["parameters"]
        # Ensure critical parameters are within bounds
        if "temperature" in params:
            params["temperature"] = min(max(0.1, float(params["temperature"])), 1.0)
        if "num_ctx" in params:
            params["num_ctx"] = min(max(1024, int(params["num_ctx"])), 8192)
        if "num_predict" in params:
            params["num_predict"] = min(max(512, int(params["num_predict"])), 4096)
    
    # Check for potential recursion in math prompts
    if config.get("task_type") == "math" and config.get("final_prompt"):
        final_prompt = config["final_prompt"]
        if isinstance(final_prompt, str) and any(term in final_prompt.lower() for term in ["calculate", "solve", "compute", "evaluate"]):
            # For math tasks, ensure we're not creating recursive prompts
            config["final_prompt"] = original_message.strip()
    
    # Validate template format
    if "template" in config:
        template = config["template"]
        if not isinstance(template, str) or "{query}" not in template:
            config["template"] = "{query}"
    
    # Clean up final prompt
    if "final_prompt" in config and isinstance(config["final_prompt"], str):
        final_prompt = config["final_prompt"]
        # Remove any refinement markers
        final_prompt = final_prompt.replace("(Please refine this further)", "").strip()
        # Remove duplicate whitespace
        final_prompt = " ".join(final_prompt.split())
        config["final_prompt"] = final_prompt
    
    # Add metadata if not present
    if "metadata" not in config:
        config["metadata"] = {
            "original_query": original_message,
            "validation_performed": True,
            "validation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    return config