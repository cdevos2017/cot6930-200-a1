### Running Custom Experiments

##  Custom Experiment Runner
- `custom_experiment.py`: Lets you run experiments with specific test case categories or custom test cases
- Supports command-line arguments for full customization
- Can generate LaTeX reports as part of the experiment

```bash
# Run with standard test cases
python custom_experiment.py --standard

# Run with technical test cases
python custom_experiment.py --technical

# Run with all test cases
python custom_experiment.py --all

# Run with your own test cases
python custom_experiment.py --custom my_test_cases.json

# Limit the number of test cases
python custom_experiment.py --technical --limit 2

# Specify which techniques to test
python custom_experiment.py --academic --techniques "chain_of_thought,socratic"

# Generate a LaTeX report
python custom_experiment.py --business --latex
```

### Creating Custom Test Cases

##  Modular Test Cases
- `research/test_cases.py`: Contains all test cases organized by category
- Updated `framework.py` to use the separate test cases module
- Added methods to set custom test cases, techniques, and parameters

You can create your own test cases in a JSON file:

```json
[
    {
        "query": "Write a function to find prime numbers",
        "category": "programming",
        "expected_role": "Software Engineer",
        "expected_technique": "chain_of_thought",
        "description": "Prime number algorithm task"
    },
    {
        "query": "Explain quantum computing to a 10-year-old",
        "category": "explanation",
        "expected_role": "Teacher",
        "expected_technique": "socratic",
        "description": "Simplified explanation task"
    }
]
```

### Generating LaTeX Reports for Existing Experiments

##  LaTeX Report Generator
- `latex_report_generator.py`: Creates LaTeX reports from experiment data that can be compiled to PDF
- Multiple style templates in separate files:
  - `latex_style_academic.py`: Academic paper style for formal publications
  - `latex_style_business.py`: Business/professional style with modern formatting

You can generate LaTeX reports for any existing experiment:

```bash
python latex_report_generator.py experiment_20250224_190643
```

## Benefits of the New Structure

1. **Easier Customization**: You can now modify test cases without changing the core framework
2. **Better Organization**: Code is more modular and easier to maintain
3. **Professional Reports**: Generate publication-quality LaTeX reports
4. **Flexible Experimentation**: Run targeted experiments with specific categories of test cases
5. **Comprehensive Analysis**: Get detailed insights with beautiful visualizations and statistical analysis