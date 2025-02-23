# research/reporter.py

import time
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

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
    
    def __init__(self, output_dir: str = "research_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set visualization style
        plt.style.use('seaborn')
        sns.set_palette("husl")
    
    def generate_report(self, results: List[Any], analysis: Dict[str, Any]) -> ResearchReport:
        """Generate a research report from results and analysis"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        experiment_id = f"experiment_{timestamp}"
        
        return ResearchReport(
            title="Automated Prompt Engineering: A Comparative Analysis of Multi-Stage Refinement Techniques",
            description="Investigating the effectiveness of automated prompt refinement systems through iterative template-based techniques and comparative analysis.",
            results=results,
            analysis=analysis,
            timestamp=timestamp,
            experiment_id=experiment_id
        )
    
    def generate_visualizations(self, report: ResearchReport, viz_dir: Path):
        """Generate all visualizations for the report"""
        df = pd.DataFrame([vars(r) for r in report.results])
        
        # Create visualization directory
        viz_dir.mkdir(exist_ok=True)
        
        # Generate each visualization
        self._plot_technique_comparison(df, viz_dir)
        self._plot_parameter_impact(df, viz_dir)
        self._plot_quality_distribution(df, viz_dir)
        self._plot_time_analysis(df, viz_dir)
        self._plot_iteration_analysis(df, viz_dir)
        self._plot_role_accuracy(report.analysis, viz_dir)
        
        plt.close('all')
    
    def format_markdown_report(self, report: ResearchReport) -> str:
        """Format the report in markdown format"""
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
* Total experiments run: {len(report.results)}

## Test Cases and Methodology
"""
        
        # Add Results section with visualizations
        markdown += "\n# Results\n\n"
        
        # Technique Performance with visualization
        markdown += "## Technique Performance\n\n"
        markdown += "![Technique Comparison](./visualizations/technique_comparison.png)\n\n"
        
        for technique, metrics in report.analysis["technique_performance"].items():
            markdown += f"### {technique}\n"
            markdown += f"* Average Quality Score: {metrics['avg_quality']:.2f}\n"
            markdown += f"* Quality Standard Deviation: {metrics['std_quality']:.2f}\n"
            markdown += f"* Average Iterations Required: {metrics['avg_iterations']:.1f}\n\n"
        
        # Parameter Impact with visualization
        markdown += "## Parameter Impact\n\n"
        markdown += "![Parameter Impact](./visualizations/parameter_impact.png)\n\n"
        
        for param_key, metrics in report.analysis["parameter_impact"].items():
            markdown += f"### {param_key}\n"
            markdown += f"* Average Quality: {metrics['avg_quality']:.2f}\n"
            markdown += f"* Average Processing Time: {metrics['avg_time']:.2f}s\n\n"
        
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
        markdown += f"* Overall role matching accuracy: {report.analysis['role_accuracy']:.2%}\n\n"
        
        # Add key findings
        markdown += self._format_key_findings(report.analysis)
        
        # Add further research section
        markdown += self._format_further_research()
        
        return markdown
    
    def _format_key_findings(self, analysis: Dict[str, Any]) -> str:
        """Format the key findings section"""
        findings = "\n## Key Findings\n\n"
        
        # Find best performing technique
        best_technique = max(analysis["technique_performance"].items(), 
                           key=lambda x: x[1]['avg_quality'])
        findings += f"* Best performing technique: {best_technique[0]} "
        findings += f"(avg quality: {best_technique[1]['avg_quality']:.2f})\n"
        
        # Find optimal parameters
        best_params = max(analysis["parameter_impact"].items(),
                         key=lambda x: x[1]['avg_quality'])
        findings += f"* Optimal parameters: {best_params[0]} "
        findings += f"(avg quality: {best_params[1]['avg_quality']:.2f})\n"
        
        return findings
    
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
    
    def _plot_technique_comparison(self, df: pd.DataFrame, viz_dir: Path):
        """Generate technique comparison visualization"""
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='technique', y='quality_score', data=df)
        plt.title('Quality Scores by Technique')
        plt.xlabel('Technique')
        plt.ylabel('Quality Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(viz_dir / 'technique_comparison.png')
        plt.close()
    
    def _plot_parameter_impact(self, df: pd.DataFrame, viz_dir: Path):
        """Generate parameter impact visualization"""
        plt.figure(figsize=(12, 6))
        temps = df['parameters'].apply(lambda x: x['temperature'])
        sns.scatterplot(x=temps, y=df['quality_score'], alpha=0.6)
        plt.title('Quality Score vs Temperature')
        plt.xlabel('Temperature')
        plt.ylabel('Quality Score')
        plt.tight_layout()
        plt.savefig(viz_dir / 'parameter_impact.png')
        plt.close()
    
    def _plot_quality_distribution(self, df: pd.DataFrame, viz_dir: Path):
        """Generate quality distribution visualization"""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='quality_score', bins=20, kde=True)
        plt.title('Distribution of Quality Scores')
        plt.xlabel('Quality Score')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(viz_dir / 'quality_distribution.png')
        plt.close()
    
    def _plot_time_analysis(self, df: pd.DataFrame, viz_dir: Path):
        """Generate time analysis visualization"""
        plt.figure(figsize=(12, 6))
        sns.barplot(x='technique', y='time_taken', data=df)
        plt.title('Average Processing Time by Technique')
        plt.xlabel('Technique')
        plt.ylabel('Time (seconds)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(viz_dir / 'time_analysis.png')
        plt.close()
    
    def _plot_iteration_analysis(self, df: pd.DataFrame, viz_dir: Path):
        """Generate iteration analysis visualization"""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='iterations_used', y='quality_score', hue='technique')
        plt.title('Quality Score vs Number of Iterations')
        plt.xlabel('Number of Iterations')
        plt.ylabel('Quality Score')
        plt.tight_layout()
        plt.savefig(viz_dir / 'iteration_analysis.png')
        plt.close()
    
    def _plot_role_accuracy(self, analysis: Dict[str, Any], viz_dir: Path):
        """Generate role accuracy visualization"""
        plt.figure(figsize=(8, 8))
        accuracy = analysis.get('role_accuracy', 0)
        plt.pie([accuracy, 1-accuracy], 
                labels=['Correct', 'Incorrect'],
                autopct='%1.1f%%',
                colors=['#2ecc71', '#e74c3c'])
        plt.title('Role Selection Accuracy')
        plt.savefig(viz_dir / 'role_accuracy.png')
        plt.close()
    
    def save_report(self, report: ResearchReport):
        """Save all report files"""
        # Create experiment directory
        experiment_dir = self.output_dir / report.experiment_id
        experiment_dir.mkdir(exist_ok=True)
        
        # Generate visualizations
        viz_dir = experiment_dir / "visualizations"
        self.generate_visualizations(report, viz_dir)
        
        # Save markdown report
        report_file = experiment_dir / "research_report.md"
        with open(report_file, 'w') as f:
            f.write(self.format_markdown_report(report))
        
        # Save raw results
        results_file = experiment_dir / "raw_results.json"
        output = {
            "experiment_id": report.experiment_id,
            "timestamp": report.timestamp,
            "results": [vars(r) for r in report.results],
            "analysis": report.analysis
        }
        with open(results_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        # Save analysis summary
        analysis_file = experiment_dir / "analysis_summary.json"
        with open(analysis_file, 'w') as f:
            json.dump(report.analysis, f, indent=2)
        
        return experiment_dir