# research/framework.py

from typing import List, Dict, Any
from dataclasses import dataclass
from statistics import mean, stdev
from prompt.prompt_refiner import iterative_prompt_refinement
from prompt.template_generator import determine_template, detect_role, detect_task_type, detect_prompt_technique

@dataclass
class TestCase:
    query: str
    category: str
    expected_role: str
    expected_technique: str
    description: str

class PromptResearchFramework:
    """Framework for conducting prompt engineering research"""
    
    def __init__(self):
        # Define test cases
        self.test_cases = [
            TestCase(
                query="Write a Python function to calculate the Fibonacci sequence",
                category="coding",
                expected_role="Software Engineer",
                expected_technique="chain_of_thought",
                description="Algorithm implementation task"
            ),
            TestCase(
                query="Explain why the sky is blue",
                category="explanation",
                expected_role="Physicist",
                expected_technique="socratic",
                description="Scientific explanation task"
            ),
            TestCase(
                query="Analyze the impact of social media on mental health",
                category="analysis",
                expected_role="Psychologist",
                expected_technique="tree_of_thought",
                description="Complex analysis task"
            ),
            TestCase(
                query="Create a marketing strategy for a new eco-friendly product",
                category="business",
                expected_role="Business Analyst",
                expected_technique="structured_output",
                description="Strategic planning task"
            ),
            TestCase(
                query="Solve this equation: 3x^2 + 2x - 5 = 0",
                category="math",
                expected_role="Mathematician",
                expected_technique="chain_of_thought",
                description="Mathematical problem-solving task"
            )
        ]
        
        # Define technique variations to test
        self.techniques = [
            "chain_of_thought",
            "tree_of_thought",
            "structured_output",
            "socratic",
            "role_playing"
        ]
        
        # Define parameter variations
        self.parameter_sets = [
            {"temperature": 0.2, "num_ctx": 2048, "num_predict": 1024},
            {"temperature": 0.5, "num_ctx": 2048, "num_predict": 1024},
            {"temperature": 0.7, "num_ctx": 2048, "num_predict": 1024},
            {"temperature": 0.2, "num_ctx": 4096, "num_predict": 2048},
            {"temperature": 0.5, "num_ctx": 4096, "num_predict": 2048}
        ]
    
    def run_experiment(self, test_case: TestCase, technique: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single experiment with given parameters"""
        try:
            # First, get base template configuration
            template_config = determine_template(test_case.query)
            
            # Override technique for experiment
            template_config["technique"] = technique
            
            # Update parameters
            template_config["parameters"].update(parameters)
            
            # Run refinement with this configuration
            result = iterative_prompt_refinement(
                test_case.query,
                min_iterations=3,
                threshold=0.9
            )
            
            if result:
                # Add experiment metadata
                result.update({
                    "original_query": test_case.query,
                    "technique_used": technique,
                    "parameters_used": parameters,
                    "expected_role": test_case.expected_role,
                    "category": test_case.category,
                    "detected_role": template_config.get("role"),
                    "detected_task_type": template_config.get("task_type"),
                    "template_used": template_config.get("template")
                })
            
            return result
            
        except Exception as e:
            print(f"Error in experiment: {str(e)}")
            return None
    
    def analyze_experiment_accuracy(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze accuracy of our template detection"""
        if not results:
            return {
                "role_detection_accuracy": 0.0,
                "technique_detection_accuracy": 0.0,
                "task_type_detection_accuracy": 0.0
            }
            
        role_matches = sum(1 for r in results 
                         if r.get("detected_role") == r.get("expected_role", ""))
        technique_matches = sum(1 for r in results 
                              if r.get("technique_used") == r.get("expected_technique", ""))
        
        return {
            "role_detection_accuracy": role_matches / len(results),
            "technique_detection_accuracy": technique_matches / len(results)
        }
    
    def run_full_evaluation(self) -> List[Dict[str, Any]]:
        """Run complete evaluation across all test cases and variations"""
        results = []
        
        for test_case in self.test_cases:
            print(f"\nEvaluating: {test_case.description}")
            
            # Test each technique
            for technique in self.techniques:
                print(f"\nTesting technique: {technique}")
                
                # Test each parameter set
                for params in self.parameter_sets:
                    print(f"Parameters: {params}")
                    
                    result = self.run_experiment(test_case, technique, params)
                    if result:
                        results.append(result)
        
        return results
    
    def analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze experimental results"""
        if not results:
            return {
                "error": "No successful experiments to analyze",
                "technique_performance": {},
                "parameter_impact": {},
                "detection_accuracy": {
                    "role_detection_accuracy": 0.0,
                    "technique_detection_accuracy": 0.0
                }
            }
            
        analysis = {
            "technique_performance": {},
            "parameter_impact": {},
            "detection_accuracy": self.analyze_experiment_accuracy(results)
        }
        
        # Analyze technique performance
        for technique in self.techniques:
            technique_results = [r for r in results if r.get("technique_used") == technique]
            if technique_results:
                quality_scores = [r.get("final_quality", 0) for r in technique_results]
                iterations = [r.get("iterations_used", 0) for r in technique_results]
                
                analysis["technique_performance"][technique] = {
                    "avg_quality": mean(quality_scores),
                    "std_quality": stdev(quality_scores) if len(quality_scores) > 1 else 0,
                    "avg_iterations": mean(iterations)
                }
        
        # Analyze parameter impact
        for params in self.parameter_sets:
            param_key = f"temp_{params['temperature']}_ctx_{params['num_ctx']}"
            param_results = [r for r in results 
                           if r.get("parameters_used", {}).get("temperature") == params["temperature"]
                           and r.get("parameters_used", {}).get("num_ctx") == params["num_ctx"]]
            
            if param_results:
                quality_scores = [r.get("final_quality", 0) for r in param_results]
                time_taken = [r.get("time_taken", 0) for r in param_results]
                
                analysis["parameter_impact"][param_key] = {
                    "avg_quality": mean(quality_scores),
                    "avg_time": mean(time_taken)
                }
                if len(quality_scores) > 1:
                    analysis["parameter_impact"][param_key]["std_quality"] = stdev(quality_scores)
                    analysis["parameter_impact"][param_key]["std_time"] = stdev(time_taken)
                    
        return analysis