# research/visualizer.py

from typing import List, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd
import numpy as np

class ResearchVisualizer:
    """Generates visualizations for research results"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.viz_dir = output_dir / "visualizations"
        self.viz_dir.mkdir(exist_ok=True)
        
        # Set style
        plt.style.use('seaborn')
        sns.set_palette("husl")
    
    def generate_all_visualizations(self, results: List[Any], analysis: Dict[str, Any]):
        """Generate all visualizations for the research"""
        # Convert results to DataFrame for easier plotting
        df = pd.DataFrame([vars(r) for r in results])
        
        # Generate each type of visualization
        self.plot_technique_comparison(df)
        self.plot_parameter_impact(df)
        self.plot_quality_distribution(df)
        self.plot_time_analysis(df)
        self.plot_iteration_analysis(df)
        self.plot_role_accuracy(analysis)
        
        plt.close('all')  # Clean up
    
    def plot_technique_comparison(self, df: pd.DataFrame):
        """Plot comparison of different techniques"""
        plt.figure(figsize=(12, 6))
        
        # Create grouped box plot
        sns.boxplot(x='technique', y='quality_score', data=df)
        
        plt.title('Quality Scores by Technique')
        plt.xlabel('Technique')
        plt.ylabel('Quality Score')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'technique_comparison.png')
        plt.close()
    
    def plot_parameter_impact(self, df: pd.DataFrame):
        """Plot impact of different parameters"""
        plt.figure(figsize=(12, 6))
        
        # Create temperature vs quality plot
        temps = df['parameters'].apply(lambda x: x['temperature'])
        sns.scatterplot(x=temps, y=df['quality_score'], alpha=0.6)
        
        plt.title('Quality Score vs Temperature')
        plt.xlabel('Temperature')
        plt.ylabel('Quality Score')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'parameter_impact.png')
        plt.close()
    
    def plot_quality_distribution(self, df: pd.DataFrame):
        """Plot distribution of quality scores"""
        plt.figure(figsize=(10, 6))
        
        # Create quality distribution plot
        sns.histplot(data=df, x='quality_score', bins=20, kde=True)
        
        plt.title('Distribution of Quality Scores')
        plt.xlabel('Quality Score')
        plt.ylabel('Count')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'quality_distribution.png')
        plt.close()
    
    def plot_time_analysis(self, df: pd.DataFrame):
        """Plot time analysis by technique"""
        plt.figure(figsize=(12, 6))
        
        # Create time vs technique plot
        sns.barplot(x='technique', y='time_taken', data=df)
        
        plt.title('Average Processing Time by Technique')
        plt.xlabel('Technique')
        plt.ylabel('Time (seconds)')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'time_analysis.png')
        plt.close()
    
    def plot_iteration_analysis(self, df: pd.DataFrame):
        """Plot iteration analysis"""
        plt.figure(figsize=(10, 6))
        
        # Create iterations vs quality plot
        sns.scatterplot(data=df, x='iterations_used', y='quality_score', hue='technique')
        
        plt.title('Quality Score vs Number of Iterations')
        plt.xlabel('Number of Iterations')
        plt.ylabel('Quality Score')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'iteration_analysis.png')
        plt.close()
    
    def plot_role_accuracy(self, analysis: Dict[str, Any]):
        """Plot role accuracy analysis"""
        plt.figure(figsize=(8, 8))
        
        # Create role accuracy pie chart
        accuracy = analysis.get('role_accuracy', 0)
        plt.pie([accuracy, 1-accuracy], 
                labels=['Correct', 'Incorrect'],
                autopct='%1.1f%%',
                colors=['#2ecc71', '#e74c3c'])
        
        plt.title('Role Selection Accuracy')
        
        plt.savefig(self.viz_dir / 'role_accuracy.png')
        plt.close()
    
    def get_visualization_paths(self) -> Dict[str, Path]:
        """Get paths to all generated visualizations"""
        return {
            'technique_comparison': self.viz_dir / 'technique_comparison.png',
            'parameter_impact': self.viz_dir / 'parameter_impact.png',
            'quality_distribution': self.viz_dir / 'quality_distribution.png',
            'time_analysis': self.viz_dir / 'time_analysis.png',
            'iteration_analysis': self.viz_dir / 'iteration_analysis.png',
            'role_accuracy': self.viz_dir / 'role_accuracy.png'
        }