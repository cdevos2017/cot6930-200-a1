"""
Advanced Prompt Engineering Techniques for Requirements Analysis.

This module contains multi-level prompt engineering techniques specifically designed
for requirements elicitation, analysis, and refinement.
"""

from typing import Dict, List, Optional, Union, Any, Tuple

# Level-1 techniques use a meta-prompt to generate more effective prompts
L1_TECHNIQUES = {
    "meta_prompt": {
        "description": "Uses a prompt to generate another prompt for requirement analysis",
        "template": """
        Create an effective prompt that will elicit comprehensive and structured requirements for this task:

        {query}

        Your prompt should:
        1. Ask clarifying questions about scope and constraints
        2. Guide the analysis through different requirement categories
        3. Help identify both explicit and implicit requirements
        4. Ensure requirements are testable and measurable
        """
    },
    "stakeholder_perspective": {
        "description": "Analyzes requirements from multiple stakeholder perspectives",
        "template": """
        Analyze the following requirement task from three different stakeholder perspectives:

        {query}

        For each perspective (End User, Business Owner, Technical Team):
        1. What are the key priorities and concerns?
        2. What specific requirements would they emphasize?
        3. What potential conflicts might arise between perspectives?
        4. How can these requirements be reconciled into a comprehensive specification?
        """
    },
    "quality_criteria": {
        "description": "Structures requirements using quality attributes",
        "template": """
        Develop detailed requirements for the following task by systematically addressing quality attributes:

        {query}

        For each of these quality attributes:
        - Functionality: What should the system do?
        - Usability: How will users interact with it?
        - Reliability: How should it perform under stress?
        - Performance: What are the speed/efficiency requirements?
        - Security: What protections should be in place?
        - Maintainability: How can it be designed for future change?

        Format each requirement to be specific, measurable, achievable, relevant, and time-bound (SMART).
        """
    }
}

# Level-2 techniques use a chain of prompts with state maintained between steps
L2_TECHNIQUES = {
    "refinement_chain": {
        "description": "Uses a chain of prompts to progressively refine requirements",
        "templates": [
            # First step: Initial requirements gathering
            """
            Generate an initial set of requirements based on this task:
            
            {query}
            
            Focus on capturing the core functionality and main user needs.
            List at least 5 high-level requirements.
            """,
            
            # Second step: Analysis and elaboration
            """
            Analyze the following initial requirements:
            
            {previous_response}
            
            For each requirement:
            1. Identify any ambiguities or missing details
            2. Add acceptance criteria
            3. Consider edge cases and exceptions
            4. Categorize as functional or non-functional
            """,
            
            # Third step: Quality check and refinement
            """
            Review and refine these analyzed requirements:
            
            {previous_response}
            
            For each requirement:
            1. Ensure it's specific, measurable, achievable, relevant, and time-bound (SMART)
            2. Remove any redundancies or conflicts
            3. Add priority levels (High/Medium/Low)
            4. Provide a rationale for each requirement
            
            Present the final requirements in a structured format suitable for technical documentation.
            """
        ]
    },
    "divergent_convergent": {
        "description": "First diverges to explore many possible requirements, then converges to select the best ones",
        "templates": [
            # First step: Divergent thinking
            """
            For the following task, generate as many potential requirements as possible through divergent thinking:
            
            {query}
            
            Consider:
            - Different user types and their needs
            - Various use cases and scenarios
            - Functional requirements
            - Non-functional requirements
            - Business rules and constraints
            - Technical considerations
            
            Don't filter or evaluate at this stage - aim for quantity and diversity.
            """,
            
            # Second step: Evaluation
            """
            Review the following list of potential requirements:
            
            {previous_response}
            
            Evaluate each requirement based on:
            1. Value to users and business
            2. Technical feasibility
            3. Alignment with project scope
            4. Potential implementation complexity
            
            For each requirement, provide a score of 1-5 in each category and brief justification.
            """,
            
            # Third step: Convergent thinking
            """
            Based on your evaluation:
            
            {previous_response}
            
            1. Select the top 10-15 most valuable and feasible requirements
            2. Organize them into a coherent specification
            3. Identify dependencies between requirements
            4. Suggest an implementation priority order
            
            Present the final requirement specification in a clear, structured format.
            """
        ]
    },
    "adverse_analysis": {
        "description": "Uses adversarial thinking to identify missing requirements and edge cases",
        "templates": [
            # First step: Generate baseline requirements
            """
            Create a baseline set of requirements for:
            
            {query}
            
            Focus on the happy path scenarios and core functionality.
            """,
            
            # Second step: Adversarial analysis
            """
            Analyze these baseline requirements from an adversarial perspective:
            
            {previous_response}
            
            For each requirement:
            1. How could it fail or be misinterpreted?
            2. What edge cases are not covered?
            3. How might users misuse or abuse this feature?
            4. What security vulnerabilities might exist?
            5. What performance issues could arise?
            
            Identify at least 3 issues for each requirement.
            """,
            
            # Third step: Refinement and hardening
            """
            Based on the adversarial analysis:
            
            {previous_response}
            
            1. Refine each original requirement to address the identified issues
            2. Add new requirements to cover gaps and edge cases
            3. Include explicit error handling and validation requirements
            4. Specify security and performance safeguards
            
            Present the improved, hardened requirements specification.
            """
        ]
    }
}

def get_l1_technique_names() -> List[str]:
    """Get a list of available Level-1 technique names."""
    return list(L1_TECHNIQUES.keys())

def get_l2_technique_names() -> List[str]:
    """Get a list of available Level-2 technique names."""
    return list(L2_TECHNIQUES.keys())

def get_technique_description(technique_name: str) -> str:
    """
    Get the description of a specific technique.
    
    Args:
        technique_name: Name of the technique
        
    Returns:
        Description of the technique
        
    Raises:
        ValueError: If the technique name is not recognized
    """
    if technique_name in L1_TECHNIQUES:
        return L1_TECHNIQUES[technique_name]["description"]
    elif technique_name in L2_TECHNIQUES:
        return L2_TECHNIQUES[technique_name]["description"]
    else:
        raise ValueError(f"Unknown technique: {technique_name}")

def apply_l1_technique(query: str, technique_name: str) -> str:
    """
    Apply a Level-1 requirement analysis technique to a query.
    
    Args:
        query: The original requirements task/query
        technique_name: Name of the Level-1 technique to apply
        
    Returns:
        Formatted prompt using the specified technique
        
    Raises:
        ValueError: If the technique name is not recognized
    """
    if technique_name not in L1_TECHNIQUES:
        raise ValueError(f"Unknown L1 technique: {technique_name}")
    
    technique = L1_TECHNIQUES[technique_name]
    return technique["template"].format(query=query)

def get_l2_technique_steps(technique_name: str) -> int:
    """
    Get the number of steps in a Level-2 technique.
    
    Args:
        technique_name: Name of the Level-2 technique
        
    Returns:
        Number of steps in the technique
        
    Raises:
        ValueError: If the technique name is not recognized
    """
    if technique_name not in L2_TECHNIQUES:
        raise ValueError(f"Unknown L2 technique: {technique_name}")
    
    return len(L2_TECHNIQUES[technique_name]["templates"])

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
        
    Raises:
        ValueError: If the technique name is not recognized or the step is invalid
    """
    if technique_name not in L2_TECHNIQUES:
        raise ValueError(f"Unknown L2 technique: {technique_name}")
    
    technique = L2_TECHNIQUES[technique_name]
    
    if step < 0 or step >= len(technique["templates"]):
        raise ValueError(f"Invalid step {step} for technique {technique_name}. "
                         f"Valid steps are 0-{len(technique['templates'])-1}.")
    
    template = technique["templates"][step]
    
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
        
    Raises:
        ValueError: If the technique name is not recognized
    """
    if technique_name not in L2_TECHNIQUES:
        raise ValueError(f"Unknown L2 technique: {technique_name}")
    
    technique = L2_TECHNIQUES[technique_name]
    num_steps = len(technique["templates"])
    
    # Initialize default parameters if not provided
    if step_params is None:
        step_params = [{}] * num_steps
    elif len(step_params) != num_steps:
        raise ValueError(f"Parameter list length ({len(step_params)}) must match "
                        f"number of steps ({num_steps})")
    
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