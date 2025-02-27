![GenI-banner](https://github.com/genilab-fau/genilab-fau.github.io/blob/8d6ab41403b853a273983e4c06a7e52229f43df5/images/genilab-banner.png?raw=true)

# **Comparison of Prompt Refinement and Temperature Optimization Techniques for Various Requirements Analysis Tasks**

## **Project Overview**
This project is an **extension** of the Prompt Engineering Lab originally provided in the course. It expands the foundational framework by implementing **multi-level prompt engineering techniques** with a systematic **prompt refinement system** that improves requirements analysis tasks using **dynamic template generation, automated prompt refinement, and parameter tuning.** The research investigates how **Level-1 and Level-2 techniques** impact quality, consistency, and efficiency in **requirements extraction and analysis.**  

This project goes **beyond** the base implementation by:
- **Developing new techniques** for prompt refinement.
- **Experimenting with different parameters** to optimize results.
- **Performing an extensive comparative analysis** on technique effectiveness.
- **Automating prompt refinement and iterative evaluation.**
- **Generating empirical evidence** on prompt behavior across different **requirement types.**  
 
This work is based on the **Prompt Engineering Lab project** from:  
📌 **[Original Prompt Engineering Lab Repository](https://github.com/genilab-fau/prompt-eng)**  

---

# **How to Use This Project**
### **Install Dependencies**
```
pip install -r requirements.txt
```

### **Run Experiments**
```
python research_runner.py
```

### **Re-Generate Research Report if it is Missing**
```
python report_regenerator.py
```
### **Running Custom Experiments**

##  **Custom Experiment Runner**
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

### **Creating Custom Test Cases**

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
