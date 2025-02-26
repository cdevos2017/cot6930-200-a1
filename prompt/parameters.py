"""
Parameters module for prompt engineering.

Contains parameter configurations for different tasks and parameter validation functions.
"""

from typing import Dict, Any, Optional, Union

# Dictionary mapping task types to parameter configurations
TASK_PARAMETERS = {
    # Academic tasks
    "math": {
        "temperature": 0.2,
        "num_ctx": 2048,
        "num_predict": 1024
    },
    "statistics": {
        "temperature": 0.3,
        "num_ctx": 2048,
        "num_predict": 1024
    },
    "physics": {
        "temperature": 0.3,
        "num_ctx": 2048,
        "num_predict": 1024
    },
    "chemistry": {
        "temperature": 0.3,
        "num_ctx": 2048,
        "num_predict": 1024
    },
    "biology": {
        "temperature": 0.4,
        "num_ctx": 2048,
        "num_predict": 1280
    },
    "history": {
        "temperature": 0.5,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    "literature": {
        "temperature": 0.6,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    
    # Technical tasks
    "coding": {
        "temperature": 0.3,
        "num_ctx": 4096,
        "num_predict": 2048
    },
    "data_analysis": {
        "temperature": 0.3,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    "system_design": {
        "temperature": 0.4,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    "database": {
        "temperature": 0.3,
        "num_ctx": 2048,
        "num_predict": 1024
    },
    "devops": {
        "temperature": 0.3,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    "testing": {
        "temperature": 0.4,
        "num_ctx": 2048,
        "num_predict": 1280
    },
    
    # Writing tasks
    "copywriting": {
        "temperature": 0.7,
        "num_ctx": 2048,
        "num_predict": 1536
    },
    "technical_writing": {
        "temperature": 0.4,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    "creative_writing": {
        "temperature": 0.8,
        "num_ctx": 4096,
        "num_predict": 3096
    },
    "journalism": {
        "temperature": 0.5,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    "essay": {
        "temperature": 0.6,
        "num_ctx": 3072,
        "num_predict": 2048
    },
    
    # Business tasks
    "business_analysis": {
        "temperature": 0.5,
        "num_ctx": 2560,
        "num_predict": 1536
    },
    "product_strategy": {
        "temperature": 0.6,
        "num_ctx": 2560,
        "num_predict": 1536
    },
    "marketing": {
        "temperature": 0.7,
        "num_ctx": 2560,
        "num_predict": 1536
    },
    "financial_analysis": {
        "temperature": 0.3,
        "num_ctx": 2560,
        "num_predict": 1280
    },
    "consulting": {
        "temperature": 0.5,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    
    # Educational tasks
    "teaching": {
        "temperature": 0.5,
        "num_ctx": 2560,
        "num_predict": 1536
    },
    "tutoring": {
        "temperature": 0.4,
        "num_ctx": 2048,
        "num_predict": 1280
    },
    "career_advice": {
        "temperature": 0.6,
        "num_ctx": 2048,
        "num_predict": 1280
    },
    
    # Research tasks
    "research_design": {
        "temperature": 0.4,
        "num_ctx": 3584,
        "num_predict": 1792
    },
    "literature_review": {
        "temperature": 0.5,
        "num_ctx": 4096,
        "num_predict": 2048
    },
    "grant_writing": {
        "temperature": 0.5,
        "num_ctx": 3072,
        "num_predict": 1792
    },
    
    # Specialized analysis
    "legal_analysis": {
        "temperature": 0.4,
        "num_ctx": 3584,
        "num_predict": 1792
    },
    "policy_analysis": {
        "temperature": 0.5,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    "ethical_analysis": {
        "temperature": 0.6,
        "num_ctx": 3072,
        "num_predict": 1536
    },
    
    # General tasks
    "explanation": {
        "temperature": 0.5,
        "num_ctx": 2048,
        "num_predict": 1280
    },
    "planning": {
        "temperature": 0.5,
        "num_ctx": 2560,
        "num_predict": 1536
    },
    "analysis": {
        "temperature": 0.5,
        "num_ctx": 2560,
        "num_predict": 1536
    },
    "summarization": {
        "temperature": 0.4,
        "num_ctx": 2560,
        "num_predict": 1024
    },
    "translation": {
        "temperature": 0.3,
        "num_ctx": 2048,
        "num_predict": 1280
    },
    "creative": {
        "temperature": 0.8,
        "num_ctx": 4096,
        "num_predict": 3096
    },
    "default": {
        "temperature": 0.7,
        "num_ctx": 2048,
        "num_predict": 1024
    }
}

def get_parameters_for_task(task_type: str, base_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get parameters for a specific task type with optional base parameters.
    
    Args:
        task_type: Type of task
        base_params: Optional base parameters to override
    
    Returns:
        Parameters dictionary for the task
    """
    task_params = TASK_PARAMETERS.get(task_type, TASK_PARAMETERS["default"]).copy()
    
    if base_params:
        task_params.update(base_params)
    
    return task_params

def validate_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize model parameters.
    
    Args:
        params: Parameters to validate
        
    Returns:
        Validated parameters
    """
    validated = params.copy()
    
    # Temperature bounds
    if "temperature" in validated:
        try:
            temp = float(validated["temperature"])
            validated["temperature"] = max(0.0, min(1.0, temp))
        except (ValueError, TypeError):
            print(f"Warning: Invalid temperature value. Using default.")
            validated["temperature"] = 0.7
    
    # Context window bounds
    if "num_ctx" in validated:
        try:
            ctx = int(validated["num_ctx"])
            validated["num_ctx"] = max(512, min(8192, ctx))
        except (ValueError, TypeError):
            print(f"Warning: Invalid context window value. Using default.")
            validated["num_ctx"] = 2048
    
    # Prediction length bounds
    if "num_predict" in validated:
        try:
            pred = int(validated["num_predict"])
            validated["num_predict"] = max(64, min(4096, pred))
        except (ValueError, TypeError):
            print(f"Warning: Invalid prediction length value. Using default.")
            validated["num_predict"] = 1024
    
    return validated

def merge_parameters(default_params: Dict[str, Any], override_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Merge default parameters with override parameters.
    
    Args:
        default_params: Base parameters to start with
        override_params: Parameters to override defaults
        
    Returns:
        Merged and validated parameters
    """
    if not override_params:
        return validate_parameters(default_params)
    
    merged = default_params.copy()
    merged.update(override_params)
    
    return validate_parameters(merged)

def get_parameter_presets() -> Dict[str, Dict[str, Union[float, int]]]:
    """
    Get a dictionary of parameter presets for common use cases.
    
    Returns:
        Dictionary of parameter presets
    """
    return {
        "creative": {
            "temperature": 0.8,
            "num_ctx": 4096,
            "num_predict": 2048
        },
        "precise": {
            "temperature": 0.2,
            "num_ctx": 2048,
            "num_predict": 1024
        },
        "balanced": {
            "temperature": 0.5,
            "num_ctx": 2048,
            "num_predict": 1024
        },
        "chat": {
            "temperature": 0.7,
            "num_ctx": 2048,
            "num_predict": 512
        },
        "code": {
            "temperature": 0.3,
            "num_ctx": 4096,
            "num_predict": 2048
        }
    }