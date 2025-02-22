# utils.py

import json
import re
from typing import Dict, Any, Optional
from config.default_templates import TASK_PARAMETERS, ROLE_TEMPLATES, PROMPT_TECHNIQUES

def format_prompt_with_template(template: str, query: str, role: Optional[str] = None, 
                              technique: Optional[str] = None) -> str:
    """
    Safely format a template with a query, optionally applying role and technique templates
    
    Args:
        template (str): Template string with {query} placeholder
        query (str): User query to insert
        role (str, optional): Role to use for template
        technique (str, optional): Prompt technique to apply
        
    Returns:
        str: Formatted prompt
    """
    # Start with base template
    current_template = template
    
    # Apply role template if specified
    if role and role in ROLE_TEMPLATES:
        role_template = ROLE_TEMPLATES[role]
        current_template = role_template.format(query=current_template)
    
    # Apply technique template if specified
    if technique and technique in PROMPT_TECHNIQUES:
        technique_template = PROMPT_TECHNIQUES[technique]
        current_template = technique_template.format(
            query=current_template,
            role=role if role else "Assistant"
        )
    
    # Final query insertion
    if "{query}" in current_template:
        return current_template.format(query=query)
    return query

def get_parameters_for_task(task_type: str, base_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get recommended parameters for specific task types with optional base parameters
    
    Args:
        task_type (str): Type of task (math, coding, creative, etc.)
        base_params (dict, optional): Base parameters to extend
        
    Returns:
        dict: Parameter configuration
    """
    # Get task-specific parameters
    task_params = TASK_PARAMETERS.get(task_type, TASK_PARAMETERS["default"]).copy()
    
    # Merge with base parameters if provided
    if base_params:
        task_params.update(base_params)
    
    return task_params

def validate_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize model parameters
    
    Args:
        params (dict): Parameters to validate
        
    Returns:
        dict: Validated parameters
    """
    validated = params.copy()
    
    # Temperature bounds
    if "temperature" in validated:
        validated["temperature"] = max(0.0, min(1.0, float(validated["temperature"])))
    
    # Context window bounds
    if "num_ctx" in validated:
        validated["num_ctx"] = max(512, min(8192, int(validated["num_ctx"])))
    
    # Prediction length bounds
    if "num_predict" in validated:
        validated["num_predict"] = max(64, min(4096, int(validated["num_predict"])))
    
    return validated

def format_response(response: str, task_type: str) -> str:
    """
    Format model response based on task type
    
    Args:
        response (str): Raw model response
        task_type (str): Type of task
        
    Returns:
        str: Formatted response
    """
    if task_type == "code":
        # Clean up code response
        return clean_code_response(response)
    elif task_type == "math":
        # Format mathematical response
        return format_math_response(response)
    else:
        # Default formatting
        return response.strip()

def clean_code_response(response: str) -> str:
    """Clean and format code response"""
    # Remove extra whitespace
    response = response.strip()
    
    # Extract code blocks if present
    code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', response, re.DOTALL)
    if code_blocks:
        return "\n\n".join(block.strip() for block in code_blocks)
    
    return response

def format_math_response(response: str) -> str:
    """Format mathematical response"""
    # Clean up math symbols
    response = response.replace('**', '^')
    response = response.replace('*', '×')
    
    # Add step numbers if not present
    if not re.search(r'Step \d+:', response):
        steps = response.split('\n\n')
        numbered_steps = [f"Step {i+1}: {step.strip()}" 
                         for i, step in enumerate(steps) if step.strip()]
        response = '\n\n'.join(numbered_steps)
    
    return response

def print_step(step_name: str, data: Any, is_json: bool = True) -> None:
    """
    Print formatted output with clear section separators
    
    Args:
        step_name (str): Name of the step or section
        data (any): Data to display
        is_json (bool): Whether to format the data as JSON
    """
    separator = "=" * 80
    print(f"\n{separator}")
    print(f"  {step_name}")
    print(f"{separator}\n")
    
    if is_json and isinstance(data, dict):
        try:
            # Handle nested objects that might not be JSON serializable
            def handle_non_serializable(obj):
                return str(obj)
            
            formatted_json = json.dumps(data, indent=2, default=handle_non_serializable)
            print(formatted_json)
        except Exception as e:
            print(f"Error formatting JSON: {e}")
            print(data)
    else:
        print(data)
    print()

def log_request_response(request: Dict[str, Any], response: str, 
                        time_taken: float) -> None:
    """
    Log request and response details
    
    Args:
        request (dict): Request payload
        response (str): Model response
        time_taken (float): Time taken for request
    """
    print_step("REQUEST", request)
    print_step("RESPONSE", response, is_json=False)
    print(f"Time taken: {time_taken:.2f}s")