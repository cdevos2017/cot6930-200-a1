# research/reporter.py

import time
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from research.visualization import ResearchVisualizer

@dataclass
class ResearchReport:
    """Container for research report data"""
    title: str
    description: str
    results: List[Any]
    analysis: Dict[str, Any]
    timestamp: str
    experiment_id: str

class ResearchReporter:
    """Handles generation and saving of research reports"""
    
    def __init__(self, output_dir: str = "research/research_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_report(self, results: List[Any], analysis: Dict[str, Any]) -> ResearchReport:
        """Generate a research report from results and analysis"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        experiment_id = f"experiment_{timestamp}"
        
        # Ensure analysis is valid
        if not isinstance(analysis, dict):
            print(f"Warning: Analysis is not a dictionary, type: {type(analysis)}")
            analysis = {"error": f"Invalid analysis type: {type(analysis)}"}
        
        # Ensure required keys exist in analysis
        for key in ["technique_performance", "parameter_impact", "detection_accuracy"]:
            if key not in analysis:
                analysis[key] = {}
        
        return ResearchReport(
            title="Automated Prompt Engineering: A Comparative Analysis of Multi-Stage Refinement Techniques",
            description="Investigating the effectiveness of automated prompt refinement systems through iterative template-based techniques and comparative analysis.",
            results=results,
            analysis=analysis,
            timestamp=timestamp,
            experiment_id=experiment_id
        )
    
    def save_report(self, report: ResearchReport):
        """Save all report files with robust error handling and detailed logging"""
        # Create experiment directory
        experiment_dir = self.output_dir / report.experiment_id
        experiment_dir.mkdir(exist_ok=True)
        
        print(f"Saving report to: {experiment_dir}")
        
        try:
            # Generate visualizations
            viz_dir = experiment_dir / "visualizations"
            visualizer = ResearchVisualizer(experiment_dir)
            
            print(f"Generating visualizations in: {viz_dir}")
            visualizer.generate_all_visualizations(report.results, report.analysis)
            
            # Save markdown report
            report_file = experiment_dir / "research_report.md"
            print(f"Saving markdown report to: {report_file}")
            
            report_content = self.format_markdown_report(report)
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"Markdown report saved: {report_file} ({len(report_content)} bytes)")
            
            # Save raw results - handle different types of result objects safely
            results_file = experiment_dir / "raw_results.json"
            print(f"Saving raw results to: {results_file}")
            
            # Convert results to serializable format
            serialized_results = []
            for r in report.results:
                if hasattr(r, '__dict__'):
                    # If it's an object with a __dict__ attribute, use vars()
                    serialized_results.append(vars(r))
                elif isinstance(r, dict):
                    # If it's already a dictionary, use it directly
                    serialized_results.append(r)
                else:
                    # For other types, convert to a string representation
                    serialized_results.append({"data": str(r), "type": str(type(r))})
            
            # Prepare output with error handling for JSON serialization
            try:
                output = {
                    "experiment_id": report.experiment_id,
                    "timestamp": report.timestamp,
                    "results": serialized_results,
                    "analysis": report.analysis
                }
                
                # Try to serialize to string first to verify JSON is valid
                json_str = json.dumps(output, indent=2, default=str)
                json_bytes = json_str.encode('utf-8')
                
                # Write to file
                with open(results_file, 'wb') as f:
                    f.write(json_bytes)
                
                print(f"Raw results saved: {results_file} ({len(json_bytes)} bytes)")
                    
            except (TypeError, ValueError) as e:
                print(f"Warning: Error serializing full results to JSON: {e}")
                # Fallback: save a simplified version
                simplified_output = {
                    "experiment_id": report.experiment_id,
                    "timestamp": report.timestamp,
                    "analysis": report.analysis,
                    "error": f"Could not serialize full results: {str(e)}",
                    "results_count": len(report.results)
                }
                with open(results_file, 'w', encoding='utf-8') as f:
                    json.dump(simplified_output, f, indent=2, default=str)
                
                print(f"Simplified results saved due to serialization error")
            
            # Save analysis summary
            analysis_file = experiment_dir / "analysis_summary.json"
            print(f"Saving analysis summary to: {analysis_file}")
            
            analysis_json = json.dumps(report.analysis, indent=2, default=str)
            with open(analysis_file, 'w', encoding='utf-8') as f:
                f.write(analysis_json)
            
            print(f"Analysis summary saved: {analysis_file} ({len(analysis_json)} bytes)")
            
            # Verify all files were created
            expected_files = [report_file, results_file, analysis_file]
            for file_path in expected_files:
                if not file_path.exists():
                    print(f"WARNING: Expected file not found: {file_path}")
                else:
                    print(f"Verified file exists: {file_path} ({file_path.stat().st_size} bytes)")
            
            return experiment_dir
            
        except Exception as e:
            print(f"Error saving report: {e}")
            import traceback
            traceback.print_exc()
            
            # Create a simple error report
            error_file = experiment_dir / "error_report.txt"
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f"Error generating full report: {str(e)}\n\n")
                f.write(f"Experiment ID: {report.experiment_id}\n")
                f.write(f"Timestamp: {report.timestamp}\n")
                f.write(f"Results count: {len(report.results) if report.results else 0}\n")
                f.write("\nTraceback:\n")
                import traceback
                traceback.print_exc(file=f)
            
            return experiment_dir
    
    def format_markdown_report(self, report: ResearchReport) -> str:
        """Format the report in markdown format with robust error handling"""
        try:
            markdown = f"""
# {report.title}

{report.description}

# Research Question

How can we systematically evaluate and optimize automated prompt engineering techniques to improve prompt quality, response consistency, and task-specific performance?

## Arguments

#### What is already known about this topic

* Manual prompt engineering requires expertise and multiple iterations to achieve high-quality results
* Different techniques (chain-of-thought, tree-of-thought, etc.) work better for different types of tasks
* Template-based approaches can help standardize prompt construction
* Parameter tuning significantly affects model response quality and consistency

#### What this research is exploring

* We employ a multi-stage automated prompt refinement system that combines:
  - Rule-based template selection and validation
  - LLM-based prompt analysis and improvement
  - Dynamic role and technique detection
  - Iterative quality assessment
  - Parameter optimization

* We are building a comparative analysis framework to evaluate:
  - Different prompt engineering techniques (chain-of-thought vs tree-of-thought vs structured output)
  - Impact of role-based vs technique-based refinements
  - Effects of parameter variations on response quality
  - Model response consistency across different tasks

#### Implications for practice

* More consistent and higher quality prompts through automation
* Reduced dependency on manual prompt engineering expertise
* Better understanding of which techniques work best for different tasks
* Framework for systematic prompt engineering evaluation
* Improved efficiency in prompt development and optimization

# Research Method

Our experimental setup included:
* Total experiments run: {len(report.results) if report.results else 0}

## Test Cases and Methodology
"""
            
            # Add Results section with visualizations
            markdown += "\n# Results\n\n"
            
            # Technique Performance with visualization
            markdown += "## Technique Performance\n\n"
            markdown += "![Technique Comparison](./visualizations/technique_comparison.png)\n\n"
            
            # Get technique performance data safely
            technique_performance = report.analysis.get("technique_performance", {})
            if technique_performance:
                for technique, metrics in technique_performance.items():
                    markdown += f"### {technique}\n"
                    markdown += f"* Average Quality Score: {metrics.get('avg_quality', 0):.2f}\n"
                    markdown += f"* Quality Standard Deviation: {metrics.get('std_quality', 0):.2f}\n"
                    markdown += f"* Average Iterations Required: {metrics.get('avg_iterations', 0):.1f}\n\n"
            else:
                markdown += "No technique performance data available.\n\n"
            
            # Parameter Impact with visualization
            markdown += "## Parameter Impact\n\n"
            markdown += "![Parameter Impact](./visualizations/parameter_impact.png)\n\n"
            
            # Get parameter impact data safely
            parameter_impact = report.analysis.get("parameter_impact", {})
            if parameter_impact:
                for param_key, metrics in parameter_impact.items():
                    markdown += f"### {param_key}\n"
                    markdown += f"* Average Quality: {metrics.get('avg_quality', 0):.2f}\n"
                    markdown += f"* Average Processing Time: {metrics.get('avg_time', 0):.2f}s\n\n"
            else:
                markdown += "No parameter impact data available.\n\n"
            
            # Quality Distribution
            markdown += "## Quality Distribution\n\n"
            markdown += "![Quality Distribution](./visualizations/quality_distribution.png)\n\n"
            
            # Time Analysis
            markdown += "## Processing Time Analysis\n\n"
            markdown += "![Time Analysis](./visualizations/time_analysis.png)\n\n"
            
            # Iteration Analysis
            markdown += "## Iteration Impact Analysis\n\n"
            markdown += "![Iteration Analysis](./visualizations/iteration_analysis.png)\n\n"
            
            # Role Accuracy
            markdown += "## Role Selection Performance\n\n"
            markdown += "![Role Accuracy](./visualizations/role_accuracy.png)\n\n"
            
            # Get role accuracy safely
            role_accuracy = report.analysis.get("role_accuracy", 0)
            markdown += f"* Overall role matching accuracy: {role_accuracy:.2%}\n\n"
            
            # Add key findings
            markdown += self._format_key_findings(report.analysis)
            
            # Add further research section
            markdown += self._format_further_research()
            
            return markdown
            
        except Exception as e:
            print(f"Error formatting markdown report: {e}")
            # Return a basic error report
            return f"""
# Prompt Engineering Research Report (Error)

## Error generating full report

An error occurred while formatting the research report: 

```
{str(e)}
```

### Basic Information

* Experiment ID: {report.experiment_id}
* Timestamp: {report.timestamp}
* Number of experiments: {len(report.results) if report.results else 0}

Please check the raw data files for more information.
"""
    
    def _format_key_findings(self, analysis: Dict[str, Any]) -> str:
        """Format the key findings section with error handling"""
        findings = "\n## Key Findings\n\n"
        
        try:
            # Find best performing technique
            technique_performance = analysis.get("technique_performance", {})
            if technique_performance:
                best_technique = None
                best_quality = -1
                
                for technique, metrics in technique_performance.items():
                    avg_quality = metrics.get('avg_quality', 0)
                    if avg_quality > best_quality:
                        best_quality = avg_quality
                        best_technique = technique
                
                if best_technique:
                    findings += f"* Best performing technique: {best_technique} "
                    findings += f"(avg quality: {best_quality:.2f})\n"
                else:
                    findings += "* Could not determine best performing technique due to missing data\n"
            else:
                findings += "* No technique performance data available\n"
            
            # Find optimal parameters
            parameter_impact = analysis.get("parameter_impact", {})
            if parameter_impact:
                best_params = None
                best_quality = -1
                
                for param_key, metrics in parameter_impact.items():
                    avg_quality = metrics.get('avg_quality', 0)
                    if avg_quality > best_quality:
                        best_quality = avg_quality
                        best_params = param_key
                
                if best_params:
                    findings += f"* Optimal parameters: {best_params} "
                    findings += f"(avg quality: {best_quality:.2f})\n"
                else:
                    findings += "* Could not determine optimal parameters due to missing data\n"
            else:
                findings += "* No parameter impact data available\n"
            
            # Add role accuracy if available
            if "role_accuracy" in analysis:
                findings += f"* Overall role detection accuracy: {analysis['role_accuracy']:.2%}\n"
            
            # Add time metrics if available
            time_metrics = analysis.get("time_metrics", {})
            if time_metrics and time_metrics.get("average_time"):
                findings += f"* Average processing time: {time_metrics.get('average_time', 0):.2f}s\n"
            
            return findings
            
        except Exception as e:
            print(f"Error formatting key findings: {e}")
            return "\n## Key Findings\n\n* Error generating key findings: {str(e)}\n"
    
    def _format_further_research(self) -> str:
        """Format the further research section"""
        return """
# Further research

Potential areas for future investigation include:

1. **Extended Parameter Space Exploration**
   * Testing wider ranges of temperature and context window sizes
   * Investigating impact of other model parameters
   * Exploring adaptive parameter selection

2. **Additional Technique Combinations**
   * Hybrid approaches combining multiple techniques
   * Task-specific technique optimization
   * Novel prompt engineering patterns

3. **Automation Improvements**
   * Enhanced role and technique detection
   * More sophisticated quality metrics
   * Real-time technique adaptation

4. **Task-Specific Optimization**
   * Detailed analysis of technique effectiveness per task type
   * Custom techniques for specific domains
   * Performance benchmarking across different task categories
"""