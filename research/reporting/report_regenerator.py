#!/usr/bin/env python3
"""
Report Regenerator Tool - Regenerate visualizations and reports for existing experiment results.

Usage:
    python report_regenerator.py [experiment_id]

If experiment_id is not provided, it will list all available experiment directories.
"""

import sys
import os
import json
from pathlib import Path
import pandas as pd
from research.visualization import ResearchVisualizer
from research.reporting.reporter import ResearchReporter, ResearchReport

def list_experiment_dirs(research_output_dir="research_output"):
    """List all experiment directories in the research_output directory"""
    output_dir = Path(research_output_dir)
    if not output_dir.exists() or not output_dir.is_dir():
        print(f"Error: Research output directory '{research_output_dir}' not found.")
        return []
    
    experiment_dirs = [d for d in output_dir.iterdir() if d.is_dir() and d.name.startswith("experiment_")]
    return sorted(experiment_dirs)

def load_experiment_data(experiment_dir):
    """Load experiment data from raw_results.json and analysis_summary.json"""
    raw_results_path = experiment_dir / "raw_results.json"
    analysis_path = experiment_dir / "analysis_summary.json"
    
    if not raw_results_path.exists():
        print(f"Error: raw_results.json not found in {experiment_dir}")
        return None, None
    
    if not analysis_path.exists():
        print(f"Error: analysis_summary.json not found in {experiment_dir}")
        return None, None
    
    try:
        with open(raw_results_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        with open(analysis_path, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        return raw_data.get('results', []), analysis_data
    except Exception as e:
        print(f"Error loading experiment data: {e}")
        return None, None

def regenerate_report(experiment_dir):
    """Regenerate visualizations and report for an existing experiment"""
    print(f"Regenerating report for {experiment_dir.name}...")
    
    # Load experiment data
    results, analysis = load_experiment_data(experiment_dir)
    if results is None or analysis is None:
        print("Failed to load experiment data.")
        return False
    
    try:
        # Create visualizer and generate visualizations
        visualizer = ResearchVisualizer(experiment_dir)
        visualizer.generate_all_visualizations(results, analysis)
        
        # Recreate report object
        experiment_id = experiment_dir.name
        timestamp = experiment_id.replace("experiment_", "")
        
        report = ResearchReport(
            title="Automated Prompt Engineering: A Comparative Analysis of Multi-Stage Refinement Techniques",
            description="Investigating the effectiveness of automated prompt refinement systems through iterative template-based techniques and comparative analysis.",
            results=results,
            analysis=analysis,
            timestamp=timestamp,
            experiment_id=experiment_id
        )
        
        # Generate markdown report
        reporter = ResearchReporter()
        report_file = experiment_dir / "research_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(reporter.format_markdown_report(report))
        
        print(f"Successfully regenerated report and visualizations for {experiment_id}")
        print(f"Report saved to: {report_file}")
        return True
    
    except Exception as e:
        print(f"Error regenerating report: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    # Handle command-line arguments
    if len(sys.argv) > 1:
        # Regenerate report for specific experiment ID
        experiment_id = sys.argv[1]
        
        # Check if it has the "experiment_" prefix, add it if not
        if not experiment_id.startswith("experiment_"):
            experiment_id = f"experiment_{experiment_id}"
        
        experiment_dir = Path("research_output") / experiment_id
        
        if not experiment_dir.exists() or not experiment_dir.is_dir():
            print(f"Error: Experiment directory '{experiment_dir}' not found.")
            print("Available experiment directories:")
            for exp_dir in list_experiment_dirs():
                print(f"  {exp_dir.name}")
            return 1
        
        success = regenerate_report(experiment_dir)
        return 0 if success else 1
    else:
        # List all experiment directories
        experiment_dirs = list_experiment_dirs()
        
        if not experiment_dirs:
            print("No experiment directories found in 'research_output'.")
            return 1
        
        print("Available experiment directories:")
        for i, exp_dir in enumerate(experiment_dirs, 1):
            print(f"{i}. {exp_dir.name}")
        
        # Prompt user to select an experiment directory
        try:
            choice = input("\nEnter the number of the experiment to regenerate report for (or 'all' for all): ")
            
            if choice.lower() == 'all':
                # Regenerate reports for all experiments
                success_count = 0
                for exp_dir in experiment_dirs:
                    if regenerate_report(exp_dir):
                        success_count += 1
                
                print(f"\nRegenerated reports for {success_count} out of {len(experiment_dirs)} experiments.")
                return 0
            else:
                # Regenerate report for selected experiment
                choice = int(choice)
                if 1 <= choice <= len(experiment_dirs):
                    exp_dir = experiment_dirs[choice - 1]
                    success = regenerate_report(exp_dir)
                    return 0 if success else 1
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(experiment_dirs)}.")
                    return 1
        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}")
            return 1

if __name__ == "__main__":
    sys.exit(main())