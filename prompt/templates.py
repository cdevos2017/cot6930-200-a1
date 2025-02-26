"""
Templates module.

Contains all templates used in prompt engineering, including role templates,
technique templates, and specialized templates for L1 and L2 techniques.
"""

from typing import Dict, Optional

# Dictionary mapping roles to templates
ROLE_TEMPLATES = {
    # Academic roles
    "Mathematician": "Solve this mathematical problem step-by-step: {query}\n\nShow your reasoning clearly.",
    "Statistician": "Analyze this statistical problem: {query}\n\nProvide a detailed explanation of the statistical concepts involved and show your calculations.",
    "Computer Scientist": "Explain this computer science concept: {query}\n\nBreak down the theory, applications, and provide examples.",
    "Physicist": "Explain this physics problem: {query}\n\nApply the relevant physical laws and show your calculations step-by-step.",
    "Historian": "Analyze this historical event or period: {query}\n\nProvide context, key figures, causes, effects, and significance.",
    "Literature Professor": "Analyze this text or literary concept: {query}\n\nDiscuss themes, literary devices, historical context, and significance.",
    "Biologist": "Explain this biological process or concept: {query}\n\nDescribe the mechanisms, components, and significance in detail.",
    
    # Technical roles
    "Software Engineer": "Write code to solve the following problem:\n{query}\n\nProvide a clear explanation of your implementation.",
    "Data Scientist": "Analyze this dataset/problem: {query}\n\nOutline your approach, methods, and provide insights from the data.",
    "Systems Architect": "Design a system architecture for: {query}\n\nExplain components, interactions, trade-offs, and rationale.",
    "Database Administrator": "Address this database challenge: {query}\n\nProvide SQL queries, schema designs, or optimization strategies as needed.",
    "DevOps Engineer": "Solve this deployment/infrastructure issue: {query}\n\nProvide configuration examples, scripts, and best practices.",
    "QA Engineer": "Develop a testing strategy for: {query}\n\nOutline test cases, methodologies, and quality assurance approaches.",
    
    # Writing roles
    "Copywriter": "Create compelling copy for: {query}\n\nTailor the tone, style, and messaging to the target audience.",
    "Technical Writer": "Create documentation for: {query}\n\nProvide clear, concise instructions with appropriate technical detail.",
    "Creative Writer": "Write a creative piece based on: {query}\n\nFocus on narrative, character development, and engaging storytelling.",
    "Journalist": "Write a news article about: {query}\n\nInclude the who, what, when, where, why, and how. Maintain objectivity and cite sources.",
    "Essay Writer": "Write an essay on: {query}\n\nDevelop a clear thesis, supporting arguments, and thoughtful conclusion.",
    
    # Business roles
    "Business Analyst": "Analyze this business scenario: {query}\n\nProvide insights, identify opportunities, and suggest improvements.",
    "Product Manager": "Develop a product strategy for: {query}\n\nAddress market fit, user needs, competitive landscape, and implementation approach.",
    "Marketing Strategist": "Create a marketing strategy for: {query}\n\nIdentify target audience, positioning, channels, and metrics for success.",
    "Financial Analyst": "Perform financial analysis on: {query}\n\nProvide calculations, interpretations, and strategic recommendations.",
    "Management Consultant": "Provide consulting advice for: {query}\n\nAnalyze the situation, identify key issues, and recommend solutions.",
    
    # Educational roles
    "Teacher": "Create a lesson plan for: {query}\n\nInclude learning objectives, activities, assessments, and differentiation strategies.",
    "Tutor": "Explain this concept for a student: {query}\n\nUse simple language, analogies, and examples to aid understanding.",
    "Professor": "Explain the following concept in clear, simple terms:\n{query}",
    "Career Counselor": "Provide career advice regarding: {query}\n\nConsider skills, interests, market trends, and practical next steps.",
    
    # Research roles
    "Research Scientist": "Design a research methodology for: {query}\n\nOutline hypotheses, methods, controls, analysis techniques, and limitations.",
    "Literature Reviewer": "Synthesize research on: {query}\n\nIdentify key findings, contradictions, gaps, and future directions.",
    "Grant Writer": "Outline a grant proposal for: {query}\n\nAddress significance, innovation, approach, and expected outcomes.",
    
    # Specialized analysis
    "Legal Analyst": "Analyze this legal question: {query}\n\nDiscuss relevant laws, precedents, arguments, and potential outcomes.",
    "Policy Analyst": "Analyze this policy issue: {query}\n\nConsider stakeholders, trade-offs, evidence, and recommendations.",
    "Ethics Advisor": "Provide ethical analysis of: {query}\n\nConsider multiple perspectives, principles, consequences, and recommendations.",
    
    # General roles
    "Explainer": "Explain this concept in simple terms: {query}\n\nUse analogies, examples, and clear language.",
    "Planner": "Create a detailed plan for: {query}\n\nInclude steps, resources, timeline, and potential challenges.",
    "Analyzer": "Analyze the following: {query}\n\nBreak down components, identify patterns, and provide insights.",
    "Summarizer": "Summarize the following: {query}\n\nCapture the key points, main arguments, and significant details.",
    "Assistant": "{query}"
}

# Basic prompt technique templates
TECHNIQUE_TEMPLATES = {
    "zero_shot": "{query}",
    "few_shot": "Here are some examples:\n\nExample 1: [First example]\nAnswer: [First answer]\n\nExample 2: [Second example]\nAnswer: [Second answer]\n\nNow answer this: {query}",
    "chain_of_thought": "Think through this step-by-step: {query}\n\nLet's break this down into parts and solve methodically.",
    "self_consistency": "Consider multiple approaches to solve this problem: {query}\n\nApproach 1:\nApproach 2:\nApproach 3:\n\nBased on these approaches, the most consistent answer is:",
    "tree_of_thought": "Let's explore different reasoning paths for: {query}\n\nPath A:\n  Step A1\n  Step A2\n  Outcome A\n\nPath B:\n  Step B1\n  Step B2\n  Outcome B\n\nEvaluating these paths, the best solution is:",
    "role_playing": "You are an expert {role}. {query}",
    "structured_output": "Provide your answer in the following format:\n\n1. Initial thoughts\n2. Analysis\n3. Solution steps\n4. Final answer\n5. Verification\n\n{query}",
    "socratic": "To answer: {query}\n\nLet me ask myself some clarifying questions:\n1. What are the key components of this problem?\n2. What information do I need to solve it?\n3. What assumptions am I making?\n4. How can I verify my answer?",
    "guided_conversation": "Let's discuss this step by step. I'll guide you through analyzing: {query}\n\nFirst, let's clarify the scope and objectives. Then we'll explore key considerations, and finally develop a detailed response."
}

# Level-1 technique templates
L1_TECHNIQUE_TEMPLATES = {
    "meta_prompt": """
    Create an effective prompt that will elicit comprehensive and structured requirements for this task:

    {query}

    Your prompt should:
    1. Ask clarifying questions about scope and constraints
    2. Guide the analysis through different requirement categories
    3. Help identify both explicit and implicit requirements
    4. Ensure requirements are testable and measurable
    """,
    
    "stakeholder_perspective": """
    Analyze the following requirement task from three different stakeholder perspectives:

    {query}

    For each perspective (End User, Business Owner, Technical Team):
    1. What are the key priorities and concerns?
    2. What specific requirements would they emphasize?
    3. What potential conflicts might arise between perspectives?
    4. How can these requirements be reconciled into a comprehensive specification?
    """,
    
    "quality_criteria": """
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

# Level-2 technique templates (each technique has multiple step templates)
L2_TECHNIQUE_TEMPLATES = {
    "refinement_chain": [
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
    ],
    
    "divergent_convergent": [
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
    ],
    
    "adverse_analysis": [
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

# Template access functions

def get_role_template(role: str) -> str:
    """
    Get the template for a specific role.
    
    Args:
        role: Role name
    
    Returns:
        Template string for the role
    """
    return ROLE_TEMPLATES.get(role, ROLE_TEMPLATES["Assistant"])

def get_technique_template(technique_name: str) -> str:
    """
    Get the template for a specific technique.
    
    Args:
        technique_name: Name of the technique
        
    Returns:
        Template string for the technique
    """
    if not technique_name:
        return "{query}"  # Return default template for None
        
    if technique_name in TECHNIQUE_TEMPLATES:
        return TECHNIQUE_TEMPLATES[technique_name]
    else:
        # Print warning but don't raise error, return default template
        print(f"Warning: Unknown technique template: {technique_name}. Using default template.")
        return "{query}"

def get_l1_technique_template(technique_name: str) -> str:
    """
    Get the template for a Level-1 technique.
    
    Args:
        technique_name: Name of the Level-1 technique
        
    Returns:
        Template string for the technique
    """
    if technique_name in L1_TECHNIQUE_TEMPLATES:
        return L1_TECHNIQUE_TEMPLATES[technique_name]
    else:
        print(f"Warning: Unknown L1 technique: {technique_name}. Using default template.")
        return "{query}"

def get_l2_technique_step_template(technique_name: str, step: int) -> Optional[str]:
    """
    Get the template for a specific step in a Level-2 technique.
    
    Args:
        technique_name: Name of the Level-2 technique
        step: Step index (0-based)
        
    Returns:
        Template string for the step or None if not found
    """
    if technique_name not in L2_TECHNIQUE_TEMPLATES:
        print(f"Warning: Unknown L2 technique: {technique_name}")
        return None
        
    templates = L2_TECHNIQUE_TEMPLATES[technique_name]
    
    if step < 0 or step >= len(templates):
        print(f"Warning: Invalid step {step} for technique {technique_name}")
        return None
        
    return templates[step]

def get_l2_technique_steps_count(technique_name: str) -> int:
    """
    Get the number of steps in a Level-2 technique.
    
    Args:
        technique_name: Name of the Level-2 technique
        
    Returns:
        Number of steps in the technique
    """
    if technique_name not in L2_TECHNIQUE_TEMPLATES:
        return 0
    
    return len(L2_TECHNIQUE_TEMPLATES[technique_name])

def list_all_templates() -> Dict[str, Dict]:
    """
    Return a structured dictionary of all available templates.
    
    Returns:
        Dictionary with all template categories and counts
    """
    return {
        "role_templates": {
            "count": len(ROLE_TEMPLATES),
            "available": list(ROLE_TEMPLATES.keys())
        },
        "technique_templates": {
            "count": len(TECHNIQUE_TEMPLATES),
            "available": list(TECHNIQUE_TEMPLATES.keys())
        },
        "l1_technique_templates": {
            "count": len(L1_TECHNIQUE_TEMPLATES),
            "available": list(L1_TECHNIQUE_TEMPLATES.keys())
        },
        "l2_technique_templates": {
            "count": len(L2_TECHNIQUE_TEMPLATES),
            "available": list(L2_TECHNIQUE_TEMPLATES.keys())
        }
    }