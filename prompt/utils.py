"""
Helper functions for prompt engineering workflows.
"""
import json
from config.default_templates import TASK_PARAMETERS

def format_prompt_with_template(template, query):
    """
    Safely format a template with a query
    
    Args:
        template (str): Template string with {query} placeholder
        query (str): User query to insert
        
    Returns:
        str: Formatted prompt
    """
    if "{query}" in template:
        return template.format(query=query)
    return query

def get_parameters_for_task(task_type):
    """
    Get recommended parameters for specific task types
    
    Args:
        task_type (str): Type of task (math, coding, creative, etc.)
        
    Returns:
        dict: Parameter configuration
    """
    return TASK_PARAMETERS.get(task_type, TASK_PARAMETERS["default"])

def print_step(step_name, data, is_json=True):
    """
    Prints formatted output with clear section separators for debugging and tracing.
    
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
            formatted_json = json.dumps(data, indent=2)
            print(formatted_json)
        except json.JSONDecodeError:
            print(data)
    else:
        print(data)
    print()  # Extra newline for separation