"""
Automated Prompt Engineering Research Framework
"""
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from statistics import mean, stdev
# research/framework.py
from prompt.prompt_refiner import iterative_prompt_refinement

@dataclass
class TestCase:
    query: str
    category: str
    expected_role: str
    expected_technique: str
    description: str

@dataclass
class ExperimentResult:
    query: str
    technique: str
    parameters: Dict[str, Any]
    quality_score: float
    iterations_used: int
    time_taken: float
    final_prompt: str
    role_used: str
    reasoning: str

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
        
    def run_experiment(self, test_case: TestCase, technique: str, 
                      parameters: Dict[str, Any]) -> ExperimentResult:
        """Run a single experiment with given parameters"""
        start_time = time.time()
        
        # Configure the refinement process
        config = {
            "technique": technique,
            "min_iterations": 3,
            "threshold": 0.9,
            "parameters": parameters
        }
        
        # Run the refinement
        result = iterative_prompt_refinement(test_case.query, **config)
        
        # Calculate time taken
        time_taken = time.time() - start_time
        
        return ExperimentResult(
            query=test_case.query,
            technique=technique,
            parameters=parameters,
            quality_score=result.get("final_quality", 0.0),
            iterations_used=result.get("iterations_used", 0),
            time_taken=time_taken,
            final_prompt=result.get("final_prompt", ""),
            role_used=result.get("role", ""),
            reasoning=result.get("reasoning", "")
        )
    
    def run_full_evaluation(self) -> List[ExperimentResult]:
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
                    
                    try:
                        result = self.run_experiment(test_case, technique, params)
                        results.append(result)
                        
                        print(f"Quality Score: {result.quality_score:.2f}")
                        print(f"Time Taken: {result.time_taken:.2f}s")
                        print(f"Iterations: {result.iterations_used}")
                        
                    except Exception as e:
                        print(f"Error in experiment: {e}")
        
        return results
    
    def analyze_results(self, results: List[ExperimentResult]) -> Dict[str, Any]:
        """Analyze experimental results"""
        analysis = {
            "technique_performance": {},
            "parameter_impact": {},
            "role_accuracy": {},
            "time_efficiency": {},
            "quality_distribution": {}
        }
        
        # Analyze technique performance
        for technique in self.techniques:
            technique_results = [r for r in results if r.technique == technique]
            if technique_results:
                analysis["technique_performance"][technique] = {
                    "avg_quality": mean(r.quality_score for r in technique_results),
                    "std_quality": stdev(r.quality_score for r in technique_results),
                    "avg_iterations": mean(r.iterations_used for r in technique_results)
                }
        
        # Analyze parameter impact
        for params in self.parameter_sets:
            param_key = f"temp_{params['temperature']}_ctx_{params['num_ctx']}"
            param_results = [r for r in results 
                           if r.parameters["temperature"] == params["temperature"]
                           and r.parameters["num_ctx"] == params["num_ctx"]]
            if param_results:
                analysis["parameter_impact"][param_key] = {
                    "avg_quality": mean(r.quality_score for r in param_results),
                    "avg_time": mean(r.time_taken for r in param_results)
                }
        
        # Calculate role matching accuracy
        role_matches = 0
        for test_case in self.test_cases:
            case_results = [r for r in results if r.query == test_case.query]
            for result in case_results:
                if result.role_used == test_case.expected_role:
                    role_matches += 1
        
        analysis["role_accuracy"] = role_matches / len(results)
        
        return analysis
    
    def generate_report(self, results: List[ExperimentResult], 
                       analysis: Dict[str, Any]) -> str:
        """Generate a research report from the results"""
        report = """
# Automated Prompt Engineering: Experimental Results

## Overview
This report presents the findings from our experimental evaluation of various 
prompt engineering techniques and their effectiveness across different types of queries.

## Methodology
We tested {num_techniques} different techniques across {num_test_cases} test cases,
with {num_param_sets} parameter variations for each combination.

## Key Findings

### 1. Technique Performance
""".format(
            num_techniques=len(self.techniques),
            num_test_cases=len(self.test_cases),
            num_param_sets=len(self.parameter_sets)
        )
        
        # Add technique performance details
        for technique, metrics in analysis["technique_performance"].items():
            report += f"\n{technique}:\n"
            report += f"- Average Quality: {metrics['avg_quality']:.2f}\n"
            report += f"- Quality StdDev: {metrics['std_quality']:.2f}\n"
            report += f"- Average Iterations: {metrics['avg_iterations']:.1f}\n"
        
        # Add parameter impact analysis
        report += "\n### 2. Parameter Impact\n"
        for param_key, metrics in analysis["parameter_impact"].items():
            report += f"\n{param_key}:\n"
            report += f"- Average Quality: {metrics['avg_quality']:.2f}\n"
            report += f"- Average Time: {metrics['avg_time']:.2f}s\n"
        
        # Add role accuracy
        report += f"\n### 3. Role Selection Accuracy\n"
        report += f"Overall role matching accuracy: {analysis['role_accuracy']:.2%}\n"
        
        return report