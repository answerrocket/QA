# file_executor.py
import subprocess
import sys
import argparse
from pathlib import Path

class FileExecutor:
    def __init__(self, python_path=None):
        self.python_path = python_path or sys.executable

    def run_file(self, filepath):
        """Execute a Python file and return output"""
        try:
            # Convert to Path object and resolve to absolute path
            file_path = Path(filepath).resolve()

            # Check if file exists
            if not file_path.exists():
                return {
                    'stdout': '',
                    'stderr': f"File not found: {filepath}",
                    'returncode': -1,
                    'success': False
                }

            result = subprocess.run(
                [self.python_path, str(file_path)],
                capture_output=True,
                text=True,
                cwd=file_path.parent  # Set working dir to file's directory
            )

            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'success': result.returncode == 0
            }
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'success': False
            }

    def run_code(self, code_string):
        """Execute Python code string and return output"""
        try:
            result = subprocess.run(
                [self.python_path, '-c', code_string],
                capture_output=True,
                text=True
            )

            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'success': result.returncode == 0
            }
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'success': False
            }

    def run_input(self, input_str):
        """Execute input as file if it exists, otherwise as Python code"""
        # Check if input is a file path that exists
        if Path(input_str).exists():
            return self.run_file(input_str)
        # Check if input looks like a file path (has .py extension or path separators)
        elif (input_str.endswith('.py') or '/' in input_str or '\\' in input_str):
            # Treat as file path but it doesn't exist
            return {
                'stdout': '',
                'stderr': f"File not found: {input_str}",
                'returncode': 1,
                'success': False
            }
        else:
            return self.run_code(input_str)

def main():
    """Main function to run Python code or file specified as command line argument"""
    parser = argparse.ArgumentParser(description='Execute a Python file or code string and display output')
    parser.add_argument('input', help='Path to Python file or Python code string to execute')
    parser.add_argument('--python-path', help='Path to Python interpreter (optional)')

    args = parser.parse_args()

    executor = FileExecutor(python_path=args.python_path)
    result = executor.run_input(args.input)

    print("=== EXECUTION OUTPUT ===")
    if result['stdout']:
        print(result['stdout'])

    if result['stderr']:
        print("=== ERRORS ===")
        print(result['stderr'])

    print(f"=== EXECUTION COMPLETE (Return Code: {result['returncode']}) ===")

    # Exit with the same return code as the executed script
    sys.exit(result['returncode'])

if __name__ == "__main__":
    main()
