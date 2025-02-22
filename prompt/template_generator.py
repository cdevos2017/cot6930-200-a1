from .analyzers import call_llm_for_analysis
from .analyzers import parse_json_response

def determine_template(message):
    """Analyze message and return appropriate template configuration"""
    
    # Example logic - you could make this much more sophisticated
    if any(term in message.lower() for term in ['calculate', 'solve', '*', '/', '+', '-', 'log', 'sin']):
        return {
            "role": "Mathematician",
            "template": "Solve this mathematical problem step-by-step: {query}\n\nShow your reasoning clearly.",
            "parameters": {"temperature": 0.2, "num_ctx": 2048}
        }
    elif any(term in message.lower() for term in ['code', 'function', 'algorithm', 'programming']):
        return {
            "role": "Software Engineer",
            "template": "Write code to solve the following problem:\n{query}\n\nProvide a clear explanation of your implementation.",
            "parameters": {"temperature": 0.3, "num_ctx": 4096}
        }
    elif any(term in message.lower() for term in ['explain', 'describe', 'what is']):
        return {
            "role": "Professor",
            "template": "Explain the following concept in clear, simple terms:\n{query}",
            "parameters": {"temperature": 0.7, "num_ctx": 2048}
        }
    else:
        # Default template
        return {
            "role": "Assistant",
            "template": "{query}",
            "parameters": {"temperature": 0.7, "num_ctx": 1024}
        }

def get_meta_template(message):
    meta_prompt = f"""
    Analyze this user query: "{message}"
    
    Determine the most appropriate role and prompt template to handle this query.
    Return your response in this JSON format:
    {{
        "role": "[appropriate expert role]",
        "template": "[prompt template with {{query}} placeholder]",
        "parameters": {{
            "temperature": [appropriate value],
            "num_ctx": [appropriate value],
            "num_predict": [appropriate value]
        }}
    }}
    """
    
    # Call a separate LLM to analyze and return template configuration
    meta_response = call_llm_for_analysis(meta_prompt)
    return parse_json_response(meta_response)