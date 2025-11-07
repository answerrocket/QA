"""
Visualization Testing Module for Claude Code
Provides JSON validation and console error detection for skill visualizations
"""

from playwright.sync_api import sync_playwright
import json
import time
import subprocess
import os
import signal
import tempfile
import shutil
from typing import Dict, List
from dataclasses import dataclass
from skill_framework import SkillOutput, SkillVisualization, preview_skill


@dataclass
class ValidationResult:
    """Result of visualization validation"""
    success: bool
    errors: List[str]
    warnings: List[str]
    console_logs: List[Dict]
    performance_metrics: Dict


class VisualizationTester:
    """
    Visualization testing for Claude Code with temporary file cleanup
    """

    def __init__(self,
                 preview_port: int = 8484,
                 headless: bool = True):
        self.preview_port = preview_port
        self.headless = headless
        self.server_process = None
        self.base_url = f"http://localhost:{preview_port}"
        self.temp_dir = None
        self.original_cwd = None

    def start_preview_server(self) -> bool:
        """Start the skill-framework preview server with temporary directory"""
        try:
            # Create temporary directory for preview files
            self.temp_dir = tempfile.mkdtemp(prefix="viz_test_")
            self.original_cwd = os.getcwd()

            # Change to temp directory
            os.chdir(self.temp_dir)

            # Create required resources directory
            os.makedirs("resources", exist_ok=True)

            # Start the preview server
            self.server_process = subprocess.Popen(
                [os.path.join(self.original_cwd, ".venv/bin/preview-server")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )

            # Wait for server to start
            time.sleep(3)

            # Check if server is running
            if self.server_process.poll() is None:
                print(f"✅ Preview server started on {self.base_url} (temp dir: {self.temp_dir})")
                return True
            else:
                print("❌ Failed to start preview server")
                self._cleanup_temp_files()
                return False

        except Exception as e:
            print(f"❌ Error starting preview server: {e}")
            self._cleanup_temp_files()
            return False

    def stop_preview_server(self):
        """Stop the preview server and clean up temporary files"""
        if self.server_process:
            try:
                # Kill the process group to ensure all child processes are terminated
                os.killpg(os.getpgid(self.server_process.pid), signal.SIGTERM)
                self.server_process.wait(timeout=5)
                print("✅ Preview server stopped")
            except Exception as e:
                print(f"⚠️ Error stopping preview server: {e}")
                try:
                    os.killpg(os.getpgid(self.server_process.pid), signal.SIGKILL)
                except:
                    pass

        self._cleanup_temp_files()

    def _cleanup_temp_files(self):
        """Clean up temporary files and restore working directory"""
        try:
            # Restore original working directory
            if self.original_cwd:
                os.chdir(self.original_cwd)

            # Remove temporary directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                print(f"🧹 Cleaned up temporary files: {self.temp_dir}")

        except Exception as e:
            print(f"⚠️ Error cleaning up temporary files: {e}")
        finally:
            self.temp_dir = None
            self.original_cwd = None

    def print_test_results(self, result: ValidationResult, test_name: str = "Visualization Test"):
        """Print formatted test results"""
        print(f"\n📊 {test_name} Results:")
        print(f"{'='*50}")

        if result.success:
            print("✅ Status: PASSED")
        else:
            print("❌ Status: FAILED")

        if result.errors:
            print(f"\n❌ Errors ({len(result.errors)}):")
            for error in result.errors:
                print(f"  • {error}")

        if result.warnings:
            print(f"\n⚠️ Warnings ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  • {warning}")

        if result.console_logs:
            print(f"\n📝 Console Logs ({len(result.console_logs)}):")
            for log in result.console_logs:
                icon = "❌" if log["type"] == "error" else "⚠️" if log["type"] == "warning" else "ℹ️"
                print(f"  {icon} [{log['type'].upper()}] {log['text']}")

        if result.performance_metrics:
            print(f"\n⚡ Performance:")
            for key, value in result.performance_metrics.items():
                if key == "page_load_time":
                    print(f"  • Load Time: {value:.2f}s")
                elif key == "response_status":
                    print(f"  • Response Status: {value}")
                else:
                    print(f"  • {key}: {value}")

        print(f"{'='*50}")



    def test_skill_visualization(self,
                                skill_function,
                                skill_output: SkillOutput,
                                test_name: str = None) -> ValidationResult:
        """
        Test skill visualization with full browser validation using temporary files

        Args:
            skill_function: The skill function (decorated with @skill)
            skill_output: The SkillOutput containing visualizations
            test_name: Optional name for the test (defaults to skill function name)

        Returns:
            ValidationResult with comprehensive test results
        """
        if test_name is None:
            # Try different ways to get the skill name
            test_name = getattr(skill_function, '__name__', None)
            if test_name is None and hasattr(skill_function, 'fn'):
                test_name = getattr(skill_function.fn, '__name__', None)
            if test_name is None:
                test_name = 'unknown_skill'

        print(f"🧪 Testing visualization for: {test_name}")

        # First validate JSON structure
        all_errors = []
        all_warnings = []

        for i, viz in enumerate(skill_output.visualizations):
            json_result = self.test_visualization_json(viz)
            if not json_result.success:
                all_errors.extend([f"Viz {i}: {error}" for error in json_result.errors])
            all_warnings.extend([f"Viz {i}: {warning}" for warning in json_result.warnings])

        # If JSON is invalid, don't proceed to browser test
        if all_errors:
            return ValidationResult(
                success=False,
                errors=all_errors,
                warnings=all_warnings,
                console_logs=[],
                performance_metrics={}
            )

        # Generate preview files in temporary directory
        try:
            preview_skill(skill_function, skill_output)
            print(f"✅ Preview files generated for {test_name}")
        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[f"Failed to generate preview files: {str(e)}"],
                warnings=all_warnings,
                console_logs=[],
                performance_metrics={}
            )

        # Test the visualization in browser
        return self._test_visualization_in_browser(test_name, all_warnings)

    def _test_visualization_in_browser(self, skill_name: str, existing_warnings: List[str]) -> ValidationResult:
        """Test visualization rendering in browser using Playwright"""
        console_logs = []
        errors = []
        warnings = existing_warnings.copy()
        performance_metrics = {}

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()

                # Set up console and error monitoring
                page.on("console", lambda msg: console_logs.append({
                    "type": msg.type,
                    "text": msg.text,
                    "location": str(msg.location) if msg.location else "unknown"
                }))

                page.on("pageerror", lambda err: console_logs.append({
                    "type": "error",
                    "text": str(err),
                    "location": "page"
                }))

                # Navigate to the preview page
                preview_url = f"{self.base_url}/print/{skill_name}"
                print(f"🌐 Loading: {preview_url}")

                start_time = time.time()
                response = page.goto(preview_url, wait_until="networkidle")
                load_time = time.time() - start_time

                performance_metrics["page_load_time"] = load_time
                performance_metrics["response_status"] = response.status if response else None

                # Wait for charts to render
                page.wait_for_timeout(5000)  # 5 seconds for charts to fully render

                # Check for specific error patterns
                errors.extend(self._check_for_visualization_errors(console_logs))
                warnings.extend(self._check_for_visualization_warnings(console_logs))

                # Check if charts are actually rendered
                chart_elements = page.query_selector_all('[data-highcharts-chart]')
                if not chart_elements:
                    warnings.append("No Highcharts elements found on page")
                else:
                    print(f"✅ Found {len(chart_elements)} chart element(s)")

                browser.close()

        except Exception as e:
            errors.append(f"Browser testing failed: {str(e)}")

        success = len(errors) == 0
        return ValidationResult(
            success=success,
            errors=errors,
            warnings=warnings,
            console_logs=console_logs,
            performance_metrics=performance_metrics
        )

    def _check_for_visualization_errors(self, console_logs: List[Dict]) -> List[str]:
        """Check console logs for visualization-specific errors"""
        errors = []

        error_patterns = [
            "l.call is not a function",  # Common Highcharts error from JS functions in JSON
            "Highcharts error",
            "Cannot read property",
            "TypeError",
            "ReferenceError",
            "SyntaxError",
            "Failed to load",
            "404",
            "500"
        ]

        for log in console_logs:
            if log["type"] == "error":
                log_text = log["text"].lower()
                for pattern in error_patterns:
                    if pattern.lower() in log_text:
                        errors.append(f"Console Error: {log['text']}")
                        break

        return errors

    def _check_for_visualization_warnings(self, console_logs: List[Dict]) -> List[str]:
        """Check console logs for visualization warnings"""
        warnings = []

        warning_patterns = [
            "deprecated",
            "warning",
            "fallback",
            "missing",
            "invalid"
        ]

        for log in console_logs:
            if log["type"] == "warning":
                log_text = log["text"].lower()
                for pattern in warning_patterns:
                    if pattern.lower() in log_text:
                        warnings.append(f"Console Warning: {log['text']}")
                        break

        return warnings

    def _check_highcharts_config(self, layout_dict: Dict, viz_index: int, errors: List[str], warnings: List[str]):
        """Check for common Highcharts configuration issues that cause console errors"""
        def check_component(component, path=""):
            if not isinstance(component, dict):
                return

            # Check for HighchartsChart components
            if component.get("type") == "HighchartsChart":
                options = component.get("options", {})

                # Check for common formatter issues
                self._check_formatter_issues(options, f"{path}.options", viz_index, errors, warnings)

                # Check for missing required properties
                if not options:
                    warnings.append(f"Viz {viz_index}: HighchartsChart at {path} missing options")

            # Recursively check children
            children = component.get("children", [])
            if isinstance(children, list):
                for i, child in enumerate(children):
                    check_component(child, f"{path}.children[{i}]")

        # Check the entire layout
        check_component(layout_dict, "root")

    def _check_formatter_issues(self, options: Dict, path: str, viz_index: int, errors: List[str], warnings: List[str]):
        """Check for formatter function issues in Highcharts options"""
        def check_formatters(obj, obj_path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{obj_path}.{key}" if obj_path else key

                    # Check for formatter functions
                    if key == "formatter" and isinstance(value, str):
                        if "function" in value.lower():
                            errors.append(f"Viz {viz_index}: Formatter function at {path}.{current_path} - use template strings instead")
                        elif "{" not in value and "}" not in value:
                            warnings.append(f"Viz {viz_index}: Formatter at {path}.{current_path} may need template string syntax")

                    # Recursively check nested objects
                    elif isinstance(value, (dict, list)):
                        check_formatters(value, current_path)

            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    check_formatters(item, f"{obj_path}[{i}]")

        check_formatters(options)



    def test_visualization_json(self, visualization: SkillVisualization) -> ValidationResult:
        """
        Test visualization JSON structure without browser rendering

        Args:
            visualization: SkillVisualization object to validate

        Returns:
            ValidationResult with JSON validation results
        """
        errors = []
        warnings = []

        try:
            # Test JSON parsing
            layout_dict = json.loads(visualization.layout)

            # Check required Document properties
            required_props = ["type", "rows", "columns", "rowHeight", "colWidth", "gap", "children"]
            for prop in required_props:
                if prop not in layout_dict:
                    errors.append(f"Missing required Document property: {prop}")

            # Check Document type
            if layout_dict.get("type") != "Document":
                errors.append(f"Root type must be 'Document', got: {layout_dict.get('type')}")

            # Check children structure
            if "children" in layout_dict:
                self._validate_children_structure(layout_dict["children"], errors, warnings)

            # Check for JavaScript functions in JSON (common error)
            layout_str = visualization.layout
            if "function(" in layout_str or "function (" in layout_str:
                errors.append("JavaScript functions found in JSON - use Highcharts template strings instead")

        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in layout: {str(e)}")
        except Exception as e:
            errors.append(f"Layout validation error: {str(e)}")

        return ValidationResult(
            success=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            console_logs=[],
            performance_metrics={}
        )

    def _validate_children_structure(self, children, errors: List[str], warnings: List[str]):
        """Validate the children array structure"""
        if not isinstance(children, list):
            errors.append("Children must be an array, not a string or other type")
            return

        for i, child in enumerate(children):
            if not isinstance(child, dict):
                errors.append(f"Child {i} must be an object")
                continue

            # Check required properties
            if "type" not in child:
                errors.append(f"Child {i} missing required 'type' property")

            # Check children property
            if "children" in child and not isinstance(child["children"], list):
                errors.append(f"Child {i} 'children' property must be an array")

            # Validate Highcharts specific properties
            if child.get("type") == "HighchartsChart":
                if "options" not in child:
                    warnings.append(f"HighchartsChart {i} missing 'options' property")




# Convenience functions for Claude Code execution
def test_skill_visualization_standalone(skill_file_path: str,
                                      skill_name: str,
                                      test_parameters: Dict = None,
                                      headless: bool = True) -> Dict:
    """
    Standalone function for testing skill visualizations that Claude Code can execute
    Uses temporary files with automatic cleanup

    Args:
        skill_file_path: Path to the skill Python file
        skill_name: Name of the skill function
        test_parameters: Optional parameters to pass to the skill
        headless: Whether to run browser in headless mode

    Returns:
        Dict with test results that can be easily parsed
    """
    import importlib.util

    results = {
        "success": False,
        "errors": [],
        "warnings": [],
        "console_logs": [],
        "performance_metrics": {},
        "test_summary": ""
    }

    tester = None
    try:
        # Import the skill module
        spec = importlib.util.spec_from_file_location("test_skill", skill_file_path)
        skill_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(skill_module)

        # Get the skill function
        if not hasattr(skill_module, skill_name):
            results["errors"].append(f"Skill function '{skill_name}' not found in {skill_file_path}")
            return results

        skill_function = getattr(skill_module, skill_name)

        # Create mock parameters if none provided
        if test_parameters is None:
            test_parameters = {}

        # Create mock SkillInput
        class MockSkillInput:
            def __init__(self, params):
                self.arguments = type('obj', (object,), params)()
                self.user_full_query = "Test query for visualization validation"
                self.workflow_id = "viz-test-workflow"

        # Execute the skill
        mock_input = MockSkillInput(test_parameters)
        skill_output = skill_function(mock_input)

        # Test the visualization with full browser validation
        tester = VisualizationTester(headless=headless)

        # Start server
        if not tester.start_preview_server():
            results["errors"].append("Failed to start preview server")
            return results

        try:
            # Test the visualization
            validation_result = tester.test_skill_visualization(skill_function, skill_output)

            # Convert ValidationResult to dict
            results["success"] = validation_result.success
            results["errors"] = validation_result.errors
            results["warnings"] = validation_result.warnings
            results["console_logs"] = validation_result.console_logs
            results["performance_metrics"] = validation_result.performance_metrics

            # Create summary
            if validation_result.success:
                results["test_summary"] = f"✅ Visualization test PASSED for {skill_name}"
            else:
                results["test_summary"] = f"❌ Visualization test FAILED for {skill_name} - {len(validation_result.errors)} errors"

        finally:
            # Always stop server and cleanup
            tester.stop_preview_server()

    except Exception as e:
        results["errors"].append(f"Test execution failed: {str(e)}")
        results["test_summary"] = f"❌ Test execution failed: {str(e)}"

    finally:
        # Ensure cleanup even if there's an exception
        if tester:
            tester.stop_preview_server()

    return results


def quick_json_validation(skill_file_path: str, skill_name: str, test_parameters: Dict = None) -> Dict:
    """
    Quick JSON-only validation that doesn't require browser or server
    Perfect for Claude Code to validate visualization JSON structure

    Args:
        skill_file_path: Path to the skill Python file
        skill_name: Name of the skill function
        test_parameters: Optional parameters to pass to the skill

    Returns:
        Dict with validation results
    """
    import importlib.util

    results = {
        "success": False,
        "errors": [],
        "warnings": [],
        "test_summary": ""
    }

    try:
        # Import the skill module
        spec = importlib.util.spec_from_file_location("test_skill", skill_file_path)
        skill_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(skill_module)

        # Get the skill function
        if not hasattr(skill_module, skill_name):
            results["errors"].append(f"Skill function '{skill_name}' not found in {skill_file_path}")
            return results

        skill_function = getattr(skill_module, skill_name)

        # Create mock parameters if none provided
        if test_parameters is None:
            test_parameters = {}

        # Create mock SkillInput
        class MockSkillInput:
            def __init__(self, params):
                self.arguments = type('obj', (object,), params)()
                self.user_full_query = "Test query for JSON validation"
                self.workflow_id = "json-test-workflow"

        # Execute the skill
        mock_input = MockSkillInput(test_parameters)
        skill_output = skill_function(mock_input)

        # Validate each visualization's JSON
        tester = VisualizationTester()
        all_passed = True

        for i, viz in enumerate(skill_output.visualizations):
            validation_result = tester.test_visualization_json(viz)

            if not validation_result.success:
                all_passed = False
                results["errors"].extend([f"Viz {i}: {error}" for error in validation_result.errors])

            results["warnings"].extend([f"Viz {i}: {warning}" for warning in validation_result.warnings])

        results["success"] = all_passed

        if all_passed:
            results["test_summary"] = f"✅ JSON validation PASSED for {skill_name} ({len(skill_output.visualizations)} visualizations)"
        else:
            results["test_summary"] = f"❌ JSON validation FAILED for {skill_name} - {len(results['errors'])} errors"

    except Exception as e:
        results["errors"].append(f"JSON validation failed: {str(e)}")
        results["test_summary"] = f"❌ JSON validation failed: {str(e)}"

    return results


# Convenience functions for easy testing
def quick_test_visualization(skill_function, skill_output: SkillOutput, headless: bool = True) -> bool:
    """
    Quick test of a skill visualization - returns True if successful

    Args:
        skill_function: The skill function
        skill_output: The skill output containing visualizations
        headless: Whether to run browser in headless mode

    Returns:
        bool: True if all tests pass, False otherwise
    """
    tester = VisualizationTester(headless=headless)

    try:
        # Start server
        if not tester.start_preview_server():
            print("❌ Failed to start preview server")
            return False

        # Test the visualization
        result = tester.test_skill_visualization(skill_function, skill_output)
        tester.print_test_results(result)

        return result.success

    finally:
        tester.stop_preview_server()


def test_visualization_json_only(visualization: SkillVisualization) -> bool:
    """
    Test only the JSON structure of a visualization (no browser testing)

    Args:
        visualization: SkillVisualization to test

    Returns:
        bool: True if JSON is valid, False otherwise
    """
    tester = VisualizationTester()
    result = tester.test_visualization_json(visualization)
    tester.print_test_results(result, "JSON Structure Test")
    return result.success


def check_webpage(url: str = "http://localhost:8484", headless: bool = False) -> Dict:
    """
    Simple webpage checker (original functionality preserved)

    Args:
        url: URL to check
        headless: Whether to run browser in headless mode

    Returns:
        Dict with console logs and basic info
    """
    console_logs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # Capture all console messages
        page.on("console", lambda msg: console_logs.append({
            "type": msg.type,
            "text": msg.text
        }))

        # Capture page errors
        page.on("pageerror", lambda err: console_logs.append({
            "type": "error",
            "text": str(err)
        }))

        # Load the page
        page.goto(url)
        page.wait_for_timeout(3000)  # Wait 3 seconds for JS to run

        browser.close()

    return {
        "url": url,
        "console": console_logs
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Check if it's a skill file test
        if sys.argv[1].endswith('.py') and len(sys.argv) > 2:
            # Test a skill file: python viz_previewer.py skill_file.py skill_function_name
            skill_file = sys.argv[1]
            skill_name = sys.argv[2]

            print(f"🧪 Testing skill: {skill_name} from {skill_file}")

            # Quick JSON validation first
            json_result = quick_json_validation(skill_file, skill_name)
            print(f"📝 JSON Validation: {json_result['test_summary']}")

            if json_result["errors"]:
                print("❌ JSON Errors:")
                for error in json_result["errors"]:
                    print(f"  - {error}")

            # Full browser test if JSON is valid
            if json_result["success"]:
                print("\n🌐 Running full browser test...")
                full_result = test_skill_visualization_standalone(skill_file, skill_name)
                print(f"🎯 Full Test: {full_result['test_summary']}")

                if full_result["errors"]:
                    print("❌ Browser Test Errors:")
                    for error in full_result["errors"]:
                        print(f"  - {error}")

                # Note: No screenshots in this version - focused on console validation
        else:
            # Original functionality - check a webpage
            url = sys.argv[1]
            result = check_webpage(url, headless=False)
            print(json.dumps(result, indent=2))
    else:
        # Demo the new functionality
        print("🧪 Visualization Tester")
        print("Usage:")
        print("1. Test a webpage: python viz_previewer.py http://localhost:8484")
        print("2. Test a skill: python viz_previewer.py skill_file.py skill_function_name")
        print("3. Use in code:")
        print("   from viz_previewer import quick_json_validation, test_skill_visualization_standalone")
        print("   result = quick_json_validation('my_skill.py', 'my_skill_function')")
        print("   result = test_skill_visualization_standalone('my_skill.py', 'my_skill_function')")

        # Test the preview server if it's running
        try:
            result = check_webpage("http://localhost:8484", headless=True)
            if result["console"]:
                print(f"\n📝 Preview server test - found {len(result['console'])} console messages")
            else:
                print("\n✅ Preview server appears to be running cleanly")
        except Exception as e:
            print(f"\n⚠️ Could not connect to preview server: {e}")
            print("Make sure to run 'preview-server' first")


# Convenience functions for easy testing
def quick_test_visualization(skill_function, skill_output: SkillOutput, headless: bool = True) -> bool:
    """
    Quick test of a skill visualization - returns True if successful

    Args:
        skill_function: The skill function
        skill_output: The skill output containing visualizations
        headless: Whether to run browser in headless mode

    Returns:
        bool: True if all tests pass, False otherwise
    """
    tester = VisualizationTester(headless=headless)

    try:
        # Start server
        if not tester.start_preview_server():
            print("❌ Failed to start preview server")
            return False

        # Test the visualization
        result = tester.test_skill_visualization(skill_function, skill_output)
        tester.print_test_results(result)

        return result.success

    finally:
        tester.stop_preview_server()


def test_visualization_json_only(visualization: SkillVisualization) -> bool:
    """
    Test only the JSON structure of a visualization (no browser testing)

    Args:
        visualization: SkillVisualization to test

    Returns:
        bool: True if JSON is valid, False otherwise
    """
    tester = VisualizationTester()
    result = tester.test_visualization_json(visualization)
    tester.print_test_results(result, "JSON Structure Test")
    return result.success


def check_webpage(url: str = "http://localhost:8484", headless: bool = False) -> Dict:
    """
    Simple webpage checker (original functionality preserved)

    Args:
        url: URL to check
        headless: Whether to run browser in headless mode

    Returns:
        Dict with console logs and basic info
    """
    console_logs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # Capture all console messages
        page.on("console", lambda msg: console_logs.append({
            "type": msg.type,
            "text": msg.text
        }))

        # Capture page errors
        page.on("pageerror", lambda err: console_logs.append({
            "type": "error",
            "text": str(err)
        }))

        # Load the page
        page.goto(url)
        page.wait_for_timeout(3000)  # Wait 3 seconds for JS to run

        browser.close()

    return {
        "url": url,
        "console": console_logs
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Check if it's a skill file test
        if sys.argv[1].endswith('.py') and len(sys.argv) > 2:
            # Test a skill file: python viz_previewer.py skill_file.py skill_function_name
            skill_file = sys.argv[1]
            skill_name = sys.argv[2]

            print(f"🧪 Testing skill: {skill_name} from {skill_file}")

            # Quick JSON validation first
            json_result = quick_json_validation(skill_file, skill_name)
            print(f"📝 JSON Validation: {json_result['test_summary']}")

            if json_result["errors"]:
                print("❌ JSON Errors:")
                for error in json_result["errors"]:
                    print(f"  - {error}")

            # Full browser test if JSON is valid
            if json_result["success"]:
                print("\n🌐 Running full browser test...")
                full_result = test_skill_visualization_standalone(skill_file, skill_name)
                print(f"🎯 Full Test: {full_result['test_summary']}")

                if full_result["errors"]:
                    print("❌ Browser Test Errors:")
                    for error in full_result["errors"]:
                        print(f"  - {error}")

                # Note: No screenshots in this version - focused on console validation
        else:
            # Original functionality - check a webpage
            url = sys.argv[1]
            result = check_webpage(url, headless=False)
            print(json.dumps(result, indent=2))
    else:
        # Demo the new functionality
        print("🧪 Visualization Tester for Claude Code")
        print("Usage:")
        print("1. Test a webpage: python viz_previewer.py http://localhost:8484")
        print("2. Test a skill: python viz_previewer.py skill_file.py skill_function_name")
        print("3. Use in code:")
        print("   from viz_previewer import quick_json_validation, test_skill_visualization_standalone")
        print("   result = quick_json_validation('my_skill.py', 'my_skill_function')")
        print("   result = test_skill_visualization_standalone('my_skill.py', 'my_skill_function')")

        print("\n🎯 Visualization testing module is ready for Claude Code!")
        print("✅ Features: JSON validation, console error detection, temporary file cleanup")
        print("✅ No permanent files created during testing")