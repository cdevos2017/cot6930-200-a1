#!/usr/bin/env python3
"""
Debug script to test experiment data saving with minimal dependencies.
This script runs a very simple experiment and ensures the data is saved correctly.
"""

import os
import json
import time
from pathlib import Path
from research.reporting.reporter import ResearchReporter, ResearchReport
from research.visualization import ResearchVisualizer

def run_debug_experiment():
    """Run a simple experiment and save the results"""
    print("Running debug experiment...")
    
    # Create a timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    experiment_id = f"experiment_{timestamp}_debug"
    
    # Create some simple test results
    results = [
        {
            "technique_used": "chain_of_thought",
            "parameters_used": {"temperature": 0.5, "num_ctx": 2048},
            "quality_score": 0.8,
            "iterations_used": 3,
            "time_taken": 2.5,
            "query": "Test query 1",
            "category": "test",
            "expected_role": "Tester",
            "detected_role": "Tester"
        },
        {
            "technique_used": "tree_of_thought",
            "parameters_used": {"temperature": 0.7, "num_ctx": 2048},
            "quality_score": 0.7,
            "iterations_used": 4,
            "time_taken": 3.2,
            "query": "Test query 2",
            "category": "test",
            "expected_role": "Tester",
            "detected_role": "Developer"
        }
    ]
    
    # Create a simple analysis
    analysis = {
        "technique_performance": {
            "chain_of_thought": {
                "avg_quality": 0.8,
                "std_quality": 0.0,
                "avg_iterations": 3.0
            },
            "tree_of_thought": {
                "avg_quality": 0.7,
                "std_quality": 0.0,
                "avg_iterations": 4.0
            }
        },
        "parameter_impact": {
            "temp_0.5_ctx_2048": {
                "avg_quality": 0.8,
                "avg_time": 2.5
            },
            "temp_0.7_ctx_2048": {
                "avg_quality": 0.7,
                "avg_time": 3.2
            }
        },
        "detection_accuracy": {
            "role_detection_accuracy": 0.5
        },
        "role_accuracy": 0.5
    }
    
    # Create a report
    report = ResearchReport(
        title="Debug Experiment Report",
        description="A test report to debug data saving issues",
        results=results,
        analysis=analysis,
        timestamp=timestamp,
        experiment_id=experiment_id
    )
    
    # Create reporter and save report
    reporter = ResearchReporter()
    output_dir = reporter.save_report(report)
    
    print(f"\nDebug experiment completed!")
    print(f"Results saved to: {output_dir}")
    
    # Verify the files were saved
    results_file = output_dir / "raw_results.json"
    if results_file.exists():
        print(f"Success: raw_results.json was saved ({results_file.stat().st_size} bytes)")
        # Load and print the first result as verification
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                print(f"Verified: Loaded {len(saved_data.get('results', []))} results from the file")
        except Exception as e:
            print(f"Error loading saved results: {e}")
    else:
        print(f"Error: raw_results.json was not saved")
    
    return output_dir

if __name__ == "__main__":
    output_dir = run_debug_experiment()
    
    # Verify we can regenerate the report
    try:
        from research.reporting.report_regenerator import regenerate_report
        print("\nTesting report regeneration...")
        regenerate_report(output_dir)
    except ImportError:
        print("\nCouldn't test report regeneration (report_regenerator.py not found)")
    except Exception as e:
        print(f"\nError testing report regeneration: {e}")
        import traceback
        traceback.print_exc()