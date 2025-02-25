# Requirements Analysis Prompt Engineering Research

This project conducts comparative analysis of multi-level prompt engineering techniques for requirements analysis tasks.

## Overview

The research evaluates several prompt engineering approaches:

### Level-1 Techniques
These techniques use a meta-prompt to generate a more effective prompt:

1. **Meta Prompt**: Uses a prompt to generate another prompt for requirement analysis
2. **Stakeholder Perspective**: Analyzes requirements from multiple stakeholder perspectives
3. **Quality Criteria**: Structures requirements using quality attributes

### Level-2 Techniques
These techniques use a series of chained prompts with state maintained between steps:

1. **Refinement Chain**: Three-step process that progressively refines requirements
2. **Divergent-Convergent**: Three-step process that first generates many possibilities, then evaluates, and finally selects and organizes the best requirements
3. **Adverse Analysis**: Three-step process that generates baseline requirements, adversarially analyzes them, and then hardens them against the identified issues

## Running the Experiment

```bash
# Run the full experiment
python -m research.requirements_analysis.requirements_analysis_experiment

# Run with only Level-1 techniques
python -m research.requirements_analysis.requirements_analysis_experiment --l1-only

# Run with only Level-2 techniques
python -m research.requirements_analysis.requirements_analysis_experiment --l2-only

# Limit the number of test cases (for faster testing)
python -m research.requirements_analysis.requirements_analysis_experiment --limit 2

# Generate a LaTeX report
python -m research.requirements_analysis.requirements_analysis_experiment --latex
```

## Project Structure

```
research/requirements_analysis/
├── requirements_analysis_experiment.py  # Main experiment script
├── requirements_test_cases.json         # Test cases
├── custom_parameters.json               # Parameter settings
└── README.md                            # This file
```

The actual techniques are implemented in `prompt/techniques.py` to make them reusable across the entire project.

## Dependencies

The experiment depends on the following project components:
- `research.framework`: Core experiment framework
- `research.test_cases`: Test case definitions
- `research.visualization`: Visualization utilities
- `research.reporting.reporter`: Reporting utilities
- `prompt.techniques`: Requirements analysis techniques

## Output

The experiment generates several types of output:
1. Standard research report with visualizations
2. Specialized visualizations for requirements analysis:
   - L1 vs. Standard comparison
   - L2 technique step progression
   - Category-specific quality analysis
   - Temperature impact analysis
3. LaTeX academic report (if --latex flag is used)

All outputs are saved to the `research/output` directory.

## Citation

```
@misc{requirement_analysis_prompt_engineering,
  author = {Your Name},
  title = {Automated Requirement Analysis: Comparative Study of Multi-Level Prompt Engineering Techniques},
  year = {2025},
  url = {https://github.com/yourusername/requirements-analysis-prompt-engineering}
}
```