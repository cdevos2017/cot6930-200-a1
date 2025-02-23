# research/run_research.py

from .framework import PromptResearchFramework
from .reporter import ResearchReporter

def main():
    # Initialize framework and reporter
    framework = PromptResearchFramework()
    reporter = ResearchReporter()
    
    print("Starting research experiment...")
    print("\nRunning experiments...")
    
    # Run evaluation
    results = framework.run_full_evaluation()
    
    print("\nAnalyzing results...")
    analysis = framework.analyze_results(results)
    
    print("\nGenerating research report...")
    report = reporter.generate_report(results, analysis)
    
    # Save report and get output directory
    output_dir = reporter.save_report(report)
    
    print(f"\nExperiment completed!")
    print(f"\nFiles saved in: {output_dir}")
    print(f"- Research report: research_report.md")
    print(f"- Raw results: raw_results.json")
    print(f"- Analysis summary: analysis_summary.json")
    
    # Print report preview
    print("\nResearch Report Preview:")
    print("=" * 80)
    markdown_report = reporter.format_markdown_report(report)
    print(markdown_report[:500] + "...\n")
    print("=" * 80)

if __name__ == "__main__":
    main()