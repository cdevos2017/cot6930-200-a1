# setup.py

from setuptools import setup, find_packages

setup(
    name="prompt_research",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'seaborn',
        'pandas',
        'numpy',
        'requests',
        'jinja2'  # Added missing dependencies
    ]
)