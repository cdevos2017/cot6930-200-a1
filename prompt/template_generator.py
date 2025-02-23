# template_generator.py

from .analyzers import call_llm_for_analysis, parse_json_response
from .default_templates import get_role_template, get_prompt_technique, get_task_parameters
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
    template = get_role_template(role)
    
    # Detect if we should apply any specific prompt techniques
    technique = detect_prompt_technique(message)
    if technique:
        # Get the technique template
        technique_template = get_prompt_technique(technique)
        try:
            # Combine role template with prompt technique
            template = technique_template.format(
                role=role,
                query=template
            )
        except KeyError as e:
            print(f"Warning: Failed to apply technique template: {e}")
    
    # Get appropriate parameters
    task_type = detect_task_type(message)
    parameters = get_task_parameters(task_type)
    
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
        "Physicist": r"(physics|force|motion|energy|quantum|momentum)",
        "Biologist": r"(biology|cell|organism|gene|evolution|species)",
        "Historian": r"(history|century|period|war|civilization|empire)",
        "Psychologist": r"(psychology|behavior|mental|cognitive|emotion)",
        "Financial Analyst": r"(finance|stock|investment|market|portfolio|risk)",
        "Language Expert": r"(grammar|language|sentence|word|phrase|meaning)",
        "Systems Architect": r"(system|architecture|design|infrastructure|scalability)",
        "Product Manager": r"(product|feature|user|requirement|roadmap|market)",
    }
    
    # Check each pattern
    matched_roles = []
    for role, pattern in role_patterns.items():
        if re.search(pattern, message, re.IGNORECASE):
            matched_roles.append(role)
    
    # If multiple roles match, choose the most specific one
    if len(matched_roles) > 1:
        # Count the number of pattern matches for each role
        role_matches = {}
        for role in matched_roles:
            pattern = role_patterns[role]
            matches = len(re.findall(pattern, message, re.IGNORECASE))
            role_matches[role] = matches
        
        # Return the role with the most matches
        return max(role_matches.items(), key=lambda x: x[1])[0]
    elif matched_roles:
        return matched_roles[0]
            
    return "Assistant"  # Default role

def detect_prompt_technique(message):
    """
    Detect if a specific prompt technique should be applied.
    """
    # Define technique patterns with priority (higher number = higher priority)
    technique_patterns = {
        "chain_of_thought": (r"(step[s]?|how to|process|method|solve|calculate)", 3),
        "tree_of_thought": (r"(compare|different ways|alternatives|options|choose|decide)", 4),
        "self_consistency": (r"(verify|check|confirm|validate|ensure|consistent)", 2),
        "socratic": (r"(explain|why|reason|understand|concept)", 1),
        "structured_output": (r"(format|structure|organize|list|categorize)", 2),
        "role_playing": (r"(pretend|act as|simulate|behave as|respond as)", 3),
        "few_shot": (r"(similar to|like|example|reference|previous)", 1)
    }
    
    # Find all matching techniques
    matched_techniques = {}
    for technique, (pattern, priority) in technique_patterns.items():
        matches = re.findall(pattern, message, re.IGNORECASE)
        if matches:
            matched_techniques[technique] = (len(matches), priority)
    
    if matched_techniques:
        # Choose technique based on number of matches and priority
        return max(matched_techniques.items(), key=lambda x: (x[1][0], x[1][1]))[0]
    
    return "zero_shot"  # Default technique

def detect_task_type(message):
    """
    Detect the type of task from the message.
    """
    # Define task type patterns with examples
    task_patterns = {
        "math": (r"(math|calculate|equation|solve|\+|\-|\*|\/|formula)", [
            "solve", "calculate", "equation", "formula", "computation"
        ]),
        "coding": (r"(code|program|function|algorithm|implementation)", [
            "implement", "code", "function", "class", "method"
        ]),
        "creative_writing": (r"(story|write|creative|narrative|plot)", [
            "write", "compose", "create", "story", "narrative"
        ]),
        "analysis": (r"(analyze|examine|study|investigate|evaluate)", [
            "analyze", "examine", "evaluate", "assess", "review"
        ]),
        "explanation": (r"(explain|describe|what is|how does|why)", [
            "explain", "describe", "clarify", "elaborate", "detail"
        ]),
        "planning": (r"(plan|strategy|approach|method|steps)", [
            "plan", "organize", "prepare", "arrange", "structure"
        ]),
        "research": (r"(research|study|investigate|explore|literature)", [
            "research", "investigate", "study", "explore", "examine"
        ]),
        "translation": (r"(translate|convert|language|meaning|phrase)", [
            "translate", "convert", "transform", "change", "adapt"
        ]),
        "summarization": (r"(summarize|brief|overview|recap|digest)", [
            "summarize", "condense", "shorten", "brief", "synopsis"
        ])
    }
    
    # Check each pattern
    matched_tasks = {}
    for task_type, (pattern, examples) in task_patterns.items():
        # Check for pattern matches
        pattern_matches = len(re.findall(pattern, message, re.IGNORECASE))
        
        # Check for example word matches
        example_matches = sum(1 for example in examples 
                            if example in message.lower())
        
        # Combine scores with pattern matches weighted more heavily
        if pattern_matches > 0 or example_matches > 0:
            matched_tasks[task_type] = (pattern_matches * 2) + example_matches
    
    if matched_tasks:
        # Return task type with highest score
        return max(matched_tasks.items(), key=lambda x: x[1])[0]
            
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