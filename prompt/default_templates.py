"""
Default configurations for different prompt types and tasks.
"""

def get_role_template(role: str) -> str:
    """Get the template for a specific role"""
    return ROLE_TEMPLATES.get(role, ROLE_TEMPLATES["Assistant"])

def get_prompt_technique(technique: str) -> str:
    """Get the template for a specific prompt technique"""
    return PROMPT_TECHNIQUES.get(technique, PROMPT_TECHNIQUES["zero_shot"])

def get_task_parameters(task_type: str) -> dict:
    """Get the parameters for a specific task type"""
    return TASK_PARAMETERS.get(task_type, TASK_PARAMETERS["default"])

# Default role-based templates
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

# Default parameters by task type
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

# Prompt techniques with templates
PROMPT_TECHNIQUES = {
    "zero_shot": "{query}",
    "few_shot": "Here are some examples:\n\nExample 1: [First example]\nAnswer: [First answer]\n\nExample 2: [Second example]\nAnswer: [Second answer]\n\nNow answer this: {query}",
    "chain_of_thought": "Think through this step-by-step: {query}\n\nLet's break this down into parts and solve methodically.",
    "self_consistency": "Consider multiple approaches to solve this problem: {query}\n\nApproach 1:\nApproach 2:\nApproach 3:\n\nBased on these approaches, the most consistent answer is:",
    "tree_of_thought": "Let's explore different reasoning paths for: {query}\n\nPath A:\n  Step A1\n  Step A2\n  Outcome A\n\nPath B:\n  Step B1\n  Step B2\n  Outcome B\n\nEvaluating these paths, the best solution is:",
    "role_playing": "You are an expert {role}. {query}",
    "structured_output": "Provide your answer in the following format:\n\n1. Initial thoughts\n2. Analysis\n3. Solution steps\n4. Final answer\n5. Verification\n\n{query}",
    "socratic": "To answer: {query}\n\nLet me ask myself some clarifying questions:\n1. What are the key components of this problem?\n2. What information do I need to solve it?\n3. What assumptions am I making?\n4. How can I verify my answer?"
}