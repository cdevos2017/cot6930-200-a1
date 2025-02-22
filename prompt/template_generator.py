# template_generator.py

from .analyzers import call_llm_for_analysis, parse_json_response
from config.default_templates import ROLE_TEMPLATES, PROMPT_TECHNIQUES, TASK_PARAMETERS
import re

def determine_template(message, analysis_result=None):
    """
    Analyze message and return appropriate template configuration using both
    rule-based and LLM-based analysis.
    
    Args:
        message (str): User query
        analysis_result (dict, optional): Previous LLM analysis result
        
    Returns:
        dict: Template configuration
    """
    # If we have LLM analysis, use that role
    if analysis_result and "role" in analysis_result:
        role = analysis_result["role"]
    else:
        # Otherwise use rule-based role detection
        role = detect_role(message)
    
    # Get the base template for the role
    template = ROLE_TEMPLATES.get(role, ROLE_TEMPLATES["Assistant"])
    
    # Detect if we should apply any specific prompt techniques
    technique = detect_prompt_technique(message)
    if technique:
        # Combine role template with prompt technique
        template = PROMPT_TECHNIQUES[technique].format(
            role=role,
            query=template
        )
    
    # Get appropriate parameters
    task_type = detect_task_type(message)
    parameters = TASK_PARAMETERS.get(task_type, TASK_PARAMETERS["default"])
    
    return {
        "role": role,
        "template": template,
        "parameters": parameters,
        "technique": technique,
        "task_type": task_type
    }

def detect_role(message):
    """
    Detect most appropriate role based on message content.
    """
    # Define role detection patterns
    role_patterns = {
        "Mathematician": r"(math|calculate|equation|solve|formula|\+|\-|\*|\/|\^|log|sin|cos)",
        "Software Engineer": r"(code|program|function|algorithm|class|API)",
        "Data Scientist": r"(data|analysis|statistics|correlation|dataset|predict)",
        "Teacher": r"(explain|teach|learn|understand|concept|example)",
        "Creative Writer": r"(story|write|creative|narrative|plot|character)",
        "Business Analyst": r"(business|market|strategy|analyze|ROI|profit)",
        # Add more role patterns as needed
    }
    
    # Check each pattern
    for role, pattern in role_patterns.items():
        if re.search(pattern, message, re.IGNORECASE):
            return role
            
    return "Assistant"  # Default role

def detect_prompt_technique(message):
    """
    Detect if a specific prompt technique should be applied.
    """
    # Check for indicators that suggest using specific techniques
    if re.search(r"(step[s]?|how to|process|method)", message, re.IGNORECASE):
        return "chain_of_thought"
    elif re.search(r"(compare|different ways|alternatives)", message, re.IGNORECASE):
        return "tree_of_thought"
    elif re.search(r"(explain|why|reason)", message, re.IGNORECASE):
        return "socratic"
    
    return None  # No specific technique needed

def detect_task_type(message):
    """
    Detect the type of task from the message.
    """
    # Define task type patterns
    task_patterns = {
        "math": r"(math|calculate|equation|solve|\+|\-|\*|\/)",
        "coding": r"(code|program|function|algorithm)",
        "creative_writing": r"(story|write|creative|narrative)",
        "analysis": r"(analyze|examine|study|investigate)",
        "explanation": r"(explain|describe|what is|how does)",
        # Add more task patterns as needed
    }
    
    # Check each pattern
    for task_type, pattern in task_patterns.items():
        if re.search(pattern, message, re.IGNORECASE):
            return task_type
            
    return "default"

def get_meta_template(message):
    """
    Get template configuration using LLM analysis.
    """
    meta_prompt = f"""
    Analyze this user query: "{message}"
    
    Determine the most appropriate role and prompt template to handle this query.
    Consider these aspects:
    1. What expert role would be best suited to answer this?
    2. What prompt technique would be most effective?
    3. What task-specific parameters would work best?
    
    Return your analysis in JSON format:
    {{
        "role": "[appropriate expert role]",
        "technique": "[suggested prompt technique]",
        "task_type": "[specific task category]",
        "template": "[prompt template with {{query}} placeholder]",
        "parameters": {{
            "temperature": [appropriate value],
            "num_ctx": [appropriate value],
            "num_predict": [appropriate value]
        }}
    }}
    """
    
    # Get LLM analysis
    response = call_llm_for_analysis(meta_prompt)
    llm_result = parse_json_response(response)
    
    # Combine LLM analysis with rule-based template selection
    final_config = determine_template(message, llm_result)
    
    return final_config