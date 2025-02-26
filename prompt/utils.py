"""
Utility functions for prompt engineering.
"""

import json
import re
from typing import Dict, Any, Optional

# Import from the centralized techniques module
from prompt.techniques import (
    get_role_template,
    get_technique_template
)

def format_prompt_with_template(template: str, query: str, role: Optional[str] = None, 
                              technique: Optional[str] = None, task_type: Optional[str] = None) -> str:
    """
    Format a template with query, applying role and technique enhancements
    
    Args:
        template (str): Base template with {query} placeholder
        query (str): User query to insert
        role (str, optional): Role to use
        technique (str, optional): Prompt technique to apply
        task_type (str, optional): Type of task
        
    Returns:
        str: Formatted prompt
    """
    try:
        # Ensure inputs are strings
        if not isinstance(template, str):
            print(f"Warning: template is not a string, type: {type(template)}. Using default.")
            template = "{query}"
        
        if not isinstance(query, str):
            if isinstance(query, dict) and "query" in query:
                query = query["query"]
            else:
                print(f"Warning: query is not a string, type: {type(query)}. Converting to string.")
                query = str(query)
        
        current_query = query
        
        # Apply technique first if specified
        if technique:
            try:
                technique_template = get_technique_template(technique)
                
                format_dict = {
                    "query": current_query,
                    "role": role if role else "Assistant",
                    # Add default placeholders for specific techniques
                    "approach1": "Consider the fundamental principles",
                    "approach2": "Think about edge cases",
                    "approach3": "Look for patterns or similarities"
                }
                
                try:
                    current_query = technique_template.format(**format_dict)
                except KeyError as e:
                    print(f"Warning: Failed to apply technique {technique}, missing key: {e}")
                except Exception as e:
                    print(f"Warning: Failed to apply technique {technique}: {e}")
                    
            except Exception as e:
                print(f"Warning: Failed to apply technique {technique}: {e}")
        
        # Then apply role template if specified
        if role:
            try:
                role_template = get_role_template(role)
                
                try:
                    current_query = role_template.format(query=current_query)
                except KeyError as e:
                    print(f"Warning: Failed to apply role {role}, missing key: {e}")
                except Exception as e:
                    print(f"Warning: Failed to apply role {role}: {e}")
                    
            except Exception as e:
                print(f"Warning: Failed to apply role {role}: {e}")
        
        # Finally apply the base template
        if "{query}" in template:
            try:
                return template.format(query=current_query)
            except KeyError as e:
                print(f"Warning: Missing key in template: {e}. Using current query.")
                return current_query
            except Exception as e:
                print(f"Warning: Failed to format template: {e}. Using current query.")
                return current_query
        else:
            print(f"Warning: No {{query}} placeholder in template: {template}. Using current query.")
            return current_query
    
    except Exception as e:
        print(f"Error in format_prompt_with_template: {e}")
        return query

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