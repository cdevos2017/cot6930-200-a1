"""
Business/Professional LaTeX style template for research reports.
This template uses modern styling with color highlights.
"""

# Modern business/conference style template
BUSINESS_TEMPLATE = r"""
\documentclass[11pt,letterpaper]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{helvet}               % Use Helvetica font
\renewcommand{\familydefault}{\sfdefault}
\usepackage{microtype}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{array}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{float}
\usepackage{caption}
\usepackage{tcolorbox}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{geometry}

% Colors
\definecolor{primary}{RGB}{0, 83, 155}    % Deep blue
\definecolor{secondary}{RGB}{183, 28, 28} % Deep red
\definecolor{tertiary}{RGB}{38, 50, 56}   % Dark grey
\definecolor{light}{RGB}{245, 245, 245}   % Light grey

% Page setup
\geometry{margin=1in}

% Title format
\titleformat{\section}
  {\normalfont\Large\bfseries\color{primary}}
  {\thesection}{1em}{}
\titleformat{\subsection}
  {\normalfont\large\bfseries\color{tertiary}}
  {\thesubsection}{1em}{}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    filecolor=primary,
    urlcolor=primary,
    citecolor=secondary,
    pdftitle={Prompt Engineering Research Report},
    pdfauthor={Research Framework},
    pdfsubject={Prompt Engineering Research},
    pdfkeywords={prompt engineering, LLM, AI, research}
}

% Header/footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{primary}{Prompt Engineering Research}}
\fancyhead[R]{\textcolor{primary}{{{experiment_id}}}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{primary}\leaders\hrule height \headrulewidth\hfill}}
\renewcommand{\footrule}{\hbox to\headwidth{\color{primary}\leaders\hrule height \footrulewidth\hfill}}

\begin{document}

% Title page
\begin{titlepage}
    \begin{center}
        \vspace*{1cm}
        
        \includegraphics[width=0.5\textwidth]{example-image}
        
        \vspace{1.5cm}
        {\Huge\bfseries\textcolor{primary}{Prompt Engineering}\par}
        {\Huge\bfseries\textcolor{secondary}{Research Report}\par}
        \vspace{1cm}
        {\Large\textcolor{tertiary}{Experiment ID: {{experiment_id}}}\par}
        \vspace{0.5cm}
        {\large Generated on: {{generation_date}}\par}
        
        \vfill
        
        \begin{tcolorbox}[colback=light,colframe=primary,width=\textwidth,arc=0mm]
        \centering
        \large {{report_description}}
        \end{tcolorbox}
        
        \vfill
        
        {\large\textcolor{tertiary}{Prompt Engineering Research Framework}\par}
    \end{center}
\end{titlepage}

\tableofcontents
\newpage

\section{Executive Summary}
\begin{tcolorbox}[colback=light,colframe=primary]
This report presents findings from a comprehensive analysis of {{num_experiments}} experiments
evaluating prompt engineering techniques for large language models. Our research systematically 
compares different approaches and parameter settings to optimize prompt effectiveness.

{% if key_findings %}
\textbf{Key Findings:}
\begin{itemize}
{% for finding in key_findings %}
    \item {{ finding }}
{% endfor %}
\end{itemize}
{% endif %}
\end{tcolorbox}

\section{Introduction}
\subsection{Research Question}
How can we systematically evaluate and optimize automated prompt engineering techniques to improve prompt quality, response consistency, and task-specific performance?

\subsection{Background}
\begin{itemize}
    \item Manual prompt engineering requires expertise and multiple iterations
    \item Different techniques perform better for different types of tasks
    \item Template-based approaches help standardize prompt construction
    \item Parameter tuning significantly affects model response quality
\end{itemize}

\section{Methodology}
\subsection{Research Approach}
Our multi-stage automated prompt refinement system combines:
\begin{itemize}
    \item Rule-based template selection and validation
    \item LLM-based prompt analysis and improvement
    \item Dynamic role and technique detection
    \item Iterative quality assessment
    \item Parameter optimization
\end{itemize}

\subsection{Test Cases}
{% if test_cases %}
\begin{table}[h]
\centering
\caption{Test Cases}
\begin{tabular}{>{\columncolor{light}}p{0.3\textwidth}p{0.15\textwidth}p{0.2\textwidth}p{0.2\textwidth}}
\toprule
\rowcolor{primary} \textcolor{white}{\textbf{Query}} & \textcolor{white}{\textbf{Category}} & \textcolor{white}{\textbf{Expected Role}} & \textcolor{white}{\textbf{Expected Technique}} \\
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

\subsection{Techniques and Parameters}
\begin{multicols}{2}
\subsubsection{Techniques Evaluated}
{% if techniques %}
\begin{itemize}
{% for technique in techniques %}
    \item \textbf{ {{technique}} }
{% endfor %}
\end{itemize}
{% else %}
Technique information not available.
{% endif %}

\columnbreak

\subsubsection{Parameter Sets}
{% if parameter_sets %}
\begin{itemize}
{% for params in parameter_sets %}
    \item Temperature: {{ params.temperature }}, Context: {{ params.num_ctx }}, Predict: {{ params.num_predict }}
{% endfor %}
\end{itemize}
{% else %}
Parameter information not available.
{% endif %}
\end{multicols}

\section{Results}
\subsection{Technique Performance}
{% if technique_performance %}
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.technique_comparison}}}
\caption{Comparison of quality scores across different techniques}
\label{fig:technique_comparison}
\end{figure}

\begin{table}[h]
\centering
\caption{Technique Performance Metrics}
\begin{tabular}{>{\columncolor{light}}lrrr}
\toprule
\rowcolor{primary} \textcolor{white}{\textbf{Technique}} & \textcolor{white}{\textbf{Avg. Quality}} & \textcolor{white}{\textbf{Std. Deviation}} & \textcolor{white}{\textbf{Avg. Iterations}} \\
\midrule
{% for tech, metrics in technique_performance.items() %}
{{ tech }} & {{ "%.2f"|format(metrics.avg_quality) }} & {{ "%.2f"|format(metrics.std_quality) }} & {{ "%.1f"|format(metrics.avg_iterations) }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}
{% else %}
Technique performance data was not available in the experiment data.
{% endif %}

\subsection{Parameter Impact}
{% if parameter_impact %}
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{{{viz_paths.parameter_impact}}}
\caption{Impact of temperature on quality scores}
\label{fig:parameter_impact}
\end{figure}

\begin{table}[h]
\centering
\caption{Parameter Impact on Performance}
\begin{tabular}{>{\columncolor{light}}lrr}
\toprule
\rowcolor{primary} \textcolor{white}{\textbf{Parameter Set}} & \textcolor{white}{\textbf{Avg. Quality}} & \textcolor{white}{\textbf{Avg. Time (s)}} \\
\midrule
{% for param_key, metrics in parameter_impact.items() %}
{{ param_key }} & {{ "%.2f"|format(metrics.avg_quality) }} & {{ "%.2f"|format(metrics.avg_time) }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}
{% else %}
Parameter impact data was not available in the experiment data.
{% endif %}

\subsection{Additional Insights}
\begin{multicols}{2}
\subsubsection{Quality Distribution}
\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{{{viz_paths.quality_distribution}}}
\caption{Distribution of quality scores}
\label{fig:quality_distribution}
\end{figure}

\columnbreak

\subsubsection{Role Accuracy}
\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{{{viz_paths.role_accuracy}}}
\caption{Role selection accuracy}
\label{fig:role_accuracy}
\end{figure}
\end{multicols}

\begin{multicols}{2}
\subsubsection{Time Analysis}
\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{{{viz_paths.time_analysis}}}
\caption{Processing time by technique}
\label{fig:time_analysis}
\end{figure}

\columnbreak

\subsubsection{Iteration Impact}
\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{{{viz_paths.iteration_analysis}}}
\caption{Quality vs iterations}
\label{fig:iteration_analysis}
\end{figure}
\end{multicols}

\section{Conclusions \& Recommendations}
\begin{tcolorbox}[colback=light,colframe=secondary,title=Key Conclusions]
{% if best_technique %}
\textbf{Best Technique:} The \textbf{ {{best_technique}} } technique demonstrated superior performance
with an average quality score of {{ "%.2f"|format(best_technique_quality) }}.
{% endif %}

{% if best_params %}
\textbf{Optimal Parameters:} The parameter configuration \textbf{ {{best_params}} } produced
the highest average quality scores ({{ "%.2f"|format(best_params_quality) }}).
{% endif %}

\textbf{Overall Finding:} Technique selection and parameter tuning significantly impact prompt
quality and should be tailored to specific task requirements.
\end{tcolorbox}

\subsection{Recommendations}
\begin{enumerate}
    \item \textbf{Technique Selection:} {% if best_technique %}Prioritize the {{best_technique}} technique for most tasks.{% else %}Evaluate multiple techniques for each task type.{% endif %}
    
    \item \textbf{Parameter Optimization:} {% if best_params %}Use {{best_params}} as a starting point for parameter tuning.{% else %}Test multiple parameter configurations for each technique.{% endif %}
    
    \item \textbf{Implementation Strategy:} Adopt an iterative approach to prompt refinement with automated quality assessment.
    
    \item \textbf{Future Development:} Invest in task-specific optimization and hybrid technique approaches.
\end{enumerate}

\section{Future Research Directions}
\begin{itemize}
    \item Extended parameter space exploration
    \item Additional technique combinations
    \item Automation improvements
    \item Task-specific optimization
\end{itemize}

\appendix
\section{Experiment Details}
\subsection{Experiment Metadata}
\begin{itemize}
    \item \textbf{Experiment ID:} {{experiment_id}}
    \item \textbf{Date Generated:} {{generation_date}}
    \item \textbf{Total Experiments:} {{num_experiments}}
\end{itemize}

{% if statistics %}
\subsection{Detailed Statistics}
\begin{table}[h]
\centering
\caption{Statistical Summary}
\begin{tabular}{>{\columncolor{light}}lr}
\toprule
\rowcolor{primary} \textcolor{white}{\textbf{Metric}} & \textcolor{white}{\textbf{Value}} \\
\midrule
{% for key, value in statistics.items() %}
{{ key }} & {{ value }} \\
\midrule
{% endfor %}
\bottomrule
\end{tabular}
\end{table}
{% endif %}

\end{document}
"""