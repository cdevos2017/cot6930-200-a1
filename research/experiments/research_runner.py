# research/research_runner.py

# No relative imports - use absolute imports
from research.framework import PromptResearchFramework
from research.reporting.reporter import ResearchReporter


def main():
    """Run the complete research process with robust error handling"""
    
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
        
        # Debug output - show first result as example
        for key, value in results[0].items():
            if isinstance(value, dict):
                # Format dictionaries better for display
                dict_preview = "{" + ", ".join(f"'{k}': '{str(v)[:20]}...'" if isinstance(v, str) and len(str(v)) > 20 
                                    else f"'{k}': {v}" for k, v in list(value.items())[:3]) + "}"
                if len(value) > 3:
                    dict_preview = dict_preview[:-1] + ", ...}"
                print(f"  {key}: {dict_preview}")
            else:
                print(f"  {key}: {value}")
        
        print("\nPhase 2: Analyzing Results")
        print("-------------------------")
        # Framework analyzes the results
        analysis = framework.analyze_results(results)
        
        # Debug output - show analysis structure
        print("\nAnalysis structure:")
        for key, value in analysis.items():
            if isinstance(value, dict):
                print(f"  {key}: {type(value)} with keys {list(value.keys())}")
            else:
                print(f"  {key}: {value}")
        
        print("\nPhase 3: Generating Report")
        print("-------------------------")
        # Reporter generates and saves everything
        report = reporter.generate_report(results, analysis)
        output_dir = reporter.save_report(report)
        
        print("\nResearch completed successfully!")
        print(f"\nOutputs saved in: {output_dir}")
        print("\nGenerated files:")
        
        # Check if files were actually saved
        expected_files = ["research_report.md", "raw_results.json", "analysis_summary.json"]
        visualization_dir = output_dir / "visualizations"
        
        for file_name in expected_files:
            file_path = output_dir / file_name
            if file_path.exists():
                file_size = file_path.stat().st_size
                print(f"- {file_name} ({file_size} bytes)")
            else:
                print(f"- {file_name} NOT FOUND")
        
        if visualization_dir.exists():
            viz_files = list(visualization_dir.glob("*.png"))
            print(f"- visualizations/ ({len(viz_files)} files)")
            for viz_file in viz_files:
                print(f"  - {viz_file.name} ({viz_file.stat().st_size} bytes)")
        else:
            print("- visualizations/ NOT FOUND")
        
    except Exception as e:
        print(f"\nError during research execution: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full stack trace for debugging

if __name__ == "__main__":
    main()