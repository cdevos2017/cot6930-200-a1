#!/usr/bin/env python3
"""
Requirements Analysis Experiment

Runs a comparative experiment on requirement analysis techniques using
the research framework and prompt techniques.
"""

import os
import json
import time
import sys
from typing import List, Dict, Any

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Import framework components
from research.framework import PromptResearchFramework
from research.test_cases import TestCase
from research.reporting.reporter import ResearchReporter

# Import the prompt engineering modules with correct paths
from prompt.techniques import (
    get_l1_technique_names,
    get_l2_technique_names,
    apply_l1_technique,
    execute_l2_technique_step,
    L1_TECHNIQUES,
    L2_TECHNIQUES
)

# Parameter variations to test
DEFAULT_PARAMETER_SETS = [
    {"temperature": 0.2, "num_ctx": 2048, "num_predict": 1024},  # Low temperature
    {"temperature": 0.5, "num_ctx": 2048, "num_predict": 1024},  # Medium temperature
    {"temperature": 0.7, "num_ctx": 2048, "num_predict": 1024},  # High temperature
    {"temperature": 0.5, "num_ctx": 4096, "num_predict": 2048},  # Larger context
]

def load_test_cases(file_path: str) -> List[TestCase]:
    """Load custom test cases from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        test_cases = []
        for item in data:
            test_cases.append(TestCase(
                query=item["query"],
                category=item.get("category", "requirements"),
                expected_role=item.get("expected_role", "Requirements Engineer"),
                expected_technique=item.get("expected_technique", "structured_output"),
                description=item.get("description", "Requirement analysis task")
            ))
        
        return test_cases
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading test cases: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Test cases file '{file_path}' not found")
        sys.exit(1)

def load_parameter_sets(file_path: str) -> List[Dict[str, Any]]:
    """Load custom parameter sets from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            parameter_sets = json.load(f)
        return parameter_sets
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading parameter sets: {e}")
        return DEFAULT_PARAMETER_SETS
    except FileNotFoundError:
        print(f"Parameter sets file '{file_path}' not found, using defaults")
        return DEFAULT_PARAMETER_SETS

def run_l1_experiment(framework, test_cases, technique_name, technique_config):
    """Run experiment with Level-1 technique"""
    print(f"\nRunning Level-1 technique: {technique_name}")
    results = []
    
    for test_case in test_cases:
        # Create a modified test case with the L1 technique template
        l1_query = apply_l1_technique(test_case.query, technique_name)
        l1_test_case = TestCase(
            query=l1_query,
            category=f"L1_{test_case.category}",
            expected_role=test_case.expected_role,
            expected_technique=test_case.expected_technique,
            description=f"L1 {technique_name}: {test_case.description}"
        )
        
        # Run experiments with this modified test case
        for technique in framework.techniques:
            for params in framework.parameter_sets:
                result = framework.run_experiment(l1_test_case, technique, params)
                if result:
                    # Add metadata about the L1 technique
                    result["l1_technique"] = technique_name
                    result["l1_description"] = technique_config["description"]
                    result["original_task"] = test_case.query
                    results.append(result)
    
    return results

def run_l2_experiment(framework, test_cases, technique_name, technique_config):
    """Run experiment with Level-2 technique"""
    print(f"\nRunning Level-2 technique: {technique_name}")
    results = []
    
    # Import the function to get step count
    from prompt.templates import get_l2_technique_steps_count
    
    for test_case in test_cases:
        # We need to simulate the chain of prompts for L2 techniques
        print(f"  Processing task: {test_case.description}")
        
        # For L2, we'll use a single technique (chain_of_thought) and parameter set
        # to ensure consistency in the chain
        technique = "chain_of_thought"
        params = framework.parameter_sets[1]  # Use medium temperature
        
        previous_response = None
        chain_results = []
        
        # Get number of steps from templates module instead of config dictionary
        num_steps = get_l2_technique_steps_count(technique_name)
        if num_steps == 0:
            print(f"Warning: No steps found for technique {technique_name}")
            continue
            
        for i in range(num_steps):
            # Format the template with the original query and previous response if available
            l2_query = execute_l2_technique_step(
                test_case.query,
                technique_name,
                i,
                previous_response
            )
            
            # Create a test case for this step
            step_test_case = TestCase(
                query=l2_query,
                category=f"L2_{test_case.category}_step{i+1}",
                expected_role=test_case.expected_role,
                expected_technique=technique,
                description=f"L2 {technique_name} Step {i+1}: {test_case.description}"
            )
            
            # Run this step
            step_result = framework.run_experiment(step_test_case, technique, params)
            
            if step_result:
                # Extract the response for the next step
                previous_response = step_result.get("final_prompt", "")
                
                # Add metadata about the L2 technique
                step_result["l2_technique"] = technique_name
                step_result["l2_description"] = technique_config["description"]
                step_result["l2_step"] = i + 1
                step_result["l2_total_steps"] = num_steps
                step_result["original_task"] = test_case.query
                
                chain_results.append(step_result)
        
        # Add all step results to our overall results
        results.extend(chain_results)
    
    return results

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Run requirement analysis prompt engineering experiments")
    
    parser.add_argument("--test-cases", type=str, default="research/experiments/requirements_analysis/requirements_test_cases.json", 
                    help="Path to test cases JSON file")
    parser.add_argument("--params", type=str, default=None,
                        help="Path to custom parameter sets JSON file")
    parser.add_argument("--output", type=str, default="research/research_output", 
                        help="Output directory")
    parser.add_argument("--limit", type=int, help="Limit the number of test cases to run")
    parser.add_argument("--l1-only", action="store_true", 
                        help="Run only Level-1 techniques")
    parser.add_argument("--l2-only", action="store_true", 
                        help="Run only Level-2 techniques")
    parser.add_argument("--techniques", type=str, 
                        help="Comma-separated list of framework techniques to test")
    parser.add_argument("--latex", action="store_true", 
                        help="Generate LaTeX report")
    
    return parser.parse_args()

def generate_charts(results, output_dir):
    """Generate additional charts specific to requirement analysis"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert results to DataFrame
    df = pd.DataFrame(results)
    
    # 1. Compare L1 vs Standard techniques
    plt.figure(figsize=(12, 8))
    
    # Filter for L1 techniques vs standard
    l1_data = df[df['l1_technique'].notna()]
    std_data = df[df['l1_technique'].isna() & df['l2_technique'].isna()]
    
    # Calculate average quality scores
    if not l1_data.empty and not std_data.empty:
        l1_avg = l1_data.groupby('l1_technique')['quality_score'].mean().reset_index()
        std_avg = std_data.groupby('technique_used')['quality_score'].mean().reset_index()
        std_avg['l1_technique'] = "Standard (No L1)"
        
        # Combine data
        combined = pd.concat([l1_avg, std_avg])
        
        # Create plot
        sns.barplot(x='l1_technique', y='quality_score', data=combined)
        plt.title('Requirement Quality: L1 Techniques vs Standard')
        plt.xlabel('Technique')
        plt.ylabel('Average Quality Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'l1_vs_standard.png'))
    
    # 2. L2 Technique Steps Comparison
    plt.figure(figsize=(12, 8))
    
    # Filter for L2 techniques
    l2_data = df[df['l2_technique'].notna()]
    
    if not l2_data.empty:
        # Group by technique and step
        l2_step_quality = l2_data.groupby(['l2_technique', 'l2_step'])['quality_score'].mean().reset_index()
        
        # Create plot
        sns.lineplot(x='l2_step', y='quality_score', hue='l2_technique', markers=True, data=l2_step_quality)
        plt.title('Quality Progression in L2 Techniques')
        plt.xlabel('Step in Chain')
        plt.ylabel('Average Quality Score')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'l2_step_progression.png'))
    
    # 3. Requirements Completeness by Category
    plt.figure(figsize=(14, 8))
    
    # Use category from the original test cases
    if 'category' in df.columns:
        category_quality = df.groupby(['category', 'technique_used'])['quality_score'].mean().reset_index()
        
        if not category_quality.empty:
            sns.barplot(x='category', y='quality_score', hue='technique_used', data=category_quality)
            plt.title('Requirement Quality by Category and Technique')
            plt.xlabel('Requirement Category')
            plt.ylabel('Average Quality Score')
            plt.xticks(rotation=45)
            plt.legend(title='Technique')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'category_quality.png'))
    
    # 4. Temperature Impact on L1 vs L2
    plt.figure(figsize=(12, 8))
    
    # Extract temperature from parameters_used
    def get_temp(row):
        params = row.get('parameters_used', {})
        if isinstance(params, dict):
            return params.get('temperature', None)
        return None
    
    df['temperature'] = df.apply(get_temp, axis=1)
    
    # Create technique type column
    df['technique_type'] = 'Standard'
    df.loc[df['l1_technique'].notna(), 'technique_type'] = 'Level-1'
    df.loc[df['l2_technique'].notna(), 'technique_type'] = 'Level-2'
    
    # Group by technique type and temperature
    temp_impact = df.groupby(['technique_type', 'temperature'])['quality_score'].mean().reset_index()
    
    if not temp_impact.empty and not temp_impact['temperature'].isna().all():
        sns.lineplot(x='temperature', y='quality_score', hue='technique_type', 
                    markers=True, data=temp_impact)
        plt.title('Impact of Temperature on Different Technique Levels')
        plt.xlabel('Temperature')
        plt.ylabel('Average Quality Score')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'temperature_impact.png'))
    
    plt.close('all')
    return {
        'l1_vs_standard': os.path.join(output_dir, 'l1_vs_standard.png'),
        'l2_step_progression': os.path.join(output_dir, 'l2_step_progression.png'),
        'category_quality': os.path.join(output_dir, 'category_quality.png'),
        'temperature_impact': os.path.join(output_dir, 'temperature_impact.png')
    }

# Main function to run the experiment
def main():
    """Main function to run the experiment"""
    args = parse_arguments()
    
    # Load test cases
    test_cases = load_test_cases(args.test_cases)
    
    # Load parameter sets
    parameter_sets = DEFAULT_PARAMETER_SETS
    if args.params:
        parameter_sets = load_parameter_sets(args.params)
    
    # Limit test cases if specified
    if args.limit and args.limit > 0 and args.limit < len(test_cases):
        test_cases = test_cases[:args.limit]
    
    print(f"Loaded {len(test_cases)} test cases for requirement analysis")
    
    # Initialize the framework
    framework = PromptResearchFramework(test_cases=test_cases)
    
    # Set techniques if specified
    if args.techniques:
        techniques = [t.strip() for t in args.techniques.split(',')]
        framework.set_techniques(techniques)
    
    # Set parameter sets
    framework.set_parameter_sets(parameter_sets)
    
    # Create experiment timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    experiment_id = f"requirement_analysis_{timestamp}"
    
    # Run standard experiments as baseline
    print("\nRunning baseline experiments with standard techniques...")
    baseline_results = []
    if not args.l1_only and not args.l2_only:
        baseline_results = framework.run_full_evaluation()
    
    # Run L1 experiments
    l1_results = []
    if not args.l2_only:
        for name in get_l1_technique_names():
            config = L1_TECHNIQUES[name]
            l1_results.extend(run_l1_experiment(framework, test_cases, name, config))
    
    # Run L2 experiments
    l2_results = []
    if not args.l1_only:
        for name in get_l2_technique_names():
            config = L2_TECHNIQUES[name]
            l2_results.extend(run_l2_experiment(framework, test_cases, name, config))
    
    # Combine all results
    all_results = baseline_results + l1_results + l2_results
    
    # Analyze results
    print("\nAnalyzing experiment results...")
    analysis = framework.analyze_results(all_results)
    
    # Add experiment metadata
    analysis["experiment_name"] = "Requirement Analysis Prompt Engineering"
    analysis["experiment_id"] = experiment_id
    analysis["experiment_timestamp"] = timestamp
    analysis["num_test_cases"] = len(test_cases)
    analysis["num_l1_techniques"] = len(L1_TECHNIQUES)
    analysis["num_l2_techniques"] = len(L2_TECHNIQUES)
    analysis["l1_techniques"] = list(L1_TECHNIQUES.keys())
    analysis["l2_techniques"] = list(L2_TECHNIQUES.keys())
    
    # Calculate L1 vs Standard metrics
    l1_data = [r for r in all_results if 'l1_technique' in r and r['l1_technique']]
    std_data = [r for r in all_results if 'l1_technique' not in r and 'l2_technique' not in r]
    
    if l1_data and std_data:
        l1_avg_quality = sum(r.get('quality_score', 0) for r in l1_data) / len(l1_data)
        std_avg_quality = sum(r.get('quality_score', 0) for r in std_data) / len(std_data)
        
        analysis["l1_vs_standard"] = {
            "l1_avg_quality": l1_avg_quality,
            "std_avg_quality": std_avg_quality,
            "quality_improvement": ((l1_avg_quality - std_avg_quality) / std_avg_quality) * 100
        }
    
    # Calculate L2 metrics
    l2_data = [r for r in all_results if 'l2_technique' in r and r['l2_technique']]
    
    if l2_data:
        # Group by technique and step
        l2_by_tech_step = {}
        for r in l2_data:
            tech = r.get('l2_technique', '')
            step = r.get('l2_step', 0)
            
            if tech not in l2_by_tech_step:
                l2_by_tech_step[tech] = {}
            
            if step not in l2_by_tech_step[tech]:
                l2_by_tech_step[tech][step] = []
            
            l2_by_tech_step[tech][step].append(r)
        
        # Calculate average quality by step
        l2_step_quality = {}
        for tech, steps in l2_by_tech_step.items():
            l2_step_quality[tech] = {}
            for step, results in steps.items():
                avg_quality = sum(r.get('quality_score', 0) for r in results) / len(results)
                l2_step_quality[tech][step] = avg_quality
        
        analysis["l2_step_quality"] = l2_step_quality
        
        # Calculate overall L2 quality
        l2_avg_quality = sum(r.get('quality_score', 0) for r in l2_data) / len(l2_data)
        
        if std_data:
            analysis["l2_vs_standard"] = {
                "l2_avg_quality": l2_avg_quality,
                "std_avg_quality": std_avg_quality,
                "quality_improvement": ((l2_avg_quality - std_avg_quality) / std_avg_quality) * 100
            }
        
        if l1_data:
            analysis["l2_vs_l1"] = {
                "l2_avg_quality": l2_avg_quality,
                "l1_avg_quality": l1_avg_quality,
                "quality_improvement": ((l2_avg_quality - l1_avg_quality) / l1_avg_quality) * 100
            }
    
    # Generate report
    print("\nGenerating research report...")
    ensure_directories_exist(args.output)
    reporter = ResearchReporter(output_dir=args.output)
    
    # Create a report
    report = reporter.generate_report(all_results, analysis)
    
    # Customize report title and description
    report.title = "Automated Requirement Analysis: Comparative Study of Multi-Level Prompt Engineering Techniques"
    report.description = "This research compares Level-1 and Level-2 prompt engineering techniques for requirement analysis tasks."
    
    # Save report
    output_dir = reporter.save_report(report)
    
    # Generate custom visualizations
    print("\nGenerating specialized visualizations...")
    viz_dir = output_dir / "specialized_visualizations"
    custom_charts = generate_charts(all_results, viz_dir)
    
    # Print summary
    print(f"\nExperiment '{experiment_id}' completed successfully!")
    print(f"Results saved to: {output_dir}")
    
    # Print key findings
    l1_finding = analysis.get("l1_vs_standard", {})
    if l1_finding:
        print(f"\nLevel-1 vs Standard: {l1_finding.get('quality_improvement', 0):.2f}% quality improvement")
    
    l2_finding = analysis.get("l2_vs_standard", {})
    if l2_finding:
        print(f"Level-2 vs Standard: {l2_finding.get('quality_improvement', 0):.2f}% quality improvement")
    
    l2_vs_l1 = analysis.get("l2_vs_l1", {})
    if l2_vs_l1:
        print(f"Level-2 vs Level-1: {l2_vs_l1.get('quality_improvement', 0):.2f}% quality improvement")
    
    return 0

def ensure_directories_exist(output_dir):
    """Ensure all necessary directories exist"""
    from pathlib import Path
    
    # Create output directory with parents
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Create specialized visualizations directory if needed
    viz_dir = Path(output_dir).joinpath("specialized_visualizations")
    viz_dir.mkdir(parents=True, exist_ok=True)

# Then in your main() function, add a call to this function before initializing the reporter:
# ensure_directories_exist(args.output)

# Then keep your if __name__ block simple:
if __name__ == "__main__":
    sys.exit(main())