"""
Prompt Engineering Techniques Module

This module contains all prompt techniques logic and functionality,
separated from the actual templates and parameter configurations.
"""

from typing import Dict, List, Optional, Any, Tuple

# Import templates from the dedicated templates module
# Make sure techniques.py properly imports from templates.py
from .templates import (
    get_technique_template,
    get_role_template,
    get_l1_technique_template,
    get_l2_technique_step_template,
    get_l2_technique_steps_count
)

# Technique descriptions - metadata about different techniques
BASIC_TECHNIQUES = {
    "zero_shot": {
        "description": "Direct approach without examples or special formatting",
    },
    "few_shot": {
        "description": "Uses examples to guide the model's response",
    },
    "chain_of_thought": {
        "description": "Encourages step-by-step reasoning",
    },
    "self_consistency": {
        "description": "Considers multiple approaches to verify consistency",
    },
    "tree_of_thought": {
        "description": "Explores multiple reasoning paths",
    },
    "role_playing": {
        "description": "Assumes a specific expert role",
    },
    "structured_output": {
        "description": "Provides output in a specific format",
    },
    "socratic": {
        "description": "Uses self-questioning to approach the problem",
    },
    "guided_conversation": {
        "description": "Uses guided steps to analyze and respond",
    }
}

# Level-1 techniques use a meta-prompt to generate more effective prompts
L1_TECHNIQUES = {
    "meta_prompt": {
        "description": "Uses a prompt to generate another prompt for requirement analysis",
    },
    "stakeholder_perspective": {
        "description": "Analyzes requirements from multiple stakeholder perspectives",
    },
    "quality_criteria": {
        "description": "Structures requirements using quality attributes",
    }
}

# Level-2 techniques use a chain of prompts with state maintained between steps
L2_TECHNIQUES = {
    "refinement_chain": {
        "description": "Uses a chain of prompts to progressively refine requirements",
    },
    "divergent_convergent": {
        "description": "First diverges to explore many possible requirements, then converges to select the best ones",
    },
    "adverse_analysis": {
        "description": "Uses adversarial thinking to identify missing requirements and edge cases",
    }
}

# Core technique functions

def get_technique_description(technique_name: str) -> str:
    """
    Get the description of a specific technique.
    
    Args:
        technique_name: Name of the technique
        
    Returns:
        Description of the technique
    """
    if technique_name in BASIC_TECHNIQUES:
        return BASIC_TECHNIQUES[technique_name]["description"]
    elif technique_name in L1_TECHNIQUES:
        return L1_TECHNIQUES[technique_name]["description"]
    elif technique_name in L2_TECHNIQUES:
        return L2_TECHNIQUES[technique_name]["description"]
    else:
        return f"Unknown technique: {technique_name}"

def select_technique(message: str, task_type: str) -> str:
    """
    Select the most appropriate prompt technique based on message content and task type.
    
    Args:
        message: The user's query
        task_type: Type of task being performed
        
    Returns:
        Name of the selected technique
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

def apply_technique(message: str, technique: str, role: Optional[str] = None) -> str:
    """
    Apply a specific prompt technique to a message.
    
    Args:
        message: The message to enhance
        technique: The technique to apply
        role: Optional role context
        
    Returns:
        Enhanced message using the technique
    """
    try:
        template = get_technique_template(technique)
        format_dict = {
            "query": message,
            "role": role if role else "Assistant",
            # Add default placeholders for specific techniques
            "approach1": "Consider the fundamental principles",
            "approach2": "Think about edge cases",
            "approach3": "Look for patterns or similarities"
        }
        return template.format(**format_dict)
    except (KeyError, AttributeError, ValueError) as e:
        print(f"Warning: Failed to apply technique {technique}: {e}")
        return message

# Level-1 and Level-2 technique functions

def get_l1_technique_names() -> List[str]:
    """Get a list of available Level-1 technique names."""
    return list(L1_TECHNIQUES.keys())

def get_l2_technique_names() -> List[str]:
    """Get a list of available Level-2 technique names."""
    return list(L2_TECHNIQUES.keys())

def apply_l1_technique(query: str, technique_name: str) -> str:
    """
    Apply a Level-1 requirement analysis technique to a query.
    
    Args:
        query: The original requirements task/query
        technique_name: Name of the Level-1 technique to apply
        
    Returns:
        Formatted prompt using the specified technique
    """
    template = get_l1_technique_template(technique_name)
    return template.format(query=query)

def execute_l2_technique_step(
    query: str, 
    technique_name: str, 
    step: int, 
    previous_response: Optional[str] = None
) -> str:
    """
    Execute a specific step in a Level-2 technique.
    
    Args:
        query: The original requirements task/query
        technique_name: Name of the Level-2 technique
        step: The step number (0-indexed)
        previous_response: Response from the previous step (if applicable)
        
    Returns:
        Formatted prompt for the specified step
    """
    template = get_l2_technique_step_template(technique_name, step)
    
    if not template:
        print(f"Warning: No template found for {technique_name} step {step}. Using original query.")
        return query
        
    if previous_response:
        return template.format(query=query, previous_response=previous_response)
    else:
        return template.format(query=query)

def execute_l2_technique_full(
    query: str, 
    technique_name: str, 
    model_call_fn: callable,
    step_params: Optional[List[Dict[str, Any]]] = None
) -> Tuple[List[str], List[str]]:
    """
    Execute all steps of a Level-2 technique sequentially, using a model call function.
    
    Args:
        query: The original requirements task/query
        technique_name: Name of the Level-2 technique
        model_call_fn: Function that takes a prompt string and optional parameters and returns a response
        step_params: Optional list of parameter dictionaries for each step (must match number of steps)
        
    Returns:
        Tuple of (prompts, responses) where each is a list containing the prompt/response for each step
    """
    num_steps = get_l2_technique_steps_count(technique_name)
    
    if num_steps == 0:
        print(f"Warning: Unknown L2 technique: {technique_name}. Using single step with original query.")
        prompt = query
        response = model_call_fn(prompt, **(step_params[0] if step_params else {}))
        return [prompt], [response]
    
    # Initialize default parameters if not provided
    if step_params is None:
        step_params = [{}] * num_steps
    elif len(step_params) != num_steps:
        print(f"Warning: Parameter list length ({len(step_params)}) doesn't match "
              f"number of steps ({num_steps}). Using default parameters.")
        step_params = [{}] * num_steps
    
    prompts = []
    responses = []
    previous_response = None
    
    # Execute each step sequentially
    for i in range(num_steps):
        # Format the prompt for this step
        prompt = execute_l2_technique_step(query, technique_name, i, previous_response)
        prompts.append(prompt)
        
        # Call the model
        response = model_call_fn(prompt, **step_params[i])
        responses.append(response)
        
        # Use this response for the next step
        previous_response = response
    
    return prompts, responses