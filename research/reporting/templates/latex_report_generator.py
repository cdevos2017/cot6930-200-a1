#!/usr/bin/env python3
"""
LaTeX Report Generator - Generate LaTeX reports from experiment data.

This script can take experiment data and generate a professional LaTeX report,
which can then be compiled into a PDF.

Usage:
    python latex_report_generator.py [experiment_id]

If experiment_id is not provided, it will list all available experiment directories.

Requirements:
    - A LaTeX distribution (e.g., TeX Live, MiKTeX) must be installed to compile the output.
    - Python packages: jinja2 for templating
"""

import sys
import os
import json
import subprocess
from pathlib import Path
import datetime
from typing import Dict, List, Any, Optional

try:
    import jinja2
except ImportError:
    print("Error: jinja2 package is required for LaTeX templating.")
    print("Please install it using: pip install jinja2")
    sys.exit(1)

# Default LaTeX template
LATEX_TEMPLATE = r"""
\documentclass[11pt,a4paper]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{multicol}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{float}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{listings}
\usepackage{fancyhdr}

% Page setup
\usepackage[top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm]{geometry}

% Custom colors
\definecolor{mypurple}{RGB}{100,0,100}
\definecolor{myblue}{RGB}{0,0,150}
\definecolor{mygreen}{RGB}{0,100,0}

% Header/footer
\pagestyle{fancy}
\fancyhf{}
\lhead{Prompt Engineering Research}
\rhead{{{experiment_id}}}
\lfoot{Generated on {{generation_date}}}
\rfoot{Page \thepage}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=myblue,
    filecolor=myblue,
    urlcolor=myblue,
    citecolor=mygreen,
    pdftitle={Prompt Engineering Research Report},
    pdfauthor={Research Framework},
    pdfsubject={Automated Prompt Engineering Analysis},
    pdfkeywords={prompt engineering, LLM, research}
}

% Title information
\title{\LARGE \textbf{Automated Prompt Engineering Research Report}}
\author{Research Framework}
\date{{{generation_date}}}

\begin{document}

\maketitle

\begin{abstract}
\noindent {{report_description}}
This report analyzes the effectiveness of various prompt engineering techniques 
and parameters across different task types. The research was conducted using 
an automated framework that tested {{num_experiments}} experimental conditions.
The report presents quantitative findings on technique effectiveness, parameter 
impact, and role detection accuracy.
\end{abstract}

\tableofcontents
\newpage

\section{Introduction}
\subsection{Research Question}
How can we systematically evaluate and optimize automated prompt engineering techniques 
to improve prompt quality, response consistency, and task-specific performance?

\subsection{Research Context}
\begin{itemize}
    \item Manual prompt engineering requires expertise and multiple iterations to achieve high-quality results
    \item Different techniques (chain-of-thought, tree-of-thought, etc.) work better for different types of tasks
    \item Template-based approaches can help standardize prompt construction
    \item Parameter tuning significantly affects model response quality and consistency
\end{itemize}

\subsection{Research Approach}
We employ a multi-stage automated prompt refinement system that combines:
\begin{itemize}
    \item Rule-based template selection and validation
    \item LLM-based prompt analysis and improvement
    \item Dynamic role and technique detection
    \item Iterative quality assessment
    \item Parameter optimization
\end{itemize}

\section{Methodology}
\subsection{Experiment Structure}
This research builds a comparative analysis framework to evaluate:
\begin{itemize}
    \item Different prompt engineering techniques
    \item Impact of role-based vs technique-based refinements
    \item Effects of parameter variations on response quality
    \item Model response consistency across different tasks
\end{itemize}

\subsection{Test Cases}
The following test cases were used in this research:
{% if test_cases %}
\begin{table}[h]
\centering
\caption{Test Cases}
\begin{tabular}{|p{0.3\textwidth}|p{0.15\textwidth}|p{0.2\textwidth}|p{0.2\textwidth}|}
\hline
\textbf{Query} & \textbf{Category} & \textbf{Expected Role} & \textbf{Expected Technique} \\
\hline
{% for case in test_cases %}
{{ case.query }} & {{ case.category }} & {{ case.expected_role }} & {{ case.expected_technique }} \\
\hline
{% endfor %}
\end{tabular}
\end{table}
{% else %}
Test case information was not available in the experiment data.
{% endif %}

\subsection{Techniques and Parameters}
The framework tested the following prompt engineering techniques and parameter combinations:

\subsubsection{Techniques}
{% if techniques %}
\begin{itemize}
{% for technique in techniques %}
    \item \textbf{ {{technique}} }
{% endfor %}
\end{itemize}
{% else %}
Specific technique information was not available in the experiment data.
{% endif %}

\subsubsection{Parameter Sets}
{% if parameter_sets %}
\begin{table}[h]
\centering
\caption{Parameter Sets}
\begin{tabular}{|c|c|c|}
\hline
\textbf{Temperature} & \textbf{Context Window} & \textbf{Prediction Length} \\
\hline
{% for params in parameter_sets %}
{{ params.temperature }} & {{ params.num_ctx }} & {{ params.num_predict }} \\
\hline
{% endfor %}
\end{tabular}
\end{table}
{% else %}
Specific parameter set information was not available in the experiment data.
{% endif %}

\section{Results}
\subsection{Technique Performance}
{% if technique_performance %}
The following table shows the performance metrics for each tested technique:

\begin{table}[h]
\centering
\caption{Technique Performance Comparison}
\begin{tabular}{|l|c|c|c|}
\hline
\textbf{Technique} & \textbf{Avg. Quality} & \textbf{Std. Deviation} & \textbf{Avg. Iterations} \\
\hline
{% for tech, metrics in technique_performance.items() %}
{{ tech }} & {{ "%.2f"|format(metrics.avg_quality) }} & {{ "%.2f"|format(metrics.std_quality) }} & {{ "%.1f"|format(metrics.avg_iterations) }} \\
\hline
{% endfor %}
\end{tabular}
\end{table}

\subsubsection{Visual Comparison}
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.technique_comparison}}}
\caption{Comparison of quality scores across different techniques}
\label{fig:technique_comparison}
\end{figure}
{% else %}
Technique performance data was not available in the experiment data.
{% endif %}

\subsection{Parameter Impact}
{% if parameter_impact %}
The following table shows the impact of different parameter combinations:

\begin{table}[h]
\centering
\caption{Parameter Impact on Performance}
\begin{tabular}{|l|c|c|}
\hline
\textbf{Parameter Set} & \textbf{Avg. Quality} & \textbf{Avg. Time (s)} \\
\hline
{% for param_key, metrics in parameter_impact.items() %}
{{ param_key }} & {{ "%.2f"|format(metrics.avg_quality) }} & {{ "%.2f"|format(metrics.avg_time) }} \\
\hline
{% endfor %}
\end{tabular}
\end{table}

\subsubsection{Visual Comparison}
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.parameter_impact}}}
\caption{Impact of temperature on quality scores}
\label{fig:parameter_impact}
\end{figure}
{% else %}
Parameter impact data was not available in the experiment data.
{% endif %}

\subsection{Quality Distribution}
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.quality_distribution}}}
\caption{Distribution of quality scores across all experiments}
\label{fig:quality_distribution}
\end{figure}

\subsection{Time Analysis}
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.time_analysis}}}
\caption{Processing time by technique}
\label{fig:time_analysis}
\end{figure}

\subsection{Iteration Impact}
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.iteration_analysis}}}
\caption{Relationship between number of iterations and quality score}
\label{fig:iteration_analysis}
\end{figure}

\subsection{Role Selection Accuracy}
\begin{figure}[h]
\centering
\includegraphics[width=0.6\textwidth]{{{viz_paths.role_accuracy}}}
\caption{Role selection accuracy}
\label{fig:role_accuracy}
\end{figure}

\section{Key Findings}
{% if key_findings %}
\begin{itemize}
{% for finding in key_findings %}
    \item {{ finding }}
{% endfor %}
\end{itemize}
{% else %}
No specific key findings were extracted from the experiment data.
{% endif %}

\section{Discussion}
\subsection{Technique Effectiveness}
{% if best_technique %}
The \textbf{ {{best_technique}} } technique showed the highest average quality score 
({{ "%.2f"|format(best_technique_quality) }}), suggesting that this approach may be most effective
for the types of tasks tested in this research.
{% else %}
The experiment data didn't clearly identify a single best-performing technique.
{% endif %}

\subsection{Parameter Optimization}
{% if best_params %}
The parameter combination \textbf{ {{best_params}} } produced the highest average quality scores
({{ "%.2f"|format(best_params_quality) }}). This suggests that these settings may offer a good 
balance between exploration and coherence for the model.
{% else %}
The experiment data didn't clearly identify optimal parameter settings.
{% endif %}

\section{Future Research Directions}
\begin{itemize}
    \item \textbf{Extended Parameter Space Exploration}
    \begin{itemize}
        \item Testing wider ranges of temperature and context window sizes
        \item Investigating impact of other model parameters
        \item Exploring adaptive parameter selection
    \end{itemize}
    
    \item \textbf{Additional Technique Combinations}
    \begin{itemize}
        \item Hybrid approaches combining multiple techniques
        \item Task-specific technique optimization
        \item Novel prompt engineering patterns
    \end{itemize}
    
    \item \textbf{Automation Improvements}
    \begin{itemize}
        \item Enhanced role and technique detection
        \item More sophisticated quality metrics
        \item Real-time technique adaptation
    \end{itemize}
    
    \item \textbf{Task-Specific Optimization}
    \begin{itemize}
        \item Detailed analysis of technique effectiveness per task type
        \item Custom techniques for specific domains
        \item Performance benchmarking across different task categories
    \end{itemize}
\end{itemize}

\section{Conclusion}
This research demonstrates that automated prompt engineering can be systematically evaluated
using a multi-stage refinement system. The findings suggest that technique selection and parameter
tuning have significant impacts on prompt quality and response consistency. Further research is
needed to develop more sophisticated approaches for task-specific optimization and to explore
hybrid techniques that combine the strengths of different prompt engineering approaches.

\appendix
\section{Experiment Details}
\subsection{Raw Results Summary}
Total experiments run: {{num_experiments}}
{% if experiment_counts %}
\begin{table}[h]
\centering
\caption{Experiment Counts by Technique}
\begin{tabular}{|l|c|}
\hline
\textbf{Technique} & \textbf{Number of Experiments} \\
\hline
{% for technique, count in experiment_counts.items() %}
{{ technique }} & {{ count }} \\
\hline
{% endfor %}
\end{tabular}
\end{table}
{% endif %}

\subsection{Technical Implementation}
The research framework was implemented in Python and consists of the following major components:
\begin{itemize}
    \item \textbf{Prompt Refinement System} - Iteratively improves prompt quality
    \item \textbf{Template Generator} - Selects appropriate templates based on task type
    \item \textbf{Research Framework} - Manages experiments and collects results
    \item \textbf{Visualization Module} - Generates data visualizations
    \item \textbf{Reporting System} - Creates research reports from experiment data
\end{itemize}

\section{Statistical Analysis}
{% if statistics %}
\begin{table}[h]
\centering
\caption{Summary Statistics}
\begin{tabular}{|l|c|}
\hline
\textbf{Metric} & \textbf{Value} \\
\hline
{% for key, value in statistics.items() %}
{{ key }} & {{ value }} \\
\hline
{% endfor %}
\end{tabular}
\end{table}
{% else %}
Detailed statistical analysis was not performed on this experiment data.
{% endif %}

\end{document}
"""

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

def extract_test_cases(results):
    """Extract test cases from results"""
    test_cases = []
    seen_queries = set()
    
    for result in results:
        query = result.get('query')
        if query and query not in seen_queries:
            test_case = {
                'query': query,
                'category': result.get('category', 'Unknown'),
                'expected_role': result.get('expected_role', 'Unknown'),
                'expected_technique': result.get('expected_technique', 'Unknown')
            }
            test_cases.append(test_case)
            seen_queries.add(query)
    
    return test_cases

def extract_techniques_and_params(results):
    """Extract techniques and parameter sets from results"""
    techniques = set()
    parameter_sets = []
    param_set_hashes = set()
    
    for result in results:
        # Extract technique
        technique = result.get('technique_used')
        if technique:
            techniques.add(technique)
        
        # Extract parameter set
        params = result.get('parameters_used')
        if params and isinstance(params, dict):
            # Create a hash of the parameter values to avoid duplicates
            param_hash = hash(frozenset(params.items()))
            if param_hash not in param_set_hashes:
                parameter_sets.append(params)
                param_set_hashes.add(param_hash)
    
    return list(techniques), parameter_sets

def extract_key_findings(analysis):
    """Extract key findings from analysis data"""
    findings = []
    
    # Best technique finding
    best_technique = None
    best_technique_quality = 0
    technique_performance = analysis.get('technique_performance', {})
    
    for technique, metrics in technique_performance.items():
        quality = metrics.get('avg_quality', 0)
        if quality > best_technique_quality:
            best_technique_quality = quality
            best_technique = technique
    
    if best_technique:
        findings.append(f"Best performing technique: {best_technique} (avg quality: {best_technique_quality:.2f})")
    
    # Best parameters finding
    best_params = None
    best_params_quality = 0
    parameter_impact = analysis.get('parameter_impact', {})
    
    for param_key, metrics in parameter_impact.items():
        quality = metrics.get('avg_quality', 0)
        if quality > best_params_quality:
            best_params_quality = quality
            best_params = param_key
    
    if best_params:
        findings.append(f"Optimal parameters: {best_params} (avg quality: {best_params_quality:.2f})")
    
    # Role accuracy finding
    role_accuracy = analysis.get('role_accuracy')
    if role_accuracy is not None:
        findings.append(f"Overall role detection accuracy: {role_accuracy:.2%}")
    
    # Time metrics finding
    time_metrics = analysis.get('time_metrics', {})
    avg_time = time_metrics.get('average_time')
    if avg_time is not None:
        findings.append(f"Average processing time: {avg_time:.2f}s")
    
    return findings

def calculate_experiment_counts(results):
    """Calculate experiment counts by technique"""
    counts = {}
    
    for result in results:
        technique = result.get('technique_used')
        if technique:
            counts[technique] = counts.get(technique, 0) + 1
    
    return counts

def calculate_statistics(results, analysis):
    """Calculate summary statistics"""
    statistics = {}
    
    # Quality score statistics
    quality_scores = [r.get('quality_score', 0) for r in results if 'quality_score' in r]
    if quality_scores:
        statistics['Mean Quality Score'] = f"{sum(quality_scores) / len(quality_scores):.2f}"
        statistics['Min Quality Score'] = f"{min(quality_scores):.2f}"
        statistics['Max Quality Score'] = f"{max(quality_scores):.2f}"
    
    # Iteration statistics
    iterations = [r.get('iterations_used', 0) for r in results if 'iterations_used' in r]
    if iterations:
        statistics['Mean Iterations'] = f"{sum(iterations) / len(iterations):.2f}"
        statistics['Min Iterations'] = f"{min(iterations)}"
        statistics['Max Iterations'] = f"{max(iterations)}"
    
    # Role accuracy
    role_accuracy = analysis.get('role_accuracy')
    if role_accuracy is not None:
        statistics['Role Detection Accuracy'] = f"{role_accuracy:.2%}"
    
    return statistics

def generate_latex_report(experiment_dir, results, analysis):
    """Generate a LaTeX report from experiment data"""
    # Extract data for the report
    test_cases = extract_test_cases(results)
    techniques, parameter_sets = extract_techniques_and_params(results)
    key_findings = extract_key_findings(analysis)
    experiment_counts = calculate_experiment_counts(results)
    statistics = calculate_statistics(results, analysis)
    
    # Determine best technique and parameters for discussion section
    best_technique = None
    best_technique_quality = 0
    technique_performance = analysis.get('technique_performance', {})
    
    for technique, metrics in technique_performance.items():
        quality = metrics.get('avg_quality', 0)
        if quality > best_technique_quality:
            best_technique_quality = quality
            best_technique = technique
    
    best_params = None
    best_params_quality = 0
    parameter_impact = analysis.get('parameter_impact', {})
    
    for param_key, metrics in parameter_impact.items():
        quality = metrics.get('avg_quality', 0)
        if quality > best_params_quality:
            best_params_quality = quality
            best_params = param_key
    
    # Get visualization paths relative to the experiment directory
    viz_dir = experiment_dir / "visualizations"
    viz_paths = {
        'technique_comparison': str(viz_dir / 'technique_comparison.png'),
        'parameter_impact': str(viz_dir / 'parameter_impact.png'),
        'quality_distribution': str(viz_dir / 'quality_distribution.png'),
        'time_analysis': str(viz_dir / 'time_analysis.png'),
        'iteration_analysis': str(viz_dir / 'iteration_analysis.png'),
        'role_accuracy': str(viz_dir / 'role_accuracy.png')
    }
    
    # Create template
    template = jinja2.Template(LATEX_TEMPLATE)
    
    # Render template with data
    report = template.render(
        experiment_id=experiment_dir.name,
        generation_date=datetime.datetime.now().strftime("%Y-%m-%d"),
        report_description=analysis.get('description', "Investigating the effectiveness of automated prompt refinement systems."),
        num_experiments=len(results),
        test_cases=test_cases,
        techniques=techniques,
        parameter_sets=parameter_sets,
        technique_performance=technique_performance,
        parameter_impact=parameter_impact,
        viz_paths=viz_paths,
        key_findings=key_findings,
        best_technique=best_technique,
        best_technique_quality=best_technique_quality,
        best_params=best_params,
        best_params_quality=best_params_quality,
        experiment_counts=experiment_counts,
        statistics=statistics
    )
    
    return report

def compile_latex(tex_file_path):
    """Compile LaTeX file to PDF using pdflatex"""
    try:
        # Run pdflatex twice to resolve references
        subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file_path], 
                      cwd=tex_file_path.parent, check=True)
        subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file_path], 
                      cwd=tex_file_path.parent, check=True)
        
        # Check if PDF was created
        pdf_path = tex_file_path.with_suffix('.pdf')
        if pdf_path.exists():
            print(f"LaTeX compilation successful: {pdf_path}")
            return True
        else:
            print(f"Error: PDF file was not created")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")
        return False
    except FileNotFoundError:
        print("Error: pdflatex not found. Please install LaTeX (e.g., TeX Live, MiKTeX).")
        return False

def generate_report_for_experiment(experiment_dir):
    """Generate a LaTeX report for an experiment"""
    print(f"Generating LaTeX report for {experiment_dir.name}...")
    
    # Load experiment data
    results, analysis = load_experiment_data(experiment_dir)
    if results is None or analysis is None:
        print("Failed to load experiment data.")
        return False
    
    try:
        # Generate LaTeX report
        latex_content = generate_latex_report(experiment_dir, results, analysis)
        
        # Save LaTeX file
        tex_file_path = experiment_dir / f"{experiment_dir.name}_report.tex"
        with open(tex_file_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"LaTeX report saved to: {tex_file_path}")
        
        # Ask user if they want to compile to PDF
        compile_to_pdf = input("Do you want to compile the LaTeX report to PDF? (y/n): ")
        if compile_to_pdf.lower() in ('y', 'yes'):
            if compile_latex(tex_file_path):
                pdf_path = tex_file_path.with_suffix('.pdf')
                print(f"PDF report generated: {pdf_path}")
            else:
                print("PDF compilation failed.")
        
        return True
    
    except Exception as e:
        print(f"Error generating LaTeX report: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    # Handle command-line arguments
    if len(sys.argv) > 1:
        # Generate report for specific experiment ID
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
        
        success = generate_report_for_experiment(experiment_dir)
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
            choice = input("\nEnter the number of the experiment to generate a LaTeX report for (or 'all' for all): ")
            
            if choice.lower() == 'all':
                # Generate reports for all experiments
                success_count = 0
                for exp_dir in experiment_dirs:
                    if generate_report_for_experiment(exp_dir):
                        success_count += 1
                
                print(f"\nGenerated LaTeX reports for {success_count} out of {len(experiment_dirs)} experiments.")
                return 0
            else:
                # Generate report for selected experiment
                choice = int(choice)
                if 1 <= choice <= len(experiment_dirs):
                    exp_dir = experiment_dirs[choice - 1]
                    success = generate_report_for_experiment(exp_dir)
                    return 0 if success else 1
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(experiment_dirs)}.")
                    return 1
        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}")
            return 1

if __name__ == "__main__":
    sys.exit(main())