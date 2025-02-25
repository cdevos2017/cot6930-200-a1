#!/usr/bin/env python3
"""
Custom Experiment Runner - Run experiments with custom test cases.

This script allows you to run prompt engineering experiments with
specific categories of test cases or your own custom test cases.

Example Usage:
  python custom_experiment.py --category technical
  python custom_experiment.py --all
  python custom_experiment.py --custom my_test_cases.json
"""

import argparse
import json
import sys
import time
from pathlib import Path

from research.framework import PromptResearchFramework
from research.reporting.reporter import ResearchReporter
from research.test_cases import (
    TestCase, 
    STANDARD_TEST_CASES,
    CREATIVE_WRITING_TEST_CASES,
    TECHNICAL_TEST_CASES,
    ACADEMIC_TEST_CASES,
    BUSINESS_TEST_CASES,
    get_all_test_cases
)

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Run custom prompt engineering experiments")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--standard", action="store_true", help="Use standard test cases")
    group.add_argument("--creative", action="store_true", help="Use creative writing test cases")
    group.add_argument("--technical", action="store_true", help="Use technical test cases")
    group.add_argument("--academic", action="store_true", help="Use academic test cases")
    group.add_argument("--business", action="store_true", help="Use business test cases")
    group.add_argument("--all", action="store_true", help="Use all test cases")
    group.add_argument("--custom", type=str, help="Path to custom test cases JSON file")
    
    parser.add_argument("--techniques", type=str, help="Comma-separated list of techniques to test")
    parser.add_argument("--output", type=str, default="research/research_output", help="Output directory")
    parser.add_argument("--limit", type=int, help="Limit the number of test cases to run")
    parser.add_argument("--params", type=str, help="Path to custom parameter sets JSON file")
    parser.add_argument("--latex", action="store_true", help="Generate LaTeX report")
    parser.add_argument("--name", type=str, help="Custom name for the experiment")
    
    return parser.parse_args()

def load_custom_test_cases(file_path):
    """Load custom test cases from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        test_cases = []
        for item in data:
            test_cases.append(TestCase(
                query=item["query"],
                category=item.get("category", "custom"),
                expected_role=item.get("expected_role", "Assistant"),
                expected_technique=item.get("expected_technique", "chain_of_thought"),
                description=item.get("description", "Custom test case")
            ))
        
        return test_cases
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading custom test cases: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Custom test cases file '{file_path}' not found")
        sys.exit(1)

def load_custom_parameters(file_path):
    """Load custom parameter sets from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            parameter_sets = json.load(f)
        
        # Validate parameter sets
        for params in parameter_sets:
            if not isinstance(params, dict):
                raise ValueError("Parameter set must be a dictionary")
            if "temperature" not in params:
                raise ValueError("Parameter set must include 'temperature'")
            if "num_ctx" not in params:
                raise ValueError("Parameter set must include 'num_ctx'")
            if "num_predict" not in params:
                raise ValueError("Parameter set must include 'num_predict'")
        
        return parameter_sets
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading custom parameter sets: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Custom parameter file '{file_path}' not found")
        sys.exit(1)

def main():
    """Main function"""
    args = parse_arguments()
    
    # Initialize experiment name
    experiment_name = "default"
    
    # Select test cases
    if args.standard:
        test_cases = STANDARD_TEST_CASES
        experiment_name = "standard"
    elif args.creative:
        test_cases = CREATIVE_WRITING_TEST_CASES
        experiment_name = "creative"
    elif args.technical:
        test_cases = TECHNICAL_TEST_CASES
        experiment_name = "technical"
    elif args.academic:
        test_cases = ACADEMIC_TEST_CASES
        experiment_name = "academic"
    elif args.business:
        test_cases = BUSINESS_TEST_CASES
        experiment_name = "business"
    elif args.all:
        test_cases = get_all_test_cases()
        experiment_name = "all"
    elif args.custom:
        test_cases = load_custom_test_cases(args.custom)
        experiment_name = Path(args.custom).stem
    
    # Override experiment name if provided
    if args.name:
        experiment_name = args.name
    
    # Limit the number of test cases if specified
    if args.limit and args.limit > 0 and args.limit < len(test_cases):
        test_cases = test_cases[:args.limit]
    
    # Create the framework with selected test cases
    framework = PromptResearchFramework(test_cases=test_cases)
    
    # Set techniques if specified
    if args.techniques:
        techniques = [t.strip() for t in args.techniques.split(',')]
        framework.set_techniques(techniques)
    
    # Set custom parameter sets if specified
    if args.params:
        parameter_sets = load_custom_parameters(args.params)
        framework.set_parameter_sets(parameter_sets)
    
    # Print experiment information
    print(f"\nStarting Custom Experiment: {experiment_name}")
    print(f"Number of test cases: {len(test_cases)}")
    print(f"Techniques: {', '.join(framework.techniques)}")
    print(f"Parameter sets: {len(framework.parameter_sets)}")
    print(f"Total experiments: {len(test_cases) * len(framework.techniques) * len(framework.parameter_sets)}")
    
    # Run experiments
    start_time = time.time()
    print("\nRunning experiments...")
    results = framework.run_full_evaluation()
    
    # Analyze results
    print("\nAnalyzing results...")
    analysis = framework.analyze_results(results)
    
    # Add experiment metadata
    analysis["experiment_name"] = experiment_name
    analysis["experiment_duration"] = time.time() - start_time
    analysis["num_test_cases"] = len(test_cases)
    analysis["num_techniques"] = len(framework.techniques)
    analysis["num_parameter_sets"] = len(framework.parameter_sets)
    analysis["total_experiments"] = len(results)
    
    # Generate report
    print("\nGenerating report...")
    reporter = ResearchReporter(output_dir=args.output)
    report = reporter.generate_report(results, analysis)
    
    # Add custom title reflecting the experiment type
    report.title = f"Prompt Engineering Research: {experiment_name.capitalize()} Evaluation"
    report.description = f"Systematic evaluation of prompt engineering techniques using {experiment_name} test cases."
    
    # Save report
    output_dir = reporter.save_report(report)
    
    # Generate LaTeX report if requested
    if args.latex:
        try:
            print("\nGenerating LaTeX report...")
            from latex_report_generator import generate_report_for_experiment
            generate_report_for_experiment(output_dir)
        except ImportError:
            print("Warning: Could not generate LaTeX report. Make sure latex_report_generator.py is in your path.")
    
    # Print summary
    print(f"\nExperiment '{experiment_name}' completed successfully!")
    print(f"Results saved to: {output_dir}")
    print(f"Total time: {time.time() - start_time:.2f} seconds")
    
    # Print key findings
    if "technique_performance" in analysis:
        best_technique = None
        best_score = -1
        
        for technique, metrics in analysis["technique_performance"].items():
            if metrics.get("avg_quality", 0) > best_score:
                best_score = metrics.get("avg_quality", 0)
                best_technique = technique
        
        if best_technique:
            print(f"\nBest performing technique: {best_technique} (avg quality: {best_score:.2f})")
    
    if "role_accuracy" in analysis:
        print(f"Role detection accuracy: {analysis['role_accuracy']:.2%}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())