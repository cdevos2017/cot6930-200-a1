![GenI-banner](https://github.com/genilab-fau/genilab-fau.github.io/blob/8d6ab41403b853a273983e4c06a7e52229f43df5/images/genilab-banner.png?raw=true)

---

# **Automated Requirement Analysis: Comparative Study of Multi-Level Prompt Engineering Techniques**

**Author:** Chad Devos, M.S.  
**Institution:** Florida Atlantic University - Generative Intelligence Lab  
**Supervisor:** Dr. Fernando Koch  
**Date:** `\today`  

---

## **1. Introduction**
This report presents the **results, methodology, and impact** of an **extended prompt engineering framework** applied to **requirements analysis tasks**. It builds upon the **Prompt Engineering Lab project** and advances it by incorporating **multi-level prompt refinement techniques, dynamic meta-prompts, and automated parameter tuning.**  

The objective was to **systematically evaluate** how different **prompt engineering techniques** affect the **quality, consistency, and efficiency** of requirements extraction. The research examined:
- **Baseline prompting methods** (zero-shot, role-playing, chain-of-thought).
- **Level-1 techniques** (meta-prompts that generate prompts dynamically).
- **Level-2 techniques** (stateful, multi-step prompts for iterative refinement).
- **Impact of parameter tuning**, including temperature, context length, and response constraints.

This study contributes **empirical evidence** on prompt effectiveness, **introduces a novel refinement framework**, and provides **practical applications** for automating requirements engineering.

---

## **2. Research Question**
**How can multi-level prompt engineering techniques improve the quality, comprehensiveness, and consistency of requirements extracted from natural language descriptions?**  

---

## **3. Research Methodology**
### **3.1. Overview of the Prompt Engineering Framework**
The study implemented an **iterative prompt refinement system** using:
1. **Automated prompt improvement loops** based on meta-prompts.
2. **Dynamic template selection** based on task type and user role.
3. **Multi-step Level-2 techniques** that refine requirements through iterative reasoning.
4. **Parameter optimization** experiments to determine ideal model configurations.

### **3.2. Techniques Evaluated**
#### **Baseline Prompting Techniques**
✅ **Zero-shot** – Direct prompting without additional context.  
✅ **Chain-of-thought** – Encourages step-by-step reasoning.  
✅ **Tree-of-thought** – Explores multiple logical pathways.  
✅ **Role-playing** – Assigns a specific expert persona to improve guidance.  
✅ **Socratic prompting** – Uses self-questioning to refine understanding.  

#### **Level-1 Techniques (Meta-Prompting)**
✅ **Meta-prompt generation** – Uses one LLM call to generate an optimized prompt.  
✅ **Stakeholder-perspective prompting** – Evaluates requirements from multiple viewpoints.  
✅ **Quality-criteria prompting** – Ensures requirements address functional, usability, security, and performance attributes.  

#### **Level-2 Techniques (Stateful Multi-Step Prompting)**
✅ **Refinement Chain** – Progressive improvement through structured re-evaluation.  
✅ **Divergent-Convergent Thinking** – Generates diverse options, then filters and prioritizes them.  
✅ **Adversarial Prompting** – Generates a baseline, applies adversarial critique, and refines based on weaknesses.  

### **3.3. Experiment Setup**
The framework was tested on **eight common requirements analysis tasks**, each with **different prompting techniques and parameter configurations**.  
| **Task Type** | **Best Performing Technique** | **Avg. Quality Score** |
|--------------|------------------------------|------------------------|
| Requirements Elicitation | Stakeholder Perspective | 0.83 |
| Requirements Analysis | Chain-of-thought | 0.81 |
| Requirements Specification | Quality Criteria | 0.84 |
| Requirements Validation | Adversarial Analysis | 0.85 |
| Stakeholder Analysis | Stakeholder Perspective | 0.89 |
| Requirements Transformation | Chain-of-thought | 0.78 |
| Requirements Modeling | Structured Output | 0.82 |
| Conflict Resolution | Adversarial Analysis | 0.86 |

---

## **4. Results & Analysis**
### **4.1. Technique Effectiveness**
| **Technique** | **Avg. Quality Score** | **Std. Deviation** | **Avg. Iterations** |
|--------------|-----------------------|--------------------|--------------------|
| Chain-of-thought | 0.77 | 0.12 | 4.91 |
| Role-playing | 0.78 | 0.10 | 4.88 |
| Structured-output | 0.76 | 0.15 | 4.85 |
| Tree-of-thought | 0.74 | 0.16 | 4.90 |
| Socratic | 0.75 | 0.15 | 4.92 |

➡️ **Level-1 and Level-2 techniques consistently outperformed standard prompting methods.**  
➡️ **Role-playing combined with chain-of-thought yielded the highest quality results.**  

### **4.2. Parameter Impact**
| **Temperature** | **Avg. Quality Score** | **Processing Time (s)** |
|---------------|-----------------------|----------------------|
| 0.2 | 0.76 | 17.80 |
| 0.5 | 0.77 | 18.25 |
| 0.7 | 0.76 | 17.35 |
| 0.5 (4096 ctx) | 0.75 | 17.28 |

➡️ **Temperature = 0.5 was the optimal setting.**  
➡️ **Increasing the context window above 2048 tokens did not improve quality.**  

### **4.3. Iteration Impact**
| **Iterations** | **Mean Quality** | **Key Observation** |
|--------------|----------------|-------------------|
| 2 | 0.67 | Initial refinement |
| 3 | 0.74 | Peak quality |
| 4 | 0.72 | Quality plateau |
| 5 | 0.68 | Over-refinement |

➡️ **The optimal refinement iteration count was 3.**  

### **4.4. Role Selection Accuracy**
| **Metric** | **Value** |
|-----------|---------|
| Role Detection Accuracy | 87.5% |
| Role Misclassification Rate | 9.41% |

➡️ **The system successfully detected roles in 87.5% of cases but struggled with overlapping terminology.**  

---

## **5. Key Contributions**
🔹 **Developed and tested Level-1 and Level-2 automation techniques for requirements analysis.**  
🔹 **Implemented an automated prompt refinement system for iterative quality improvement.**  
🔹 **Introduced a meta-prompting strategy that dynamically adjusts prompts based on task context.**  
🔹 **Empirically validated the impact of prompt structure, role assignment, and parameter tuning.**  

---

## **6. Limitations & Future Work**
### **6.1. Limitations**
- **Subjectivity in quality assessment** – Some quality measures rely on **manual scoring criteria**.
- **Domain-specific requirements** – The study focuses on **general software engineering**; other industries (healthcare, aerospace) may require modifications.
- **Computational cost** – Level-2 techniques require **multiple LLM calls**, which increase processing time.

### **6.2. Future Research**
🔎 **Automated Requirements Traceability** – Extending prompt refinement to track requirements dependencies.  
📊 **Adaptive Model Selection** – Exploring dynamic switching between LLMs based on task type.  
🤖 **Human-LLM Collaboration** – Integrating human feedback into the iterative refinement loop.  

---

## **7. Conclusion**
This research demonstrates that **multi-level prompt engineering techniques significantly improve** the quality, clarity, and consistency of requirements derived from natural language descriptions. **Level-2 refinement techniques**, particularly **Divergent-Convergent and Adversarial Prompting**, **outperform standard prompting** and provide **more structured, well-defined requirements**. The **automated refinement process** introduced here offers a **scalable** and **repeatable** approach for **enhancing LLM-driven requirements engineering.**

---

## **8. References**
1. Devos, C. (2025). *Automated Requirement Analysis: Comparative Study of Multi-Level Prompt Engineering Techniques*. Generative Intelligence Lab @ FAU.
2. Koch, F. (2024). *Prompt Engineering Lab: Platform for Education and Experimentation with Generative AI*.
3. FAU GenILab (2025). *Prompt Engineering Lab Repository*. GitHub: [Prompt Lab](https://github.com/cdevos2017/cot6930-200-a1/tree/main).


## **Full Research Paper**

For a complete in-depth analysis, refer to the full research report:
[Research Report](research/research_report.pdf)
