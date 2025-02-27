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

## **Authors**
- **Chad Devos, M.S.** ([GitHub](https://github.com/cdevos2017))
- **Supervised by:** [Dr. Fernando Koch](http://www.fernandokoch.me)  
- **Affiliation:** Generative Intelligence Lab, FAU  

## 📑 Research Report

The full research paper detailing the comparative study and findings can be found [here](research/research_report.pdf).

---

# **Research Question**
**How can multi-level prompt engineering techniques improve the quality, comprehensiveness, and consistency of requirements extracted from natural language descriptions?**  

---

## **Arguments & Research Goals**  

### **What is already known about this topic?**  
- Prompt engineering influences **output quality** but often requires **expert-level tuning** for best results.
- **Chain-of-thought, tree-of-thought, and self-consistency** methods can improve responses but are **task-dependent.**
- **Parameter tuning (temperature, context window, and length constraints)** affects consistency.
- Requirements analysis **is inherently ambiguous** and requires **iterative refinement** to achieve clarity.
- **Large Language Models (LLMs)** can automate requirements extraction **if properly guided** with structured prompts.

### **What this research explores**
- **Implementation of a multi-stage prompt refinement system** combining:  
  ✅ **Rule-based template generation**  
  ✅ **Dynamic meta-prompting techniques**  
  ✅ **Stateful chaining of prompts** for iterative improvement  
  ✅ **Parameter optimization** for different requirement analysis categories  
  ✅ **Evaluation of Level-1 (meta-prompt) and Level-2 (chained prompting) techniques**

### **Implications for Practice**
- **Automated, high-quality requirements extraction** with **minimal manual intervention**.
- **Standardized, template-based prompt refinement** leading to **more structured outputs**.
- **Improved requirements elicitation** across **diverse domains**.
- **Enhanced consistency and accuracy** in **LLM-driven requirement analysis.**

---

# **Research Methodology**
The project implements a **multi-step prompt refinement system** tested under various configurations.

### **📌 Framework Overview**
The implemented framework consists of the following **core components**:

1️⃣ **Prompt Refiner:**  
- Iteratively improves prompts through **automated quality scoring** and **LLM-based refinements.**  
- Implements a **feedback loop** to ensure continuous optimization.  

2️⃣ **Template Generator:**  
- Dynamically selects **the best prompt template** based on the detected **requirement type, role, and technique.**  

3️⃣ **Analysis Module:**  
- Evaluates **LLM outputs** using **qualitative and quantitative scoring.**  
- Parses **structured requirements** for key quality attributes.  

4️⃣ **Parameter Optimizer:**  
- Experiments with **temperature, context length, and response size** to determine optimal configurations.  

5️⃣ **Experimental Setup:**  
- Tests various **prompt engineering techniques** across multiple requirement analysis tasks.
- **Compares Level-0, Level-1, and Level-2 techniques.**

### **Test Cases**
The experiments evaluate **eight different requirements analysis tasks**, including:
- **Requirements elicitation**
- **Requirements validation**
- **Non-functional requirements identification**
- **Stakeholder needs analysis**
- **Requirements conflict resolution**

---

# **Results & Analysis**

### **📊 Key Findings**
✅ **Level-1 (meta-prompting) and Level-2 (chained prompting) techniques outperform standard approaches.**  
✅ **Stepwise refinement (3-step chains) improves requirement clarity and structure.**  
✅ **Temperature tuning significantly affects quality, with 0.5 yielding optimal results.**  
✅ **Role-based prompting improves extraction accuracy but suffers from misclassification issues.**  
✅ **Automated prompt refinement achieves consistent gains, particularly for complex requirements.**  

### **📉 Performance Evaluation**
#### 1️⃣ **Technique Effectiveness**
- **Role-Playing & Chain-of-Thought outperform standard zero-shot prompting.**
- **Level-2 Techniques showed the highest average quality score (0.87).**

#### 2️⃣ **Parameter Impact**
- **Temperature = 0.5 consistently produced the most balanced results.**
- **Expanding the context window beyond 2048 tokens had **no significant benefit** in requirements tasks.  

#### 3️⃣ **Prompt Refinement Progression**
- **3 iterations** were optimal; increasing to **5 degraded quality** due to **over-refinement.**
- **Divergent-Convergent techniques performed best for ambiguous requirements.**
- **Adversarial prompting improved conflict detection in requirements documents.**

---

# **Implementation Details**
The repository contains **modularized implementations** for **prompt engineering, experimentation, and reporting.**

### **📂 Project Structure**
```
📁 prompt/                     # Prompt refinement modules
 ├── prompt_refiner.py        # Main prompt refiner system
 ├── template_generator.py     # Dynamic prompt template selection
 ├── techniques.py             # Implementation of Level-0, Level-1, and Level-2 techniques
 ├── analyzers.py              # Output quality analysis and scoring
 ├── parameters.py             # Optimization of LLM parameters
 ├── utils.py                  # Utility functions

📁 research/                    # Experimentation framework
 ├── experiments/              # Test cases and configurations
 ├── reporting/                # Research reporting tools
 ├── visualization.py          # Graph generation for research results
 ├── framework.py              # Experimentation framework controller
```

---

# **Further Research & Next Steps**
🔎 **Extending Automated Requirements Traceability**  
📊 **Adaptive Prompt Optimization for Different Models**  
🤖 **Hybrid Human-LLM Collaboration for Requirements Validation**  
🚀 **Domain-Specific Adaptations for Regulated Industries**  

---

# **How to Use This Project**
### **1️⃣ Install Dependencies**
```
pip install -r requirements.txt
```

### **2️⃣ Run Experiments**
```
python research_runner.py
```

### **3️⃣ Generate Research Report**
```
python report_regenerator.py
```

### **4️⃣ Visualize Results**
```
python visualization.py
```

---

# **Final Remarks**
This research builds upon the **Prompt Engineering Lab** and expands its capabilities by integrating **multi-level automation techniques for requirements analysis.** The **empirical evaluation** confirms the effectiveness of **meta-prompting and refinement chaining**, contributing to the **advancement of structured LLM-assisted requirements engineering.**  

