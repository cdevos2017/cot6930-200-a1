"""
Academic LaTeX style template for research reports.
This template is suitable for publication-style papers.
"""

# Academic style template suitable for publication
ACADEMIC_TEMPLATE = r"""
\documentclass[12pt,a4paper,twoside]{article}

% Core packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{mathpazo}            % Palatino font with math support
\usepackage{microtype}           % Improves typography
\usepackage{amsmath,amsfonts,amssymb}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{booktabs}            % Better tables
\usepackage{array}
\usepackage{multirow}
\usepackage{hyperref}
\usepackage{url}
\usepackage{listings}            % Code listings
\usepackage[ruled,vlined]{algorithm2e}  % Algorithms
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{float}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{abstract}

% Page settings
\usepackage[top=1in, bottom=1in, left=1.25in, right=1.25in]{geometry}

% Hyperlink settings
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    citecolor=blue,
    pdftitle={Prompt Engineering Research},
    pdfauthor={Research Framework},
    pdfkeywords={prompt engineering, LLM}
}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[RE]{Prompt Engineering Research}
\fancyhead[LO]{{{experiment_id}}}
\renewcommand{\headrulewidth}{0.4pt}

% Custom abstract style
\renewcommand{\abstractname}{ABSTRACT}
\renewcommand{\absnamepos}{flushleft}

% Title information
\title{\Large\textbf{Systematic Evaluation and Optimization of Automated Prompt Engineering Techniques}}
\author{Research Framework}
\date{{{generation_date}}}

\begin{document}

\begin{titlepage}
    \centering
    \vspace*{1cm}
    
    {\scshape\LARGE Research Report \par}
    \vspace{1.5cm}
    
    {\huge\bfseries {{title}} \par}
    \vspace{2cm}
    
    {\Large\itshape Experiment ID: {{experiment_id}} \par}
    \vspace{1cm}
    
    {\large Generated on: {{generation_date}}\par}
    
    \vfill
    
    % Bottom of the page
    {\large Prompt Engineering Research Framework\par}
\end{titlepage}

\begin{abstract}
{{report_description}}
This research systematically evaluates the effectiveness of various prompt engineering techniques 
across different task domains. Using a comprehensive framework that tested {{num_experiments}} 
experimental conditions, we quantitatively analyze technique performance, parameter impact, 
and role detection accuracy. The findings provide empirical evidence for optimizing prompt 
engineering strategies in large language model applications.
\end{abstract}

\tableofcontents
\newpage

\section{Introduction}
\subsection{Research Motivation}
The effectiveness of large language models (LLMs) is highly dependent on the quality of prompts 
used to guide their responses. However, prompt engineering remains largely an art rather than 
a science, with practitioners relying on intuition and trial-and-error approaches. This research 
aims to establish a systematic framework for evaluating and optimizing prompt engineering techniques.

\subsection{Research Questions}
Our research addresses the following key questions:
\begin{enumerate}
    \item How can we systematically evaluate the effectiveness of different prompt engineering techniques?
    \item Which techniques perform best for which types of tasks?
    \item How do model parameters interact with prompt techniques to affect response quality?
    \item Can we automate the process of prompt refinement to achieve consistently high-quality outputs?
\end{enumerate}

\subsection{Background}
Manual prompt engineering requires expertise and multiple iterations to achieve high-quality results.
Different techniques such as chain-of-thought, tree-of-thought, and structured output approaches
have emerged, but their comparative effectiveness across different tasks remains understudied.
Our research builds on previous work in prompt engineering while introducing a novel framework
for systematic evaluation and optimization.

\section{Methodology}
\subsection{Research Framework}
We employ a multi-stage automated prompt refinement system that combines:
\begin{itemize}
    \item Rule-based template selection and validation
    \item LLM-based prompt analysis and improvement
    \item Dynamic role and technique detection
    \item Iterative quality assessment
    \item Parameter optimization
\end{itemize}

\subsection{Experimental Design}
\subsubsection{Test Cases}
{% if test_cases %}
Our experiment used the following test cases to represent diverse task domains:

\begin{table}[h]
\centering
\caption{Experimental Test Cases}
\begin{tabular}{>{\raggedright\arraybackslash}p{0.3\textwidth}>{\raggedright\arraybackslash}p{0.15\textwidth}>{\raggedright\arraybackslash}p{0.2\textwidth}>{\raggedright\arraybackslash}p{0.2\textwidth}}
\toprule
\textbf{Query} & \textbf{Category} & \textbf{Expected Role} & \textbf{Expected Technique} \\
\midrule
{% for case in test_cases %}
{{ case.query }} & {{ case.category }} & {{ case.expected_role }} & {{ case.expected_technique }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}
{% else %}
Test case information was not available in the experiment data.
{% endif %}

\subsubsection{Techniques Evaluated}
{% if techniques %}
The framework systematically tested the following prompt engineering techniques:
\begin{itemize}
{% for technique in techniques %}
    \item \textbf{ {{technique}} }
{% endfor %}
\end{itemize}
{% else %}
Specific technique information was not available in the experiment data.
{% endif %}

\subsubsection{Parameter Configurations}
{% if parameter_sets %}
Each technique was tested across multiple parameter configurations:

\begin{table}[h]
\centering
\caption{Parameter Configurations}
\begin{tabular}{ccc}
\toprule
\textbf{Temperature} & \textbf{Context Window} & \textbf{Prediction Length} \\
\midrule
{% for params in parameter_sets %}
{{ params.temperature }} & {{ params.num_ctx }} & {{ params.num_predict }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}
{% else %}
Specific parameter set information was not available in the experiment data.
{% endif %}

\subsubsection{Evaluation Metrics}
Our primary evaluation metrics included:
\begin{itemize}
    \item Quality score (0.0-1.0) assessed by LLM-based evaluators
    \item Number of refinement iterations required
    \item Processing time
    \item Role detection accuracy
\end{itemize}

\section{Results}
\subsection{Technique Performance}
{% if technique_performance %}
The following results show the performance metrics for each evaluated technique:

\begin{table}[h]
\centering
\caption{Technique Performance Comparison}
\begin{tabular}{lccc}
\toprule
\textbf{Technique} & \textbf{Avg. Quality} & \textbf{Std. Deviation} & \textbf{Avg. Iterations} \\
\midrule
{% for tech, metrics in technique_performance.items() %}
{{ tech }} & {{ "%.2f"|format(metrics.avg_quality) }} & {{ "%.2f"|format(metrics.std_quality) }} & {{ "%.1f"|format(metrics.avg_iterations) }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.technique_comparison}}}
\caption{Quality score distribution by technique. Higher scores indicate more effective prompt engineering techniques.}
\label{fig:technique_comparison}
\end{figure}
{% else %}
Technique performance data was not available in the experiment data.
{% endif %}

\subsection{Parameter Impact Analysis}
{% if parameter_impact %}
Our analysis revealed significant impacts of parameter configurations on performance:

\begin{table}[h]
\centering
\caption{Parameter Impact on Quality and Performance}
\begin{tabular}{lcc}
\toprule
\textbf{Parameter Set} & \textbf{Avg. Quality} & \textbf{Avg. Time (s)} \\
\midrule
{% for param_key, metrics in parameter_impact.items() %}
{{ param_key }} & {{ "%.2f"|format(metrics.avg_quality) }} & {{ "%.2f"|format(metrics.avg_time) }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.parameter_impact}}}
\caption{Relationship between temperature settings and quality scores across all techniques.}
\label{fig:parameter_impact}
\end{figure}
{% else %}
Parameter impact data was not available in the experiment data.
{% endif %}

\subsection{Quality Distribution}
Figure \ref{fig:quality_distribution} shows the distribution of quality scores across all experiments,
providing insight into the overall effectiveness of the tested prompt engineering approaches.

\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.quality_distribution}}}
\caption{Distribution of quality scores across all experiments.}
\label{fig:quality_distribution}
\end{figure}

\subsection{Efficiency Analysis}
Processing time is an important consideration for practical applications of prompt engineering.
Figure \ref{fig:time_analysis} presents the average processing time required by each technique.

\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.time_analysis}}}
\caption{Average processing time by technique.}
\label{fig:time_analysis}
\end{figure}

\subsection{Iteration Analysis}
The relationship between iteration count and quality score provides insight into the refinement
process efficiency. Figure \ref{fig:iteration_analysis} illustrates this relationship.

\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.iteration_analysis}}}
\caption{Relationship between number of iterations and quality score.}
\label{fig:iteration_analysis}
\end{figure}

\subsection{Role Detection Accuracy}
Our framework's ability to correctly detect appropriate expert roles for different tasks
is shown in Figure \ref{fig:role_accuracy}.

\begin{figure}[h]
\centering
\includegraphics[width=0.6\textwidth]{{{viz_paths.role_accuracy}}}
\caption{Role detection accuracy across all experiments.}
\label{fig:role_accuracy}
\end{figure}

\section{Discussion}
\subsection{Key Findings}
{% if key_findings %}
Our research revealed several important findings:
\begin{itemize}
{% for finding in key_findings %}
    \item {{ finding }}
{% endfor %}
\end{itemize}
{% else %}
No specific key findings were extracted from the experiment data.
{% endif %}

\subsection{Technique Effectiveness Analysis}
{% if best_technique %}
The \textbf{ {{best_technique}} } technique demonstrated superior performance with an average quality score 
of {{ "%.2f"|format(best_technique_quality) }}. This suggests that {%- if best_technique == "chain_of_thought" %} 
structured step-by-step reasoning significantly improves prompt effectiveness
{%- elif best_technique == "tree_of_thought" %}
exploring multiple reasoning paths leads to more effective prompts
{%- elif best_technique == "structured_output" %}
providing explicit formatting guidelines enhances prompt performance
{%- elif best_technique == "role_playing" %}
adopting expert personas improves the quality of prompt responses
{%- elif best_technique == "socratic" %}
using a question-based approach leads to more effective prompts
{%- else %}
this particular technique offers advantages for the types of tasks evaluated
{%- endif %}.
{% else %}
The experiment data didn't clearly identify a single best-performing technique.
{% endif %}

\subsection{Parameter Optimization Insights}
{% if best_params %}
Our analysis identified \textbf{ {{best_params}} } as the optimal parameter configuration,
with an average quality score of {{ "%.2f"|format(best_params_quality) }}. This finding has 
important implications for practical prompt engineering, suggesting that
{%- if "temp_0.2" in best_params %}
lower temperature settings that produce more deterministic outputs may be preferable
{%- elif "temp_0.7" in best_params or "temp_0.8" in best_params %}
higher temperature settings that allow for more creative responses may be advantageous
{%- elif "temp_0.5" in best_params %}
moderate temperature settings that balance creativity and consistency may be optimal
{%- else %}
specific parameter configurations can significantly impact prompt effectiveness
{%- endif %}.
{% else %}
The experiment data didn't clearly identify optimal parameter settings.
{% endif %}

\subsection{Limitations}
Several limitations should be considered when interpreting our findings:
\begin{itemize}
    \item The evaluation relies on LLM-based quality assessment, which may introduce biases
    \item Our test cases, while diverse, may not represent all possible task domains
    \item The framework was tested with a limited set of parameter configurations
    \item Interactions between techniques and specific task types require further investigation
\end{itemize}

\section{Conclusion and Future Work}
\subsection{Conclusion}
This research establishes a systematic framework for evaluating and optimizing prompt engineering
techniques. Our findings demonstrate that technique selection and parameter tuning significantly
impact prompt quality and response consistency. The automated refinement system shows promise
for improving prompt engineering efficiency and effectiveness.

\subsection{Future Research Directions}
Based on our findings, we propose several promising directions for future research:

\subsubsection{Extended Parameter Space Exploration}
\begin{itemize}
    \item Testing wider ranges of temperature and context window sizes
    \item Investigating impact of other model parameters
    \item Exploring adaptive parameter selection based on task characteristics
\end{itemize}

\subsubsection{Advanced Technique Combinations}
\begin{itemize}
    \item Hybrid approaches combining strengths of multiple techniques
    \item Task-specific technique optimization frameworks
    \item Novel prompt engineering patterns based on empirical findings
\end{itemize}

\subsubsection{Automation Enhancements}
\begin{itemize}
    \item More sophisticated role and technique detection algorithms
    \item Advanced quality metrics incorporating multiple evaluation dimensions
    \item Real-time technique adaptation based on model behavior
\end{itemize}

\subsubsection{Domain-Specific Optimization}
\begin{itemize}
    \item Detailed analysis of technique effectiveness per task domain
    \item Custom techniques for specialized fields such as medicine, law, etc.
    \item Comparative benchmarking across different model architectures
\end{itemize}

\appendix
\section{Experimental Details}
\subsection{Experiment Summary}
Total experiments run: {{num_experiments}}
{% if experiment_counts %}
\begin{table}[h]
\centering
\caption{Experiment Distribution by Technique}
\begin{tabular}{lc}
\toprule
\textbf{Technique} & \textbf{Number of Experiments} \\
\midrule
{% for technique, count in experiment_counts.items() %}
{{ technique }} & {{ count }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}
{% endif %}

\subsection{Implementation Architecture}
The research framework was implemented using a modular architecture with the following components:
\begin{itemize}
    \item \textbf{Prompt Refinement Engine} - Iterative improvement of prompts using LLM feedback
    \item \textbf{Template Generator} - Dynamic selection of appropriate templates based on task
    \item \textbf{Experiment Controller} - Management of experiment runs and result collection
    \item \textbf{Analysis Module} - Statistical analysis and visualization of results
    \item \textbf{Reporting System} - Generation of research reports in multiple formats
\end{itemize}

\section{Statistical Appendix}
{% if statistics %}
\begin{table}[h]
\centering
\caption{Detailed Statistical Metrics}
\begin{tabular}{lc}
\toprule
\textbf{Metric} & \textbf{Value} \\
\midrule
{% for key, value in statistics.items() %}
{{ key }} & {{ value }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}
{% else %}
Detailed statistical analysis was not performed on this experiment data.
{% endif %}

\end{document}
"""