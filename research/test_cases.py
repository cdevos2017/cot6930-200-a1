"""
Test cases for prompt engineering research.

This module contains test cases for the prompt engineering research framework.
Each test case includes a query, category, expected role, and expected technique.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class TestCase:
    """Definition of a prompt engineering test case"""
    query: str
    category: str
    expected_role: str
    expected_technique: str
    description: str

# Standard test cases for general prompt engineering research
STANDARD_TEST_CASES = [
    TestCase(
        query="Write a Python function to calculate the Fibonacci sequence",
        category="coding",
        expected_role="Software Engineer",
        expected_technique="chain_of_thought",
        description="Algorithm implementation task"
    ),
    TestCase(
        query="Explain why the sky is blue",
        category="explanation",
        expected_role="Physicist",
        expected_technique="socratic",
        description="Scientific explanation task"
    ),
    TestCase(
        query="Analyze the impact of social media on mental health",
        category="analysis",
        expected_role="Psychologist",
        expected_technique="tree_of_thought",
        description="Complex analysis task"
    ),
    TestCase(
        query="Create a marketing strategy for a new eco-friendly product",
        category="business",
        expected_role="Business Analyst",
        expected_technique="structured_output",
        description="Strategic planning task"
    ),
    TestCase(
        query="Solve this equation: 3x^2 + 2x - 5 = 0",
        category="math",
        expected_role="Mathematician",
        expected_technique="chain_of_thought",
        description="Mathematical problem-solving task"
    )
]

# Test cases focused on creative writing
CREATIVE_WRITING_TEST_CASES = [
    TestCase(
        query="Write a short story about a robot who discovers emotions",
        category="creative_writing",
        expected_role="Creative Writer",
        expected_technique="role_playing",
        description="Creative fiction writing task"
    ),
    TestCase(
        query="Compose a poem about the changing seasons",
        category="poetry",
        expected_role="Poet",
        expected_technique="role_playing",
        description="Poetry composition task"
    ),
    TestCase(
        query="Develop a character profile for a fantasy novel protagonist",
        category="character_development",
        expected_role="Creative Writer",
        expected_technique="structured_output",
        description="Character development task"
    ),
    TestCase(
        query="Write dialogue between two people who just discovered they're long-lost siblings",
        category="dialogue",
        expected_role="Screenwriter",
        expected_technique="role_playing",
        description="Dialogue writing task"
    ),
    TestCase(
        query="Create an engaging introduction for an article about climate change",
        category="article_writing",
        expected_role="Journalist",
        expected_technique="tree_of_thought",
        description="Article introduction task"
    )
]

# Test cases focused on technical topics
TECHNICAL_TEST_CASES = [
    TestCase(
        query="Explain how a transformer neural network architecture works",
        category="machine_learning",
        expected_role="Data Scientist",
        expected_technique="chain_of_thought",
        description="Technical explanation task"
    ),
    TestCase(
        query="Compare microservices and monolithic architecture approaches",
        category="software_architecture",
        expected_role="Systems Architect",
        expected_technique="tree_of_thought",
        description="Architectural comparison task"
    ),
    TestCase(
        query="Write a SQL query to find the top 5 customers by purchase amount",
        category="database",
        expected_role="Database Administrator",
        expected_technique="chain_of_thought",
        description="SQL query writing task"
    ),
    TestCase(
        query="Describe the process of asymmetric encryption in simple terms",
        category="cybersecurity",
        expected_role="Security Expert",
        expected_technique="socratic",
        description="Security concept explanation task"
    ),
    TestCase(
        query="Create a flowchart for a user authentication system",
        category="system_design",
        expected_role="Systems Architect",
        expected_technique="structured_output",
        description="System flowchart design task"
    )
]

# Test cases focused on academic writing and research
ACADEMIC_TEST_CASES = [
    TestCase(
        query="Synthesize the current research on renewable energy storage solutions",
        category="literature_review",
        expected_role="Research Scientist",
        expected_technique="tree_of_thought",
        description="Research synthesis task"
    ),
    TestCase(
        query="Formulate a hypothesis for studying the effects of caffeine on memory",
        category="research_design",
        expected_role="Research Scientist",
        expected_technique="socratic",
        description="Hypothesis formulation task"
    ),
    TestCase(
        query="Analyze the methodological limitations of a study on vaccine effectiveness",
        category="critical_analysis",
        expected_role="Academic Researcher",
        expected_technique="chain_of_thought",
        description="Methodology analysis task"
    ),
    TestCase(
        query="Write an abstract for a paper on the economic impacts of climate change",
        category="academic_writing",
        expected_role="Economics Professor",
        expected_technique="structured_output",
        description="Abstract writing task"
    ),
    TestCase(
        query="Outline a research proposal on the impact of social media on political polarization",
        category="grant_writing",
        expected_role="Political Scientist",
        expected_technique="structured_output",
        description="Research proposal task"
    )
]

# Test cases focused on business and professional writing
BUSINESS_TEST_CASES = [
    TestCase(
        query="Draft a press release announcing a company's new sustainability initiative",
        category="press_release",
        expected_role="Public Relations Specialist",
        expected_technique="structured_output",
        description="Press release writing task"
    ),
    TestCase(
        query="Create a SWOT analysis for a small coffee shop entering a competitive market",
        category="business_analysis",
        expected_role="Business Analyst",
        expected_technique="structured_output",
        description="SWOT analysis task"
    ),
    TestCase(
        query="Write a persuasive email to potential investors for a tech startup",
        category="persuasive_writing",
        expected_role="Marketing Strategist",
        expected_technique="role_playing",
        description="Persuasive email task"
    ),
    TestCase(
        query="Develop a 30-second elevator pitch for a new mobile app",
        category="marketing",
        expected_role="Marketing Strategist",
        expected_technique="chain_of_thought",
        description="Elevator pitch task"
    ),
    TestCase(
        query="Create a project timeline for developing and launching a new website",
        category="project_management",
        expected_role="Project Manager",
        expected_technique="structured_output",
        description="Project timeline task"
    )
]

def get_all_test_cases() -> List[TestCase]:
    """Get all available test cases"""
    all_cases = []
    all_cases.extend(STANDARD_TEST_CASES)
    all_cases.extend(CREATIVE_WRITING_TEST_CASES)
    all_cases.extend(TECHNICAL_TEST_CASES)
    all_cases.extend(ACADEMIC_TEST_CASES)
    all_cases.extend(BUSINESS_TEST_CASES)
    return all_cases

def get_test_cases_by_category(category: str) -> List[TestCase]:
    """Get test cases filtered by category"""
    all_cases = get_all_test_cases()
    return [case for case in all_cases if case.category == category]