# requirements_framework_extension.py
from research.framework import PromptResearchFramework
from research.test_cases import TestCase
from typing import Dict, Any, List, Optional

class RequirementsAnalysisFramework(PromptResearchFramework):
    """Extension of the research framework specifically for requirements analysis"""
    
    def __init__(self, test_cases=None):
        super().__init__(test_cases=test_cases)
        
        # Requirements-specific metrics
        self.requirements_metrics = {
            "completeness": 0.0,
            "clarity": 0.0,
            "testability": 0.0,
            "conflict_detection": 0.0
        }
    
    def run_requirements_experiment(self, test_case: TestCase, technique: str, 
                                   parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Run a requirements-focused experiment with enhanced metrics"""
        
        # Start timing
        import time
        start_time = time.time()
        
        # Run the base experiment
        result = super().run_experiment(test_case, technique, parameters)
        
        # Add requirements-specific analysis
        if result and "final_prompt" in result:
            final_text = result["final_prompt"]
            
            # Count number of explicit requirements (identified by numbers or bullets)
            import re
            req_count = len(re.findall(r'^\s*(\d+\.|\*|\-)\s+', final_text, re.MULTILINE))
            result["requirements_count"] = req_count
            
            # Calculate basic metrics
            result["requirements_metrics"] = {
                "explicit_count": req_count,
                "contains_priorities": "priority" in final_text.lower() or "high" in final_text.lower(),
                "contains_categories": "functional" in final_text.lower() or "non-functional" in final_text.lower()
            }
        
        # Add timing information
        result["time_taken"] = time.time() - start_time
        
        return result
    
    def analyze_requirements_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze results with a focus on requirements quality metrics"""
        # Get base analysis
        base_analysis = super().analyze_results(results)
        
        # Add requirements-specific analysis
        req_analysis = {
            "avg_requirements_count": 0,
            "requirements_by_technique": {},
            "requirements_by_category": {}
        }
        
        # Calculate average requirements count
        req_counts = [r.get("requirements_count", 0) for r in results if "requirements_count" in r]
        if req_counts:
            req_analysis["avg_requirements_count"] = sum(req_counts) / len(req_counts)
        
        # Calculate by technique
        for technique in set(r.get("technique_used", "") for r in results):
            if not technique:
                continue
                
            tech_results = [r for r in results if r.get("technique_used") == technique]
            tech_counts = [r.get("requirements_count", 0) for r in tech_results if "requirements_count" in r]
            
            if tech_counts:
                req_analysis["requirements_by_technique"][technique] = {
                    "avg_count": sum(tech_counts) / len(tech_counts),
                    "sample_count": len(tech_counts)
                }
        
        # Merge the analyses
        base_analysis.update({
            "requirements_analysis": req_analysis
        })
        
        return base_analysis