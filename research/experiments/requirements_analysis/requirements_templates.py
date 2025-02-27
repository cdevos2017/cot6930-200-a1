# requirements_templates.py
"""Requirements-specific templates that extend the base templates."""

# Requirements-specific role templates
REQUIREMENTS_ROLE_TEMPLATES = {
    "Requirements Engineer": "Analyze the following requirements task as a requirements engineer: {query}\n\nGenerate a comprehensive list of requirements, considering both functional and non-functional aspects.",
    "Business Analyst": "Analyze the following requirements task as a business analyst: {query}\n\nTranslate business needs into clear, structured requirements with appropriate acceptance criteria.",
    "Systems Analyst": "Analyze the following requirements task as a systems analyst: {query}\n\nDevelop detailed system requirements that address both technical and business needs.",
    "Product Manager": "Analyze the following requirements task as a product manager: {query}\n\nCreate a prioritized set of requirements that maximize business value and user satisfaction."
}

# Requirements-specific technique templates
REQUIREMENTS_TECHNIQUE_TEMPLATES = {
    "chain_of_thought": "Think through this requirements task step-by-step: {query}\n\n1. Identify stakeholders and their needs\n2. Define the scope and boundaries\n3. List functional requirements\n4. Consider non-functional requirements\n5. Define acceptance criteria\n\nPresent the final requirements in a structured, prioritized list.",
    
    "tree_of_thought": "Let's explore different perspectives for this requirements task: {query}\n\nUser Perspective:\n- What do users need to accomplish?\n- What are their pain points?\n- What would improve their experience?\n\nBusiness Perspective:\n- What business goals need to be addressed?\n- What metrics matter for success?\n- What constraints exist?\n\nTechnical Perspective:\n- What system capabilities are needed?\n- What potential technical limitations exist?\n- What performance requirements apply?\n\nBased on these perspectives, produce a comprehensive, prioritized requirements list.",
    
    "structured_output": "Analyze the following requirements task: {query}\n\nPresent your requirements in this structured format:\n\n1. OVERVIEW\n   - Problem statement\n   - Scope\n\n2. FUNCTIONAL REQUIREMENTS\n   - [Prioritized list of functional requirements]\n\n3. NON-FUNCTIONAL REQUIREMENTS\n   - [Categorized list of non-functional requirements]\n\n4. CONSTRAINTS\n   - [List of constraints]\n\n5. ASSUMPTIONS\n   - [List of assumptions]"
}

def get_requirements_role_template(role: str) -> str:
    """Get a requirements-specific template for a role."""
    return REQUIREMENTS_ROLE_TEMPLATES.get(role, "{query}")

def get_requirements_technique_template(technique: str) -> str:
    """Get a requirements-specific template for a technique."""
    return REQUIREMENTS_TECHNIQUE_TEMPLATES.get(technique, "{query}")

def apply_requirements_technique(message: str, technique: str, role: str = None) -> str:
    """Apply a requirements-specific technique to a message."""
    technique_template = get_requirements_technique_template(technique)
    role_template = get_requirements_role_template(role) if role else "{query}"
    
    # Apply role template first
    intermediate = role_template.format(query=message)
    
    # Then apply technique template
    result = technique_template.format(query=intermediate)
    
    return result