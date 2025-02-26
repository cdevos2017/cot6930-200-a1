# prompt/__init__.py

"""
Prompt Engineering Package
"""

# Core functionality
from .prompt_refiner import iterative_prompt_refinement, format_final_prompt
from .template_generator import determine_template
from .utils import format_prompt_with_template

# Templates module exports
from .templates import (
    get_role_template,
    get_technique_template,
    get_l1_technique_template,
    get_l2_technique_step_template,
    get_l2_technique_steps_count,
    list_all_templates
)

# Techniques module exports
from .techniques import (
    apply_technique,
    select_technique,
    get_technique_description,
    get_l1_technique_names,
    get_l2_technique_names,
    apply_l1_technique,
    execute_l2_technique_step,
    execute_l2_technique_full
)

# Parameters module exports
from .parameters import (
    get_parameters_for_task,
    validate_parameters,
    merge_parameters,
    get_parameter_presets
)

__all__ = [
    # Core functions
    'iterative_prompt_refinement',
    'format_final_prompt',
    'determine_template',
    'format_prompt_with_template',
    
    # Template functions
    'get_role_template',
    'get_technique_template',
    'get_l1_technique_template',
    'get_l2_technique_step_template',
    'get_l2_technique_steps_count',
    'list_all_templates',
    
    # Technique functions
    'apply_technique',
    'select_technique',
    'get_technique_description',
    'get_l1_technique_names',
    'get_l2_technique_names',
    'apply_l1_technique',
    'execute_l2_technique_step',
    'execute_l2_technique_full',
    
    # Parameter functions
    'get_parameters_for_task',
    'validate_parameters',
    'merge_parameters',
    'get_parameter_presets'
]