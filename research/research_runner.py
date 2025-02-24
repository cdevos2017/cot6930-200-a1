# research/research_runner.py

import os
import sys

# No relative imports - use absolute imports
from research.framework import PromptResearchFramework
from research.reporter import ResearchReporter


def main():
    """Run the complete research process"""
    
    print("Starting Automated Prompt Engineering Research...")
    
    # Initialize both framework and reporter
    framework = PromptResearchFramework()  # This handles the experiments
    reporter = ResearchReporter()          # This handles reporting and visualization
    
    try:
        print("\nPhase 1: Running Experiments")
        print("----------------------------")
        # Framework conducts all the experiments
        results = framework.run_full_evaluation()
        
        print(f"\nCompleted {len(results)} experiments")
        
        print("\nPhase 2: Analyzing Results")
        print("-------------------------")
        # Framework analyzes the results
        analysis = framework.analyze_results(results)
        
        print("\nPhase 3: Generating Report")
        print("-------------------------")
        # Reporter generates and saves everything
        report = reporter.generate_report(results, analysis)
        output_dir = reporter.save_report(report)
        
        print("\nResearch completed successfully!")
        print(f"\nOutputs saved in: {output_dir}")
        print("\nGenerated files:")
        print("- research_report.md (Full research report with visualizations)")
        print("- raw_results.json (Detailed experimental data)")
        print("- analysis_summary.json (Analysis results)")
        print("- visualizations/ (Directory containing all graphs and charts)")
        
    except Exception as e:
        print(f"\nError during research execution: {str(e)}")
        raise

if __name__ == "__main__":
    # Ensure the script is run as the main module
    if __name__ == "__main__":
        main()
    else:
        print("This script should be run as the main module.")
        sys.exit(1)
#