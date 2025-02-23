# prompt_refiner.py

import time
from .analyzers import call_llm_for_analysis, parse_json_response
from .template_generator import determine_template
from .utils import format_prompt_with_template, get_parameters_for_task, validate_parameters
from .default_templates import get_prompt_technique

def select_prompt_technique(message, task_type):
    """
    Select the most appropriate prompt technique based on message content and task type.
    
    Args:
        message (str): The user's query
        task_type (str): Type of task being performed
        
    Returns:
        str: Name of the selected technique
    """
    # Task-specific technique mapping
    task_technique_map = {
        "math": "chain_of_thought",  # Math problems benefit from step-by-step thinking
        "reasoning": "tree_of_thought",  # Complex reasoning benefits from exploring multiple paths
        "analysis": "self_consistency",  # Analysis benefits from multiple approaches
        "coding": "chain_of_thought",  # Coding benefits from step-by-step breakdown
        "explanation": "socratic",  # Explanations benefit from questioning approach
        "creative": "role_playing",  # Creative tasks benefit from role immersion
        "structured": "structured_output"  # When specific output format is needed
    }
    
    # Content-based technique detection
    message_lower = message.lower()
    
    # Look for specific indicators in the message
    if any(x in message_lower for x in ["steps", "how to", "explain steps", "process"]):
        return "chain_of_thought"
    elif any(x in message_lower for x in ["compare", "different ways", "alternatives", "options"]):
        return "tree_of_thought"
    elif any(x in message_lower for x in ["analyze", "examine", "evaluate"]):
        return "self_consistency"
    elif any(x in message_lower for x in ["why", "explain", "reason"]):
        return "socratic"
    elif any(x in message_lower for x in ["format", "structure", "organize"]):
        return "structured_output"
    
    # Fall back to task-based technique
    return task_technique_map.get(task_type, "zero_shot")

def apply_prompt_technique(message, technique, role=None):
    """
    Apply a specific prompt technique to a message.
    
    Args:
        message (str): The message to enhance
        technique (str): The technique to apply
        role (str, optional): The role context
        
    Returns:
        str: Enhanced message using the technique
    """
    try:
        template = get_prompt_technique(technique)
        format_dict = {
            "query": message,
            "role": role if role else "Assistant",
            # Add default placeholders for specific techniques
            "approach1": "Consider the fundamental principles",
            "approach2": "Think about edge cases",
            "approach3": "Look for patterns or similarities"
        }
        return template.format(**format_dict)
    except (KeyError, AttributeError) as e:
        print(f"Warning: Failed to apply technique {technique}: {e}")
        return message

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
            
            # Remove refinement markers
            final_prompt = final_prompt.replace("(Please refine this further)", "").strip()
            
            # Format with appropriate templates if needed
            return format_prompt_with_template(
                final_prompt,
                original_message,
                role=config.get("role"),
                technique=config.get("technique")
            )
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
        if any(term in final_prompt.lower() for term in ["calculate", "solve", "compute", "evaluate"]):
            # For math tasks, ensure we're not creating recursive prompts
            config["final_prompt"] = original_message.strip()
    
    # Validate template format
    if "template" in config:
        template = config["template"]
        if not isinstance(template, str) or "{query}" not in template:
            config["template"] = "{query}"
    
    # Clean up final prompt
    if "final_prompt" in config:
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