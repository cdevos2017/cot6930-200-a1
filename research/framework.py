# research/framework.py
import time
from typing import List, Dict, Any, Optional
from statistics import stdev
from prompt.prompt_refiner import iterative_prompt_refinement
from prompt.template_generator import determine_template
from prompt.utils import format_prompt_with_template
from research.test_cases import TestCase, STANDARD_TEST_CASES

class PromptResearchFramework:
    """Framework for conducting prompt engineering research"""
    
    def __init__(self, test_cases: Optional[List[TestCase]] = None):
        """
        Initialize the research framework
        
        Args:
            test_cases (List[TestCase], optional): Test cases to use for evaluation.
                If None, default to standard test cases.
        """
        # Use provided test cases or default to standard ones
        self.test_cases = test_cases if test_cases is not None else STANDARD_TEST_CASES
        
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
    
    def set_test_cases(self, test_cases: List[TestCase]) -> None:
        """
        Set the test cases to use for evaluation
        
        Args:
            test_cases (List[TestCase]): Test cases to use
        """
        self.test_cases = test_cases
    
    def set_techniques(self, techniques: List[str]) -> None:
        """
        Set the techniques to evaluate
        
        Args:
            techniques (List[str]): Techniques to test
        """
        self.techniques = techniques
    
    def set_parameter_sets(self, parameter_sets: List[Dict[str, Any]]) -> None:
        """
        Set the parameter sets to evaluate
        
        Args:
            parameter_sets (List[Dict[str, Any]]): Parameter sets to test
        """
        self.parameter_sets = parameter_sets
    
    def run_experiment(self, test_case: TestCase, technique: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()  # Start timer
        """Run a single experiment with given parameters and robust error handling"""
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
                # Format the template with the actual query
                template = template_config.get("template", "{query}")
                
                # Format the template with the query and role
                formatted_template = format_prompt_with_template(
                    template,
                    test_case.query,
                    role=template_config.get("role"),
                    technique=technique
                )
                
                # Add experiment metadata
                result.update({
                    "original_query": test_case.query,
                    "technique_used": technique,
                    "parameters_used": parameters,
                    "expected_role": test_case.expected_role,
                    "category": test_case.category,
                    "detected_role": template_config.get("role"),
                    "detected_task_type": template_config.get("task_type"),
                    "template_used": formatted_template  # Use the formatted template
                })
            end_time = time.time()  # End timer
            time_taken = end_time - start_time
            
            result["time_taken"] = time_taken
            # Ensure we return a dictionary
            return result if result else {}
                
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error in experiment: {str(e)}")
            return {
                "error": str(e),
                "technique_used": technique,
                "parameters_used": parameters,
                "query": test_case.query,
                "category": test_case.category,
                "expected_role": test_case.expected_role
            }
    
    def analyze_experiment_accuracy(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze accuracy of our template detection with error handling"""
        if not results:
            return {
                "role_detection_accuracy": 0.0,
                "technique_detection_accuracy": 0.0,
                "task_type_detection_accuracy": 0.0
            }
            
        # Count valid matches with error handling
        role_matches = 0
        technique_matches = 0
        valid_role_results = 0
        valid_technique_results = 0
        
        for r in results:
            # Check role matches
            if "detected_role" in r and "expected_role" in r:
                valid_role_results += 1
                if r["detected_role"] == r["expected_role"]:
                    role_matches += 1
                    
            # Check technique matches
            if "technique_used" in r and "expected_technique" in r:
                valid_technique_results += 1
                if r["technique_used"] == r["expected_technique"]:
                    technique_matches += 1
            
        # Calculate accuracy only if we have valid results
        role_accuracy = role_matches / valid_role_results if valid_role_results > 0 else 0.0
        technique_accuracy = technique_matches / valid_technique_results if valid_technique_results > 0 else 0.0
        
        return {
            "role_detection_accuracy": role_accuracy,
            "technique_detection_accuracy": technique_accuracy
        }
    
    def run_full_evaluation(self) -> List[Dict[str, Any]]:
        """Run complete evaluation across all test cases and variations with robust error handling"""
        results = []
        
        # Create a timestamp for this evaluation
        evaluation_timestamp = time.strftime("%Y%m%d_%H%M%S")
        
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
                        if result:
                            # Ensure the result is a dictionary
                            if not isinstance(result, dict):
                                if hasattr(result, '__dict__'):
                                    result = vars(result)
                                else:
                                    print(f"Warning: Unexpected result type: {type(result)}")
                                    result = {"data": str(result), "type": str(type(result))}
                            
                            # Add evaluation timestamp to the result for traceability
                            result["evaluation_timestamp"] = evaluation_timestamp
                            
                            # Make sure all required fields are present
                            result["technique_used"] = result.get("technique_used", technique)
                            result["parameters_used"] = result.get("parameters_used", params)
                            result["query"] = result.get("query", test_case.query)
                            result["category"] = result.get("category", test_case.category)
                            result["expected_role"] = result.get("expected_role", test_case.expected_role)
                            result["expected_technique"] = result.get("expected_technique", test_case.expected_technique)
                            
                            results.append(result)
                            
                            # Print progress
                            print(f"  Quality score: {result.get('quality_score', 'N/A')}")
                        else:
                            print("  Warning: Empty result returned from experiment")
                            # Add a placeholder result with basic info
                            results.append({
                                "technique_used": technique,
                                "parameters_used": params,
                                "query": test_case.query,
                                "category": test_case.category,
                                "expected_role": test_case.expected_role,
                                "expected_technique": test_case.expected_technique,
                                "evaluation_timestamp": evaluation_timestamp,
                                "error": "Empty result returned from experiment"
                            })
                    except Exception as e:
                        print(f"Error running experiment: {e}")
                        # Add a placeholder result to maintain counts
                        results.append({
                            "error": str(e),
                            "technique_used": technique,
                            "parameters_used": params,
                            "query": test_case.query,
                            "category": test_case.category,
                            "expected_role": test_case.expected_role,
                            "expected_technique": test_case.expected_technique,
                            "evaluation_timestamp": evaluation_timestamp
                        })
        
        # Print summary
        print(f"\nEvaluation completed: {len(results)} experiments run")
        
        return results
    
    def analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze experimental results with robust error handling"""
        # Default empty analysis structure
        empty_analysis = {
            "technique_performance": {},
            "parameter_impact": {},
            "detection_accuracy": {
                "role_detection_accuracy": 0.0,
                "technique_detection_accuracy": 0.0
            },
            "role_accuracy": 0.0,
            "time_metrics": {
                "average_time": 0.0,
                "min_time": 0.0,
                "max_time": 0.0
            }
        }
        
        # Return empty analysis if no results
        if not results:
            print("Warning: No results to analyze")
            return empty_analysis
            
        # Initialize analysis structure
        analysis = {
            "technique_performance": {},
            "parameter_impact": {},
            "detection_accuracy": self.analyze_experiment_accuracy(results),
            "role_accuracy": 0.0,
            "time_metrics": {
                "average_time": 0.0,
                "min_time": 0.0,
                "max_time": 0.0
            }
        }
        
        try:
            # Extract all unique techniques from results
            all_techniques = set()
            for result in results:
                technique = result.get("technique_used")
                if technique:
                    all_techniques.add(technique)
            
            # If no techniques were found, use the default list
            if not all_techniques and hasattr(self, 'techniques'):
                all_techniques = set(self.techniques)
            
            # Analyze technique performance
            for technique in all_techniques:
                technique_results = [r for r in results if r.get("technique_used") == technique]
                if technique_results:
                    try:
                        # Extract quality scores safely
                        quality_scores = []
                        for r in technique_results:
                            score = r.get("final_quality") or r.get("quality_score")
                            if score is not None:
                                try:
                                    quality_scores.append(float(score))
                                except (ValueError, TypeError):
                                    pass
                        
                        # Extract iteration counts safely  
                        iterations = []
                        for r in technique_results:
                            iter_count = r.get("iterations_used")
                            if iter_count is not None:
                                try:
                                    iterations.append(int(iter_count))
                                except (ValueError, TypeError):
                                    pass
                        
                        # Only calculate statistics if we have data
                        if quality_scores:
                            avg_quality = sum(quality_scores) / len(quality_scores)
                            std_quality = stdev(quality_scores) if len(quality_scores) > 1 else 0
                        else:
                            avg_quality = 0.0
                            std_quality = 0.0
                            
                        if iterations:
                            avg_iterations = sum(iterations) / len(iterations)
                        else:
                            avg_iterations = 0.0
                        
                        analysis["technique_performance"][technique] = {
                            "avg_quality": avg_quality,
                            "std_quality": std_quality,
                            "avg_iterations": avg_iterations,
                            "data_points": len(technique_results)
                        }
                    except Exception as e:
                        print(f"Error analyzing technique {technique}: {e}")
                        analysis["technique_performance"][technique] = {
                            "avg_quality": 0.0,
                            "std_quality": 0.0,
                            "avg_iterations": 0.0,
                            "data_points": len(technique_results),
                            "error": str(e)
                        }
            
            # Extract all unique parameter sets
            if hasattr(self, 'parameter_sets'):
                all_parameter_sets = self.parameter_sets
            else:
                # Extract from results
                all_parameter_sets = []
                for result in results:
                    params = result.get("parameters_used")
                    if params and params not in all_parameter_sets:
                        all_parameter_sets.append(params)
            
            # Analyze parameter impact
            for params in all_parameter_sets:
                try:
                    # Create a key for this parameter set
                    if isinstance(params, dict) and "temperature" in params and "num_ctx" in params:
                        param_key = f"temp_{params['temperature']}_ctx_{params['num_ctx']}"
                    else:
                        # Skip invalid parameter sets
                        continue
                    
                    # Find results with matching parameters
                    param_results = []
                    for r in results:
                        r_params = r.get("parameters_used", {})
                        if (isinstance(r_params, dict) and 
                            r_params.get("temperature") == params.get("temperature") and 
                            r_params.get("num_ctx") == params.get("num_ctx")):
                            param_results.append(r)
                    
                    if param_results:
                        # Extract metrics safely
                        quality_scores = []
                        for r in param_results:
                            score = r.get("final_quality") or r.get("quality_score")
                            if score is not None:
                                try:
                                    quality_scores.append(float(score))
                                except (ValueError, TypeError):
                                    pass
                        
                        time_taken = []
                        for r in param_results:
                            time_value = r.get("time_taken")
                            if time_value is not None:
                                try:
                                    time_taken.append(float(time_value))
                                except (ValueError, TypeError):
                                    pass
                        
                        # Calculate metrics only if we have data
                        param_metrics = {"data_points": len(param_results)}
                        
                        if quality_scores:
                            param_metrics["avg_quality"] = sum(quality_scores) / len(quality_scores)
                            if len(quality_scores) > 1:
                                param_metrics["std_quality"] = stdev(quality_scores)
                        else:
                            param_metrics["avg_quality"] = 0.0
                            param_metrics["std_quality"] = 0.0
                            
                        if time_taken:
                            param_metrics["avg_time"] = sum(time_taken) / len(time_taken)
                            if len(time_taken) > 1:
                                param_metrics["std_time"] = stdev(time_taken)
                        else:
                            param_metrics["avg_time"] = 0.0
                            param_metrics["std_time"] = 0.0
                        
                        analysis["parameter_impact"][param_key] = param_metrics
                except Exception as e:
                    print(f"Error analyzing parameter set: {e}")
                    if 'param_key' in locals():
                        analysis["parameter_impact"][param_key] = {
                            "error": str(e),
                            "data_points": len(param_results) if 'param_results' in locals() else 0
                        }
            
            # Analyze role accuracy separately from detection_accuracy
            role_matches = sum(1 for r in results 
                             if r.get("detected_role") == r.get("expected_role", ""))
            total_with_roles = sum(1 for r in results if r.get("expected_role"))
            
            if total_with_roles > 0:
                analysis["role_accuracy"] = role_matches / total_with_roles
            else:
                analysis["role_accuracy"] = 0.0
            
            # Calculate overall time metrics
            time_values = []
            for r in results:
                time_value = r.get("time_taken")
                if time_value is not None:
                    try:
                        time_values.append(float(time_value))
                    except (ValueError, TypeError):
                        pass
            
            if time_values:
                analysis["time_metrics"] = {
                    "average_time": sum(time_values) / len(time_values),
                    "min_time": min(time_values),
                    "max_time": max(time_values)
                }
        
        except Exception as e:
            print(f"Error during results analysis: {e}")
        
        # Ensure analysis has all expected keys even if errors occurred
        for key, value in empty_analysis.items():
            if key not in analysis:
                analysis[key] = value
        
        return analysis