from dotenv import load_dotenv
from skill_framework import SkillInput, SkillOutput
import argparse
import os
import pandas
import json
import types
import importlib.util
import sys
from pathlib import Path

def run_skill(skill_name: str, parameters: dict = None) -> SkillOutput:
    """Run a skill locally with optional parameters

    Args:
        skill_name (str): Name of the skill to execute (function name or file name)
        parameters (dict, optional): Dictionary of parameters to pass to the skill. Defaults to None.

    Returns:
        SkillOutput: The result from the skill execution
    """
    load_dotenv()

    # Prepare the parameters for the skill call
    if parameters is None:
        parameters = {}

    # Create arguments object from parameters
    args = types.SimpleNamespace()
    for key, value in parameters.items():
        setattr(args, key, value)

    # Create SkillInput object
    skill_input = SkillInput(assistant_id='local-test', arguments=args)

    # Try to find and import the skill function
    skill_function = _find_skill_function(skill_name)

    if skill_function is None:
        raise Exception(f"Skill function '{skill_name}' not found")

    # Execute the skill
    try:
        result = skill_function(skill_input)
        if not isinstance(result, SkillOutput):
            raise Exception(f"Skill function must return SkillOutput, got {type(result)}")
        return result
    except Exception as e:
        raise Exception(f"Error executing skill '{skill_name}': {str(e)}")

def _find_skill_function(skill_name: str):
    """Find and import a skill function by name or file"""

    # First, try to find a Python file with the skill name
    current_dir = Path.cwd()
    skill_file = current_dir / f"{skill_name}.py"

    if skill_file.exists():
        # Import the module from file
        spec = importlib.util.spec_from_file_location(skill_name, skill_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Look for functions that are decorated with @skill
        skill_functions = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr):
                # Check if it's a skill function (decorated with @skill)
                type_str = str(type(attr))
                if 'skill_framework.skills.Skill' in type_str:
                    skill_functions.append((attr_name, attr))
                elif hasattr(attr, '__name__') and (hasattr(attr, '_skill_metadata') or hasattr(attr, 'skill_name')):
                    skill_functions.append((attr_name, attr))
                elif hasattr(attr, '__name__') and (attr_name.endswith('_analysis') or attr_name.endswith('_skill')):
                    # Common skill function naming patterns
                    skill_functions.append((attr_name, attr))

        # Return the first skill function found
        if skill_functions:
            return skill_functions[0][1]

        # If no decorated functions, look for main function patterns
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and not attr_name.startswith('_') and attr_name != 'main':
                # Check if function signature matches skill pattern
                import inspect
                sig = inspect.signature(attr)
                params = list(sig.parameters.keys())
                if len(params) == 1 and 'parameters' in params[0].lower():
                    return attr

    # If file not found, try to import from current directory modules
    try:
        module = importlib.import_module(skill_name)
        if hasattr(module, skill_name):
            return getattr(module, skill_name)
    except ImportError:
        pass

    return None

def main():
    """Main function to run a skill locally"""
    parser = argparse.ArgumentParser(description='Run a skill locally using skill-framework')
    parser.add_argument('skill_name', help='Name of the skill to run (function name or file name without .py)')
    parser.add_argument('--parameters', '-p', help='Parameters as JSON string (optional)', default='{}')

    args = parser.parse_args()

    try:
        # Parse the parameters JSON string
        parameters = json.loads(args.parameters)

        print(f"Running skill '{args.skill_name}' with parameters: {parameters}")
        result = run_skill(args.skill_name, parameters)

        print(f"\n✅ Skill executed successfully!")
        print(f"\n📝 Final Prompt:")
        print(result.final_prompt)

        if result.visualizations:
            print(f"\n📊 Visualizations ({len(result.visualizations)}):")
            for i, viz in enumerate(result.visualizations, 1):
                print(f"  {i}. {viz.title}")

        if result.export_data:
            print(f"\n📁 Export Data ({len(result.export_data)}):")
            for i, export in enumerate(result.export_data, 1):
                print(f"  {i}. {export.name}")
                if hasattr(export.data, 'shape'):
                    print(f"     Shape: {export.data.shape}")

    except json.JSONDecodeError as e:
        print(f"❌ Error parsing parameters JSON: {e}")
        print(f"   Parameters provided: {args.parameters}")
        print('   Expected format: {"param1": "value1", "param2": "value2"}')
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
