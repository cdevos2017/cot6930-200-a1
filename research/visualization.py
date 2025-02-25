"""Visualization module for generating research report figures."""

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
        
        # Set style - using 'default' which is guaranteed to exist
        try:
            plt.style.use('default')
        except Exception as e:
            print(f"Warning: Could not set matplotlib style: {e}. Using fallback.")
        
        # Configure seaborn with direct settings instead of using style presets
        try:
            sns.set(color_codes=True)
            sns.set_palette("deep")
        except Exception as e:
            print(f"Warning: Could not configure seaborn: {e}")
    
    def generate_all_visualizations(self, results: List[Any], analysis: Dict[str, Any]):
        """Generate all visualizations for the research with error handling"""
        # Convert results to DataFrame for easier plotting
        try:
            df = pd.DataFrame(results)
            
            # Check if DataFrame is valid
            if df.empty:
                print("Warning: Empty DataFrame for visualization")
                self._create_empty_visualizations(self.viz_dir)
                return
        except Exception as e:
            print(f"Error creating DataFrame for visualization: {e}")
            self._create_empty_visualizations(self.viz_dir)
            return
            
        # Generate each visualization with error handling
        try:
            self.plot_technique_comparison(df)
            self.plot_parameter_impact(df)
            self.plot_quality_distribution(df)
            self.plot_time_analysis(df)
            self.plot_iteration_analysis(df)
            self.plot_role_accuracy(analysis)
        except Exception as e:
            print(f"Error during visualization generation: {e}")
            self._create_empty_visualizations(self.viz_dir)
        finally:
            plt.close('all')  # Clean up
    
    def _create_empty_visualizations(self, viz_dir: Path):
        """Create empty placeholder visualizations when data is missing"""
        visualizations = [
            'technique_comparison.png',
            'parameter_impact.png',
            'quality_distribution.png',
            'time_analysis.png',
            'iteration_analysis.png',
            'role_accuracy.png'
        ]
        
        for viz_name in visualizations:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, "No data available for visualization", 
                    ha='center', va='center', fontsize=14)
            plt.title(f"Missing Data for {viz_name.replace('.png', '')}")
            plt.tight_layout()
            plt.savefig(viz_dir / viz_name)
            plt.close()
    
    def plot_technique_comparison(self, df: pd.DataFrame):
        """Plot comparison of different techniques with error handling"""
        plt.figure(figsize=(12, 6))
        
        try:
            # Check if required columns exist
            if 'technique' not in df.columns or 'quality_score' not in df.columns:
                missing = []
                if 'technique' not in df.columns:
                    missing.append('technique')
                if 'quality_score' not in df.columns:
                    missing.append('quality_score')
                
                plt.text(0.5, 0.5, f"Missing columns: {', '.join(missing)}", 
                        ha='center', va='center', fontsize=14)
                plt.title('Quality Scores by Technique (Missing Data)')
            else:
                # Filter to valid data
                valid_data = df.dropna(subset=['technique', 'quality_score'])
                
                if valid_data.empty:
                    plt.text(0.5, 0.5, "No valid data points for comparison", 
                            ha='center', va='center', fontsize=14)
                    plt.title('Quality Scores by Technique (No Valid Data)')
                else:
                    # Create grouped box plot - use basic matplotlib instead of seaborn if needed
                    try:
                        sns.boxplot(x='technique', y='quality_score', data=valid_data)
                    except Exception as e:
                        print(f"Error using seaborn boxplot: {e}. Falling back to basic plot.")
                        # Fallback to basic matplotlib
                        techniques = valid_data['technique'].unique()
                        for i, tech in enumerate(techniques):
                            tech_data = valid_data[valid_data['technique'] == tech]['quality_score']
                            plt.boxplot(tech_data, positions=[i+1])
                        
                        plt.xticks(range(1, len(techniques)+1), techniques)
                        
                    plt.title('Quality Scores by Technique')
                    plt.xlabel('Technique')
                    plt.ylabel('Quality Score')
                    plt.xticks(rotation=45)
        except Exception as e:
            print(f"Error in technique comparison plot: {e}")
            plt.text(0.5, 0.5, f"Error creating plot: {str(e)}", 
                    ha='center', va='center', fontsize=14)
            plt.title('Quality Scores by Technique (Error)')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'technique_comparison.png')
        plt.close()
    
    def plot_parameter_impact(self, df: pd.DataFrame):
        """Plot impact of different parameters with error handling"""
        plt.figure(figsize=(12, 6))
        
        try:
            # Check if parameters column exists
            if 'parameters' not in df.columns or 'quality_score' not in df.columns:
                missing = []
                if 'parameters' not in df.columns:
                    missing.append('parameters')
                if 'quality_score' not in df.columns:
                    missing.append('quality_score')
                
                plt.text(0.5, 0.5, f"Missing columns: {', '.join(missing)}", 
                        ha='center', va='center', fontsize=14)
                plt.title('Parameter Impact (Missing Data)')
            else:
                # Process parameters safely
                try:
                    # Extract temperature value from parameters 
                    temps = []
                    quality_scores = []
                    
                    for _, row in df.iterrows():
                        params = row.get('parameters')
                        if isinstance(params, dict) and 'temperature' in params:
                            temp = params['temperature']
                            quality = row.get('quality_score')
                            if temp is not None and quality is not None:
                                temps.append(temp)
                                quality_scores.append(quality)
                    
                    if not temps:
                        plt.text(0.5, 0.5, "No valid temperature data available", 
                                ha='center', va='center', fontsize=14)
                        plt.title('Quality Score vs Temperature (No Valid Data)')
                    else:
                        # Create scatter plot
                        plt.scatter(temps, quality_scores, alpha=0.6)
                        plt.title('Quality Score vs Temperature')
                        plt.xlabel('Temperature')
                        plt.ylabel('Quality Score')
                except Exception as inner_e:
                    print(f"Error processing parameters data: {inner_e}")
                    plt.text(0.5, 0.5, f"Error processing data: {str(inner_e)}", 
                            ha='center', va='center', fontsize=14)
                    plt.title('Quality Score vs Temperature (Processing Error)')
        except Exception as e:
            print(f"Error in parameter impact plot: {e}")
            plt.text(0.5, 0.5, f"Error creating plot: {str(e)}", 
                    ha='center', va='center', fontsize=14)
            plt.title('Parameter Impact (Error)')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'parameter_impact.png')
        plt.close()
    
    def plot_quality_distribution(self, df: pd.DataFrame):
        """Plot distribution of quality scores with error handling"""
        plt.figure(figsize=(10, 6))
        
        try:
            # Check if quality_score column exists
            if 'quality_score' not in df.columns:
                plt.text(0.5, 0.5, "Missing 'quality_score' column in data", 
                        ha='center', va='center', fontsize=14)
                plt.title('Distribution of Quality Scores (Missing Data)')
            else:
                # Filter to valid quality scores
                valid_data = df.dropna(subset=['quality_score'])
                
                if valid_data.empty:
                    plt.text(0.5, 0.5, "No valid quality score data available", 
                            ha='center', va='center', fontsize=14)
                    plt.title('Distribution of Quality Scores (No Valid Data)')
                else:
                    try:
                        # Create quality distribution plot with seaborn
                        sns.histplot(data=valid_data, x='quality_score', bins=20, kde=True)
                    except Exception as e:
                        print(f"Error using seaborn histplot: {e}. Falling back to basic histogram.")
                        # Fallback to basic matplotlib
                        plt.hist(valid_data['quality_score'], bins=20, alpha=0.7)
                        
                    plt.title('Distribution of Quality Scores')
                    plt.xlabel('Quality Score')
                    plt.ylabel('Count')
        except Exception as e:
            print(f"Error in quality distribution plot: {e}")
            plt.text(0.5, 0.5, f"Error creating plot: {str(e)}", 
                    ha='center', va='center', fontsize=14)
            plt.title('Distribution of Quality Scores (Error)')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'quality_distribution.png')
        plt.close()
    
    def plot_time_analysis(self, df: pd.DataFrame):
        """Plot time analysis by technique with error handling"""
        plt.figure(figsize=(12, 6))
        
        try:
            # Check if required columns exist
            if 'technique' not in df.columns or 'time_taken' not in df.columns:
                missing = []
                if 'technique' not in df.columns:
                    missing.append('technique')
                if 'time_taken' not in df.columns:
                    missing.append('time_taken')
                
                plt.text(0.5, 0.5, f"Missing columns: {', '.join(missing)}", 
                        ha='center', va='center', fontsize=14)
                plt.title('Average Processing Time by Technique (Missing Data)')
            else:
                # Filter to valid data
                valid_data = df.dropna(subset=['technique', 'time_taken'])
                
                if valid_data.empty:
                    plt.text(0.5, 0.5, "No valid time data available", 
                            ha='center', va='center', fontsize=14)
                    plt.title('Average Processing Time by Technique (No Valid Data)')
                else:
                    try:
                        # Create time vs technique plot with seaborn
                        sns.barplot(x='technique', y='time_taken', data=valid_data)
                    except Exception as e:
                        print(f"Error using seaborn barplot: {e}. Falling back to basic bar chart.")
                        # Fallback to basic matplotlib
                        techniques = valid_data['technique'].unique()
                        tech_means = [valid_data[valid_data['technique'] == t]['time_taken'].mean() 
                                      for t in techniques]
                        plt.bar(range(len(techniques)), tech_means)
                        plt.xticks(range(len(techniques)), techniques)
                        
                    plt.title('Average Processing Time by Technique')
                    plt.xlabel('Technique')
                    plt.ylabel('Time (seconds)')
                    plt.xticks(rotation=45)
        except Exception as e:
            print(f"Error in time analysis plot: {e}")
            plt.text(0.5, 0.5, f"Error creating plot: {str(e)}", 
                    ha='center', va='center', fontsize=14)
            plt.title('Time Analysis (Error)')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'time_analysis.png')
        plt.close()
    
    def plot_iteration_analysis(self, df: pd.DataFrame):
        """Plot iteration analysis with error handling"""
        plt.figure(figsize=(10, 6))
        
        try:
            # Check if required columns exist
            if 'iterations_used' not in df.columns or 'quality_score' not in df.columns:
                missing = []
                if 'iterations_used' not in df.columns:
                    missing.append('iterations_used')
                if 'quality_score' not in df.columns:
                    missing.append('quality_score')
                
                plt.text(0.5, 0.5, f"Missing columns: {', '.join(missing)}", 
                        ha='center', va='center', fontsize=14)
                plt.title('Quality Score vs Number of Iterations (Missing Data)')
            else:
                # Filter to valid data
                valid_data = df.dropna(subset=['iterations_used', 'quality_score'])
                
                if valid_data.empty:
                    plt.text(0.5, 0.5, "No valid iteration data available", 
                            ha='center', va='center', fontsize=14)
                    plt.title('Quality Score vs Number of Iterations (No Valid Data)')
                else:
                    try:
                        # Create iterations vs quality plot with seaborn
                        if 'technique' in df.columns:
                            sns.scatterplot(data=valid_data, x='iterations_used', y='quality_score', hue='technique')
                        else:
                            sns.scatterplot(data=valid_data, x='iterations_used', y='quality_score')
                    except Exception as e:
                        print(f"Error using seaborn scatterplot: {e}. Falling back to basic scatter plot.")
                        # Fallback to basic matplotlib
                        plt.scatter(valid_data['iterations_used'], valid_data['quality_score'], alpha=0.6)
                        
                    plt.title('Quality Score vs Number of Iterations')
                    plt.xlabel('Number of Iterations')
                    plt.ylabel('Quality Score')
        except Exception as e:
            print(f"Error in iteration analysis plot: {e}")
            plt.text(0.5, 0.5, f"Error creating plot: {str(e)}", 
                    ha='center', va='center', fontsize=14)
            plt.title('Iteration Analysis (Error)')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'iteration_analysis.png')
        plt.close()
    
    def plot_role_accuracy(self, analysis: Dict[str, Any]):
        """Plot role accuracy analysis with error handling"""
        plt.figure(figsize=(8, 8))
        
        try:
            # Get role accuracy value
            role_accuracy = None
            
            # First check if it's directly in the analysis
            if 'role_accuracy' in analysis:
                role_accuracy = analysis.get('role_accuracy')
            # Then check if it's in detection_accuracy
            elif 'detection_accuracy' in analysis and 'role_detection_accuracy' in analysis['detection_accuracy']:
                role_accuracy = analysis['detection_accuracy'].get('role_detection_accuracy')
            
            if role_accuracy is None:
                plt.text(0.5, 0.5, "No role accuracy data available", 
                        ha='center', va='center', fontsize=14)
                plt.title('Role Selection Accuracy (Missing Data)')
            else:
                # Create role accuracy pie chart
                plt.pie([role_accuracy, 1-role_accuracy], 
                        labels=['Correct', 'Incorrect'],
                        autopct='%1.1f%%',
                        colors=['#2ecc71', '#e74c3c'])
                plt.title('Role Selection Accuracy')
        except Exception as e:
            print(f"Error in role accuracy plot: {e}")
            plt.text(0.5, 0.5, f"Error creating plot: {str(e)}", 
                    ha='center', va='center', fontsize=14)
            plt.title('Role Accuracy (Error)')
        
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